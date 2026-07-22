from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    fieldsets = UserAdmin.fieldsets + (
        ('School Info', {'fields': ('school', 'role', 'phone', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('School Info', {'fields': ('school', 'role', 'phone', 'address')}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.school:
            return qs.filter(school=request.user.school)
        if request.user.is_superuser:
            return qs
        return qs.none()

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.is_staff and request.user.school is not None

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.pk == request.user.pk:
            return False
        if obj and request.user.school and obj.school.pk == request.user.school.pk:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_staff and request.user.school:
            return True
        return False

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.is_staff and request.user.school is not None

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.school is not None
        if obj.pk == request.user.pk:
            return True
        if request.user.school and obj.school.pk == request.user.school.pk:
            return True
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'school':
            if not request.user.is_superuser and request.user.school:
                from core.models import School
                kwargs['queryset'] = School.objects.filter(pk=request.user.school.pk)
                kwargs['initial'] = request.user.school.pk
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and request.user.school and not change:
            obj.school = request.user.school
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser and request.user.school:
            readonly.append('school')
        return readonly

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        return tuple(list_display)

    def get_list_filter(self, request):
        list_filter = list(super().get_list_filter(request))
        return tuple(list_filter)

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser and request.user.school:
            return UserAdmin.fieldsets + (
                ('School Info', {'fields': ('role', 'phone', 'address')}),
            )
        return super().get_fieldsets(request, obj)
