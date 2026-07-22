from django import forms
from django.contrib.auth.hashers import make_password
from .models import Teacher, Student, Classroom, Stream, Subject, ExamType, Exam, GradeScale, Grade, FeeCategory, FeeStructure, FeePayment, Attendance
from users.models import User

TEACHER_DEFAULT_PASSWORD = 'teacher123'


GENDER_CHOICES = [
    ('', 'Select Gender'),
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]


class TeacherForm(forms.Form):
    employee_id = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter teacher ID'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}))
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}))
    date_of_joining = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    stream = forms.ModelChoiceField(queryset=Stream.objects.none(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    qualification = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter qualification'}))
    experience_years = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter years of experience'}))
    username = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}))
    password = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    confirm_password = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat password'}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}))
    city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}))
    state = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter state'}))
    zip_code = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter zip code'}))
    country = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}))
    profile_photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if self.school:
            self.fields['stream'].queryset = Stream.objects.filter(school=self.school)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, school, commit=True, teacher=None):
        if teacher is None:
            teacher = Teacher(school=school)
        teacher.first_name = self.cleaned_data['first_name']
        teacher.last_name = self.cleaned_data.get('last_name', '')
        teacher.email = self.cleaned_data['email']
        teacher.employee_id = self.cleaned_data.get('employee_id', '')
        teacher.phone = self.cleaned_data.get('phone', '')
        teacher.gender = self.cleaned_data.get('gender', '')
        teacher.date_of_birth = self.cleaned_data.get('date_of_birth')
        teacher.date_of_joining = self.cleaned_data.get('date_of_joining')
        teacher.stream = self.cleaned_data.get('stream')
        teacher.qualification = self.cleaned_data.get('qualification', '')
        teacher.experience_years = self.cleaned_data.get('experience_years')
        teacher.username = self.cleaned_data.get('username', '')
        teacher.address = self.cleaned_data.get('address', '')
        teacher.city = self.cleaned_data.get('city', '')
        teacher.state = self.cleaned_data.get('state', '')
        teacher.zip_code = self.cleaned_data.get('zip_code', '')
        teacher.country = self.cleaned_data.get('country', '')
        profile_photo = self.cleaned_data.get('profile_photo')
        if profile_photo:
            teacher.profile_photo = profile_photo
        password = self.cleaned_data.get('password')
        if password:
            teacher.password = make_password(password)
        if commit:
            teacher.save()

        email = self.cleaned_data.get('email')
        if email and not User.objects.filter(username=email).exists():
            user_password = password or TEACHER_DEFAULT_PASSWORD
            User.objects.create(
                username=email,
                email=email,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data.get('last_name', ''),
                password=make_password(user_password),
                school=school,
                role='teacher',
            )

        return teacher



class StudentForm(forms.Form):
    # --- Student Information ---
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
    )
    roll_number = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. S1001'}),
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
    )
    classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    religion = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter religion'}),
        required=False,
    )
    joining_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
        required=False,
    )
    admission_number = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter admission number'}),
        required=False,
    )
    section = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A, B, C'}),
        required=False,
    )
    profile_photo = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email (used as login username)'}),
        required=False,
    )

    # --- Parent Information ---
    father_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter father's name"}),
        required=False,
    )
    father_occupation = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter father's occupation"}),
        required=False,
    )
    father_mobile = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter father's mobile"}),
        required=False,
    )
    father_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Enter father's email"}),
        required=False,
    )
    mother_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter mother's name"}),
        required=False,
    )
    mother_occupation = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter mother's occupation"}),
        required=False,
    )
    mother_mobile = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter mother's mobile"}),
        required=False,
    )
    mother_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Enter mother's email"}),
        required=False,
    )
    present_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter present address'}),
        required=False,
    )
    permanent_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter permanent address'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if self.school:
            self.fields['classroom'].queryset = Classroom.objects.filter(school=self.school)

    def save(self, school, commit=True, student=None):
        if student is None:
            student = Student(school=school)
        student.first_name = self.cleaned_data['first_name']
        student.last_name = self.cleaned_data['last_name']
        student.email = self.cleaned_data.get('email') or None
        student.roll_number = self.cleaned_data['roll_number']
        student.gender = self.cleaned_data.get('gender')
        student.date_of_birth = self.cleaned_data.get('date_of_birth')
        student.classroom = self.cleaned_data.get('classroom')
        student.religion = self.cleaned_data.get('religion')
        student.joining_date = self.cleaned_data.get('joining_date')
        student.phone = self.cleaned_data.get('phone')
        student.admission_number = self.cleaned_data.get('admission_number')
        student.section = self.cleaned_data.get('section')
        student.profile_photo = self.cleaned_data.get('profile_photo')
        student.father_name = self.cleaned_data.get('father_name')
        student.father_occupation = self.cleaned_data.get('father_occupation')
        student.father_mobile = self.cleaned_data.get('father_mobile')
        student.father_email = self.cleaned_data.get('father_email')
        student.mother_name = self.cleaned_data.get('mother_name')
        student.mother_occupation = self.cleaned_data.get('mother_occupation')
        student.mother_mobile = self.cleaned_data.get('mother_mobile')
        student.mother_email = self.cleaned_data.get('mother_email')
        student.present_address = self.cleaned_data.get('present_address')
        student.permanent_address = self.cleaned_data.get('permanent_address')
        if commit:
            student.save()

        email = self.cleaned_data.get('email')
        if email and not User.objects.filter(username=email).exists():
            User.objects.create(
                username=email,
                email=email,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                password=make_password('student123'),
                school=school,
                role='student',
            )

        return student


class StreamForm(forms.ModelForm):
    class Meta:
        model = Stream
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter stream name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. SCI, COM'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. MTH101'}),
        }


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'capacity', 'teacher', 'subjects']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Class 10'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max students'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['teacher'].queryset = Teacher.objects.filter(school=school)
            self.fields['subjects'].queryset = Subject.objects.filter(school=school)


# ─── Exam Forms ──────────────────────────────────────────────────

class ExamTypeForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Midterm, Final, Quiz'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'exam_type', 'classroom', 'subject', 'exam_date', 'start_time', 'end_time', 'total_marks', 'passing_marks', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter exam name'}),
            'exam_type': forms.Select(attrs={'class': 'form-control'}),
            'classroom': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 100'}),
            'passing_marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 40'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['exam_type'].queryset = ExamType.objects.filter(school=school)
            self.fields['classroom'].queryset = Classroom.objects.filter(school=school)
            self.fields['subject'].queryset = Subject.objects.filter(school=school)


# ─── Grading Forms ───────────────────────────────────────────────

class GradeScaleForm(forms.ModelForm):
    class Meta:
        model = GradeScale
        fields = ['name', 'grade_letter', 'min_percentage', 'max_percentage', 'grade_point', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Primary'}),
            'grade_letter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A, B+'}),
            'min_percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 80'}),
            'max_percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 100'}),
            'grade_point': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 4.0'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional'}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['exam', 'student', 'marks_obtained', 'grade_letter', 'grade_point', 'remarks']
        widgets = {
            'exam': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 85'}),
            'grade_letter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Auto-calculated'}),
            'grade_point': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Auto-calculated'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional remarks'}),
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['exam'].queryset = Exam.objects.filter(school=school)
            self.fields['student'].queryset = Student.objects.filter(school=school)


# ─── Fees Forms ──────────────────────────────────────────────────

class FeeCategoryForm(forms.ModelForm):
    class Meta:
        model = FeeCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Tuition, Transport'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
        }


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['name', 'fee_category', 'amount', 'frequency', 'due_day', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Monthly Tuition Fee'}),
            'fee_category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5000'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'due_day': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['fee_category'].queryset = FeeCategory.objects.filter(school=school)


class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['student', 'fee_structure', 'amount_paid', 'payment_date', 'payment_method', 'transaction_id', 'status', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'fee_structure': forms.Select(attrs={'class': 'form-control'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5000'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. TXN12345'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional remarks'}),
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['student'].queryset = Student.objects.filter(school=school)
            self.fields['fee_structure'].queryset = FeeStructure.objects.filter(school=school)


# ─── Attendance Forms ────────────────────────────────────────────

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'classroom', 'date', 'status', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'classroom': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional remarks'}),
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['student'].queryset = Student.objects.filter(school=school)
            self.fields['classroom'].queryset = Classroom.objects.filter(school=school)
