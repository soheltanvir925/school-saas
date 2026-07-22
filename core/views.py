from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Q, F
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import SchoolRegistrationForm
from .models import School, SchoolEvent
from schools.models import Teacher, Student, Classroom, Subject, Stream, Exam, Grade, FeePayment, Attendance

class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_template_names(self):
        host = self.request.get_host().split(':')[0]
        parts = host.split('.')
        subdomain = parts[0] if len(parts) >= 2 else None
        is_subdomain = subdomain and subdomain not in ['localhost', '127', '0', 'www']
        if is_subdomain:
            return ['core/index_subdomain.html']
        return ['core/index.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        host = self.request.get_host().split(':')[0]
        parts = host.split('.')
        subdomain = parts[0] if len(parts) >= 2 else None
        is_subdomain = subdomain and subdomain not in ['localhost', '127', '0', 'www']
        if is_subdomain:
            try:
                context['school'] = School.objects.get(subdomain=subdomain)
            except School.DoesNotExist:
                pass
        return context

class RegisterSchoolView(CreateView):
    model = School
    form_class = SchoolRegistrationForm
    template_name = 'registration/register_school.html'
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        messages.success(self.request, "School registered successfully! You can now login as admin.")
        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        role = self.request.user.role
        if role == 'admin':
            return ['core/dashboard_admin.html']
        elif role == 'teacher':
            return ['core/dashboard_teacher.html']
        elif role == 'student':
            return ['core/dashboard_student.html']
        return ['core/dashboard_admin.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now().date()

        if user.role == 'admin':
            if user.school:
                s = user.school
                context['school'] = s
                context['is_school_admin'] = True

                students_qs = Student.objects.filter(school=s)
                teachers_qs = Teacher.objects.filter(school=s)

                context['total_teachers'] = teachers_qs.count()
                context['total_students'] = students_qs.count()
                context['total_classrooms'] = Classroom.objects.filter(school=s).count()
                context['total_subjects'] = Subject.objects.filter(school=s).count()
                context['total_streams'] = Stream.objects.filter(school=s).count()

                context['male_students'] = students_qs.filter(gender='male').count()
                context['female_students'] = students_qs.filter(gender='female').count()

                context['total_revenue'] = FeePayment.objects.filter(
                    school=s, status='paid'
                ).aggregate(t=Sum('amount_paid'))['t'] or 0

                context['pending_fees'] = FeePayment.objects.filter(
                    school=s, status='pending'
                ).count()

                context['today_attendance'] = Attendance.objects.filter(
                    school=s, date=today, status='present'
                ).count()
                context['today_absent'] = Attendance.objects.filter(
                    school=s, date=today, status='absent'
                ).count()

                context['upcoming_exams'] = Exam.objects.filter(
                    school=s, exam_date__gte=today, is_active=True
                ).order_by('exam_date')[:5]

                context['recent_payments'] = FeePayment.objects.filter(
                    school=s
                ).select_related('student', 'fee_structure').order_by('-payment_date')[:5]

                context['top_students'] = Grade.objects.filter(
                    exam__school=s
                ).select_related('student', 'exam').order_by('-marks_obtained')[:5]

                context['recent_events'] = SchoolEvent.objects.filter(
                    school=s, is_active=True, event_date__gte=today
                ).order_by('event_date')[:3]

                context['student_activity'] = Grade.objects.filter(
                    exam__school=s
                ).select_related('student', 'exam', 'exam__subject').order_by('-created_at')[:5]

            else:
                context['is_global_admin'] = True
                context['total_schools'] = School.objects.filter(is_active=True).count()
                context['total_teachers'] = Teacher.objects.all().count()
                context['total_students'] = Student.objects.all().count()
                context['schools_list'] = School.objects.filter(is_active=True).order_by('-created_at')

        elif user.role == 'teacher':
            s = user.school
            if not s:
                return context

            context['school'] = s

            teacher = Teacher.objects.filter(school=s, email=user.email).first()
            context['teacher_profile'] = teacher

            my_classrooms = Classroom.objects.filter(school=s)
            if teacher:
                my_classrooms = my_classrooms.filter(teacher=teacher)

            context['total_classes'] = my_classrooms.count()
            context['total_students'] = Student.objects.filter(
                school=s, classroom__in=my_classrooms
            ).count()
            context['total_subjects'] = Subject.objects.filter(
                school=s, classrooms__in=my_classrooms
            ).distinct().count()

            context['upcoming_exams'] = Exam.objects.filter(
                school=s, classroom__in=my_classrooms, exam_date__gte=today, is_active=True
            ).select_related('classroom', 'subject', 'exam_type').order_by('exam_date')[:5]

            context['recent_grades'] = Grade.objects.filter(
                exam__school=s, exam__classroom__in=my_classrooms
            ).select_related('student', 'exam', 'exam__subject').order_by('-created_at')[:5]

            context['today_attendance_count'] = Attendance.objects.filter(
                school=s, classroom__in=my_classrooms, date=today, status='present'
            ).count()

            context['total_exams_graded'] = Grade.objects.filter(
                exam__school=s, exam__classroom__in=my_classrooms
            ).values('exam').distinct().count()

        elif user.role == 'student':
            s = user.school
            if not s:
                return context

            context['school'] = s

            student = Student.objects.filter(school=s, email=user.email).first()
            context['student_profile'] = student

            if student:
                classroom = student.classroom

                context['total_subjects'] = classroom.subjects.count() if classroom else 0
                context['total_exams'] = Exam.objects.filter(
                    school=s, classroom=classroom, is_active=True
                ).count() if classroom else 0

                grades = Grade.objects.filter(student=student)
                context['tests_attended'] = grades.count()
                context['tests_passed'] = grades.filter(
                    marks_obtained__gte=F('exam__passing_marks')
                ).count()

                context['upcoming_exams'] = Exam.objects.filter(
                    school=s, classroom=classroom, exam_date__gte=today, is_active=True
                ).select_related('subject', 'exam_type').order_by('exam_date')[:5] if classroom else []

                context['recent_grades'] = grades.select_related(
                    'exam', 'exam__subject'
                ).order_by('-created_at')[:5]

                context['attendance_today'] = Attendance.objects.filter(
                    student=student, date=today
                ).first()
                context['attendance_count'] = Attendance.objects.filter(
                    student=student
                ).count()
                context['attendance_present'] = Attendance.objects.filter(
                    student=student, status='present'
                ).count()

        return context
