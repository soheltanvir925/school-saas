from django.db import models
from core.models import School


GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]


class Stream(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='streams')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('school', 'name')
        verbose_name = 'Stream'
        verbose_name_plural = 'Streams'

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class Teacher(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    stream = models.ForeignKey(Stream, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
    specialization = models.CharField(max_length=255, blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='teacher_photos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.school.name})"


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    roll_number = models.CharField(max_length=50)
    section = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    admission_date = models.DateField(blank=True, null=True)
    religion = models.CharField(max_length=100, blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    admission_number = models.CharField(max_length=50, blank=True, null=True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    father_occupation = models.CharField(max_length=255, blank=True, null=True)
    father_mobile = models.CharField(max_length=20, blank=True, null=True)
    father_email = models.EmailField(blank=True, null=True)
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    mother_occupation = models.CharField(max_length=255, blank=True, null=True)
    mother_mobile = models.CharField(max_length=20, blank=True, null=True)
    mother_email = models.EmailField(blank=True, null=True)
    present_address = models.TextField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.roll_number}"


class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.school.name})"



class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms')
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='classrooms')
    subjects = models.ManyToManyField(Subject, related_name='classrooms', blank=True)

    def __str__(self):
        return f"{self.name} - {self.school.name}"


# ─── Exams ───────────────────────────────────────────────────────

class ExamType(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='exam_types')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('school', 'name')

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class Exam(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='exams')
    name = models.CharField(max_length=200)
    exam_type = models.ForeignKey(ExamType, on_delete=models.SET_NULL, null=True, blank=True, related_name='exams')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    exam_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    total_marks = models.PositiveIntegerField()
    passing_marks = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.classroom.name} ({self.school.name})"


# ─── Grading ─────────────────────────────────────────────────────

class GradeScale(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='grade_scales')
    name = models.CharField(max_length=100, help_text="e.g. Primary, Secondary")
    grade_letter = models.CharField(max_length=5)
    min_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    max_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    grade_point = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('school', 'grade_letter')

    def __str__(self):
        return f"{self.grade_letter} ({self.min_percentage}%-{self.max_percentage}%)"


class Grade(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='grades')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    grade_letter = models.CharField(max_length=5, blank=True, null=True)
    grade_point = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    graded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_grades')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('exam', 'student')

    def __str__(self):
        return f"{self.student} - {self.exam}: {self.marks_obtained}/{self.exam.total_marks}"


# ─── Fees ────────────────────────────────────────────────────────

FEE_FREQUENCY_CHOICES = [
    ('monthly', 'Monthly'),
    ('quarterly', 'Quarterly'),
    ('yearly', 'Yearly'),
    ('one_time', 'One Time'),
]

PAYMENT_METHOD_CHOICES = [
    ('cash', 'Cash'),
    ('check', 'Check'),
    ('bank', 'Bank Transfer'),
    ('online', 'Online'),
]

PAYMENT_STATUS_CHOICES = [
    ('paid', 'Paid'),
    ('partial', 'Partial'),
    ('pending', 'Pending'),
    ('overdue', 'Overdue'),
]


class FeeCategory(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='fee_categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('school', 'name')
        verbose_name_plural = 'Fee categories'

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class FeeStructure(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='fee_structures')
    name = models.CharField(max_length=200)
    fee_category = models.ForeignKey(FeeCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='fee_structures')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=FEE_FREQUENCY_CHOICES, default='monthly')
    due_day = models.PositiveSmallIntegerField(blank=True, null=True, help_text="Day of month due (e.g. 10)")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ${self.amount} ({self.school.name})"


class FeePayment(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='fee_payments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='paid')
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - ${self.amount_paid} ({self.payment_date})"


# ─── Attendance ──────────────────────────────────────────────────

ATTENDANCE_STATUS_CHOICES = [
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('late', 'Late'),
    ('holiday', 'Holiday'),
]


class Attendance(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS_CHOICES, default='present')
    remarks = models.TextField(blank=True, null=True)
    marked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='marked_attendance')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'date')
        verbose_name_plural = 'Attendance records'

    def __str__(self):
        return f"{self.student} - {self.date}: {self.status}"
