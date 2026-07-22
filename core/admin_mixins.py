from django.contrib import admin
from core.models import School


class SchoolScopedModelAdmin(admin.ModelAdmin):
    """
    Base admin class for models that are scoped to a school.
    Automatically handles:
    - Filtering queryset to user's school (for non-superusers)
    - Auto-assigning school on create
    - Restricting school dropdown to user's school
    - Hiding school from list_display/list_filter for school-scoped users
    - Making school field readonly for school-scoped users
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.school:
            return qs.filter(school=request.user.school)
        return qs.none()

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.school is not None

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return request.user.school is not None
        if request.user.school and obj.school.pk == request.user.school.pk:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and request.user.school and obj.school.pk == request.user.school.pk:
            return True
        return False

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and request.user.school and not change:
            obj.school = request.user.school

        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'school':
            if not request.user.is_superuser and request.user.school:
                kwargs['queryset'] = School.objects.filter(pk=request.user.school.pk)
                kwargs['initial'] = request.user.school.pk
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser and request.user.school:
            readonly.append('school')
        return readonly

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if not request.user.is_superuser and request.user.school and 'school' in list_display:
            list_display.remove('school')
        return tuple(list_display)

    def get_list_filter(self, request):
        list_filter = list(super().get_list_filter(request))
        if not request.user.is_superuser and request.user.school and 'school' in list_filter:
            list_filter.remove('school')
        return tuple(list_filter)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.is_staff and request.user.school is not None
