from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connections
from core.models import School
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.conf import settings

class Command(BaseCommand):
    help = 'Runs migrations for all tenant databases'

    def handle(self, *args, **options):
        schools = School.objects.all()
        
        # Get default connection parameters
        default_db = settings.DATABASES['default']
        user = default_db.get('USER', 'postgres')
        password = default_db.get('PASSWORD', 'postgres')
        host = default_db.get('HOST', 'localhost')
        port = default_db.get('PORT', '5432')

        for school in schools:
            db_name = school.database_name
            self.stdout.write(f"Processing school: {school.name} (DB: {db_name})")
            
            # 1. Ensure database exists
            try:
                con = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
                con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cur = con.cursor()
                
                cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
                exists = cur.fetchone()
                if not exists:
                    self.stdout.write(f"Creating database {db_name}...")
                    cur.execute(f"CREATE DATABASE {db_name}")
                
                cur.close()
                con.close()
            except Exception as e:
                self.stderr.write(f"Error checking/creating database {db_name}: {e}")
                continue

            # 2. Configure connection dynamically if needed
            if db_name not in connections:
                new_db_config = settings.DATABASES['default'].copy()
                new_db_config['NAME'] = db_name
                connections.databases[db_name] = new_db_config
            
            # 3. Run migrations
            self.stdout.write(f"Running migrations for {db_name}...")
            try:
                call_command('migrate', database=db_name, interactive=False)
                self.stdout.write(self.style.SUCCESS(f"Successfully migrated {db_name}"))
            except Exception as e:
                self.stderr.write(f"Error migrating {db_name}: {e}")
