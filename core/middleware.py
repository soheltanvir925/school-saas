from django.conf import settings
from .models import School
from .utils import set_current_db_name, clear_current_db_name
from django.db import connections

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Admin and auth URLs - determine database based on user's school
        if (request.path.startswith('/admin') or 
            request.path.startswith('/login') or
            request.path.startswith('/logout') or
            request.path.startswith('/password')):
            db_name = 'default'
            
            # For authenticated admin users, use their school's database
            if hasattr(request, 'user') and request.user.is_authenticated:
                if hasattr(request.user, 'school') and request.user.school:
                    try:
                        school = School.objects.only('database_name').get(pk=request.user.school.pk)
                        db_name = school.database_name
                        if db_name not in connections:
                            new_db_config = connections.databases['default'].copy()
                            new_db_config['NAME'] = db_name
                            connections.databases[db_name] = new_db_config
                    except School.DoesNotExist:
                        pass
            
            set_current_db_name(db_name)
            response = self.get_response(request)
            clear_current_db_name()
            return response
        
        host = request.get_host().split(':')[0]
        parts = host.split('.')
        
        # Default to 'default' database
        db_name = 'default'
        
        # Logic to extract subdomain
        # e.g., school1.localhost -> school1
        # e.g., www.school1.localhost -> school1
        if len(parts) >= 2:
            subdomain = parts[0]
            if subdomain == 'www' and len(parts) >= 3:
                subdomain = parts[1]
            
            if subdomain not in ['localhost', '127', '0']:
                try:
                    school = School.objects.only('database_name').get(subdomain=subdomain)
                    db_name = school.database_name
                    
                    # Dynamically configure the connection if not already in DATABASES
                    if db_name not in connections:
                        # Copy default configuration and change the name
                        new_db_config = connections.databases['default'].copy()
                        new_db_config['NAME'] = db_name
                        connections.databases[db_name] = new_db_config
                except School.DoesNotExist:
                    pass

        set_current_db_name(db_name)
        response = self.get_response(request)
        clear_current_db_name()
        return response
