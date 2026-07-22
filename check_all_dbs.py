#!/usr/bin/env python
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connections, connection

# Get all databases
cursor = connection.cursor()
cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname")
all_dbs = [row[0] for row in cursor.fetchall()]

school_dbs = [db for db in all_dbs if db.startswith('school_')]
print(f"Found {len(school_dbs)} school-related databases:\n")

for db_name in school_dbs:
    print(f"=== {db_name} ===")
    try:
        # Dynamically add connection
        if db_name not in connections.databases:
            new_config = connections.databases['default'].copy()
            new_config['NAME'] = db_name
            connections.databases[db_name] = new_config
        
        cur = connections[db_name].cursor()
        
        # Check if users_user table exists
        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users_user')")
        has_users_table = cur.fetchone()[0]
        
        if has_users_table:
            cur.execute("SELECT id, username, email, role, is_staff, is_superuser, is_active FROM users_user ORDER BY id")
            users = cur.fetchall()
            if users:
                print(f"  Users ({len(users)}):")
                for u in users:
                    print(f"    id={u[0]} username={u[1]} email={u[2]} role={u[3]} staff={u[4]} super={u[5]} active={u[6]}")
            else:
                print("  No users found")
        else:
            print("  (users_user table does not exist)")
        
        # Check schools table
        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'core_school')")
        has_school_table = cur.fetchone()[0]
        
        if has_school_table:
            cur.execute("SELECT id, name, subdomain, database_name, is_active FROM core_school ORDER BY id")
            schools = cur.fetchall()
            if schools:
                print(f"  Schools ({len(schools)}):")
                for s in schools:
                    print(f"    id={s[0]} name={s[1]} subdomain={s[2]} db={s[3]} active={s[4]}")
            else:
                print("  No schools found")
        else:
            print("  (core_school table does not exist)")
    except Exception as e:
        print(f"  Error: {e}")
    print()
