from django.contrib import admin
from django.utils.html import format_html
from .models import School, SchoolEvent
from users.models import User
from .admin_mixins import SchoolScopedModelAdmin


class SchoolEventInline(admin.TabularInline):
    model = SchoolEvent
    extra = 1
    fields = ('name', 'event_date', 'event_time', 'location', 'is_active')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.school:
            return qs.filter(school=request.user.school)
        return qs

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.school is not None


class UsersInline(admin.TabularInline):
    model = User
    fk_name = 'school'
    extra = 0
    readonly_fields = ('username', 'email', 'role', 'is_staff', 'is_active')
    can_delete = False
    fields = ('username', 'email', 'role', 'is_staff', 'is_active', 'last_login')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'subdomain', 'contact_email', 'is_active', 'student_count', 'teacher_count')
    list_filter = ('is_active',)
    search_fields = ('name', 'contact_email', 'subdomain')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SchoolEventInline, UsersInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'subdomain', 'logo', 'website', 'is_active')
        }),
        ('Contact', {
            'fields': ('address', 'contact_email', 'contact_phone', 'secondary_phone')
        }),
        ('About', {
            'fields': ('about_description', 'mission', 'vision', 'established_year')
        }),
        ('Location', {
            'fields': ('google_map_embed_url',),
            'description': 'Paste either: 1) The full iframe embed code from Google Maps, OR 2) The embed URL (https://www.google.com/maps/embed?...), OR 3) Just the embed parameters (pb=...).'
        }),
        ('Slider Images', {
            'fields': ('slider_image_1', 'slider_image_2', 'slider_image_3'),
            'description': 'Upload 3 images for the landing page hero slider.'
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.school:
            return qs.filter(pk=request.user.school.pk)
        if request.user.is_superuser:
            return qs
        return qs.none()

    def has_add_permission(self, request):
        return request.user.is_superuser and not request.user.school

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and not request.user.school

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser and not request.user.school:
            return True
        if request.user.school:
            if obj is None or obj.pk == request.user.school.pk:
                return True
        return False

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.is_staff and request.user.school is not None


@admin.register(SchoolEvent)
class SchoolEventAdmin(SchoolScopedModelAdmin):
    list_display = ('name', 'event_date', 'location', 'is_active', 'created_at')
    list_filter = ('is_active', 'event_date')
    search_fields = ('name', 'description', 'location')
    date_hierarchy = 'event_date'

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and request.user.school and obj.school.pk == request.user.school.pk:
            return True
        return False
