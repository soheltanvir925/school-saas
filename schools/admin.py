from django.contrib import admin
from .models import Teacher, Student, Subject, Classroom, Stream, ExamType, Exam, GradeScale, Grade, FeeCategory, FeeStructure, FeePayment, Attendance
from core.admin_mixins import SchoolScopedModelAdmin


@admin.register(Teacher)
class TeacherAdmin(SchoolScopedModelAdmin):
    list_display = ('first_name', 'last_name', 'employee_id', 'get_stream', 'specialization', 'is_active')
    list_filter = ('stream', 'gender', 'is_active')
    search_fields = ('first_name', 'last_name', 'employee_id', 'email', 'specialization')

    def get_stream(self, obj):
        return obj.stream.name if obj.stream else '-'
    get_stream.short_description = 'Stream'
    get_stream.admin_order_field = 'stream__name'

    fieldsets = (
        ('Profile', {
            'fields': ('first_name', 'last_name', 'employee_id', 'profile_photo', 'is_active')
        }),
        ('Contact & Personal', {
            'fields': ('email', 'phone', 'address', 'gender', 'blood_group')
        }),
        ('Professional', {
            'fields': ('stream', 'specialization', 'qualification', 'experience_years', 'date_of_joining')
        }),
        ('Additional', {
            'fields': ('bio',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Student)
class StudentAdmin(SchoolScopedModelAdmin):
    list_display = ('first_name', 'last_name', 'roll_number', 'classroom', 'section', 'is_active')
    list_filter = ('classroom', 'section', 'gender', 'is_active')
    search_fields = ('first_name', 'last_name', 'roll_number', 'email', 'father_name', 'mother_name')

    fieldsets = (
        ('Profile', {
            'fields': ('first_name', 'last_name', 'roll_number', 'classroom', 'section', 'profile_photo', 'is_active')
        }),
        ('Contact & Personal', {
            'fields': ('email', 'phone', 'gender', 'blood_group', 'date_of_birth', 'religion')
        }),
        ('Admission', {
            'fields': ('admission_date', 'joining_date', 'admission_number')
        }),
        ('Father', {
            'fields': ('father_name', 'father_occupation', 'father_mobile', 'father_email')
        }),
        ('Mother', {
            'fields': ('mother_name', 'mother_occupation', 'mother_mobile', 'mother_email')
        }),
        ('Address', {
            'fields': ('present_address', 'permanent_address')
        }),
    )


@admin.register(Subject)
class SubjectAdmin(SchoolScopedModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(Classroom)
class ClassroomAdmin(SchoolScopedModelAdmin):
    list_display = ('name', 'capacity', 'teacher', 'subjects_list')
    search_fields = ('name',)

    def subjects_list(self, obj):
        return ', '.join(obj.subjects.values_list('name', flat=True))
    subjects_list.short_description = 'Subjects'


@admin.register(Stream)
class StreamAdmin(SchoolScopedModelAdmin):
    list_display = ('name', 'code', 'teacher_count')
    search_fields = ('name', 'code')

    def teacher_count(self, obj):
        return obj.teachers.count()
    teacher_count.short_description = 'Teachers'


# ─── Exam Admin ──────────────────────────────────────────────────

@admin.register(ExamType)
class ExamTypeAdmin(SchoolScopedModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Exam)
class ExamAdmin(SchoolScopedModelAdmin):
    list_display = ('name', 'exam_type', 'classroom', 'subject', 'exam_date', 'total_marks', 'is_active')
    list_filter = ('exam_type', 'classroom', 'exam_date', 'is_active')
    search_fields = ('name', 'classroom__name', 'subject__name')
    date_hierarchy = 'exam_date'

    fieldsets = (
        ('Exam Info', {
            'fields': ('name', 'exam_type', 'classroom', 'subject', 'exam_date')
        }),
        ('Timing', {
            'fields': ('start_time', 'end_time')
        }),
        ('Marks', {
            'fields': ('total_marks', 'passing_marks')
        }),
        ('Additional', {
            'fields': ('description', 'is_active'),
            'classes': ('collapse',)
        }),
    )


# ─── Grading Admin ───────────────────────────────────────────────

@admin.register(GradeScale)
class GradeScaleAdmin(SchoolScopedModelAdmin):
    list_display = ('grade_letter', 'min_percentage', 'max_percentage', 'grade_point')
    list_filter = ('grade_letter',)
    search_fields = ('grade_letter', 'name')


@admin.register(Grade)
class GradeAdmin(SchoolScopedModelAdmin):
    list_display = ('student', 'exam', 'marks_obtained', 'grade_letter', 'graded_by')
    list_filter = ('exam', 'grade_letter')
    search_fields = ('student__first_name', 'student__last_name', 'exam__name')
    date_hierarchy = 'created_at'


# ─── Fees Admin ──────────────────────────────────────────────────

@admin.register(FeeCategory)
class FeeCategoryAdmin(SchoolScopedModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(FeeStructure)
class FeeStructureAdmin(SchoolScopedModelAdmin):
    list_display = ('name', 'fee_category', 'amount', 'frequency', 'is_active')
    list_filter = ('frequency', 'is_active')
    search_fields = ('name',)


@admin.register(FeePayment)
class FeePaymentAdmin(SchoolScopedModelAdmin):
    list_display = ('student', 'fee_structure', 'amount_paid', 'payment_date', 'status')
    list_filter = ('status', 'payment_method', 'payment_date')
    search_fields = ('student__first_name', 'student__last_name', 'transaction_id')
    date_hierarchy = 'payment_date'


# ─── Attendance Admin ────────────────────────────────────────────

@admin.register(Attendance)
class AttendanceAdmin(SchoolScopedModelAdmin):
    list_display = ('student', 'classroom', 'date', 'status', 'marked_by')
    list_filter = ('status', 'date', 'classroom')
    search_fields = ('student__first_name', 'student__last_name', 'remarks')
    date_hierarchy = 'date'


