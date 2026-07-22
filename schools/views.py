from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import F, Value, Sum, Q, DecimalField
from django.db.models.functions import Coalesce
from .models import Teacher, Student, Stream, Subject, Classroom, ExamType, Exam, GradeScale, Grade, FeeCategory, FeeStructure, FeePayment, Attendance
from .forms import TeacherForm, StudentForm, StreamForm, SubjectForm, ClassroomForm, ExamTypeForm, ExamForm, GradeScaleForm, GradeForm, FeeCategoryForm, FeeStructureForm, FeePaymentForm, AttendanceForm

class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = 'schools/teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        return Teacher.objects.filter(school=self.request.user.school)

class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'schools/teacher_detail.html'
    context_object_name = 'teacher'

    def get_queryset(self):
        return Teacher.objects.filter(school=self.request.user.school)


class TeacherCreateView(LoginRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'schools/teacher_form.html'
    success_url = reverse_lazy('schools:teacher_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        school = self.request.user.school
        if not school:
            messages.error(self.request, "Your account is not linked to a school. Please contact support.")
            return self.form_invalid(form)
            
        form.save(school=school)
        messages.success(self.request, "Teacher created successfully.")
        return redirect(self.success_url)

class TeacherUpdateView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'schools/teacher_form.html'

    def get_queryset(self):
        return Teacher.objects.filter(school=self.request.user.school)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['editing'] = True
        return ctx

    def get(self, request, *args, **kwargs):
        storage = messages.get_messages(request)
        storage.used = True
        self.object = self.get_object()
        teacher = self.object
        initial = {
            'employee_id': teacher.employee_id,
            'first_name': teacher.first_name,
            'last_name': teacher.last_name,
            'stream': teacher.stream_id,
            'gender': teacher.gender,
            'date_of_birth': teacher.date_of_birth,
            'phone': teacher.phone,
            'date_of_joining': teacher.date_of_joining,
            'qualification': teacher.qualification,
            'experience_years': teacher.experience_years,
            'username': teacher.username,
            'email': teacher.email,
            'address': teacher.address,
            'city': teacher.city,
            'state': teacher.state,
            'zip_code': teacher.zip_code,
            'country': teacher.country,
        }
        form = TeacherForm(initial=initial, school=request.user.school)
        return render(request, self.template_name, {'form': form, 'teacher': teacher, 'editing': True})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        school = request.user.school
        form = TeacherForm(request.POST, request.FILES, school=school)
        if form.is_valid():
            form.save(school=school, teacher=self.object)
            messages.success(request, "Teacher updated successfully.")
            return redirect('schools:teacher_list')
        return render(request, self.template_name, {'form': form, 'teacher': self.object, 'editing': True})


class TeacherDeleteView(LoginRequiredMixin, DeleteView):
    model = Teacher
    success_url = reverse_lazy('schools:teacher_list')

    def get_queryset(self):
        return Teacher.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        teacher = self.get_object()
        teacher.delete()
        messages.success(self.request, "Teacher deleted successfully.")
        return HttpResponseRedirect(self.success_url)


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'schools/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.filter(school=self.request.user.school).select_related('classroom')

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'schools/student_detail.html'
    context_object_name = 'student'

    def get_queryset(self):
        return Student.objects.filter(school=self.request.user.school).select_related('classroom')


class StudentUpdateView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'schools/student_form.html'

    def get_queryset(self):
        return Student.objects.filter(school=self.request.user.school)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['editing'] = True
        return ctx

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        student = self.object
        initial = {
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email,
            'roll_number': student.roll_number,
            'gender': student.gender,
            'date_of_birth': student.date_of_birth,
            'classroom': student.classroom_id,
            'religion': student.religion,
            'joining_date': student.joining_date,
            'phone': student.phone,
            'admission_number': student.admission_number,
            'section': student.section,
            'father_name': student.father_name,
            'father_occupation': student.father_occupation,
            'father_mobile': student.father_mobile,
            'father_email': student.father_email,
            'mother_name': student.mother_name,
            'mother_occupation': student.mother_occupation,
            'mother_mobile': student.mother_mobile,
            'mother_email': student.mother_email,
            'present_address': student.present_address,
            'permanent_address': student.permanent_address,
        }
        school = request.user.school
        form = StudentForm(initial=initial, school=school)
        return render(request, self.template_name, {'form': form, 'student': student, 'editing': True})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        school = request.user.school
        form = StudentForm(request.POST, request.FILES, school=school)
        if form.is_valid():
            form.save(school=school, student=self.object)
            messages.success(request, "Student updated successfully.")
            return redirect('schools:student_list')
        return render(request, self.template_name, {'form': form, 'student': self.object, 'editing': True})


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('schools:student_list')

    def get_queryset(self):
        return Student.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        student = self.get_object()
        student.delete()
        messages.success(self.request, "Student deleted successfully.")
        return HttpResponseRedirect(self.success_url)


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'schools/student_form.html'
    success_url = reverse_lazy('schools:student_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        school = self.request.user.school
        if not school:
            messages.error(self.request, "Your account is not linked to a school. Please contact support.")
            return self.form_invalid(form)

        form.save(school=school)
        messages.success(self.request, "Student registered successfully.")
        return redirect(self.success_url)


# --- Stream Views ---

class StreamListView(LoginRequiredMixin, ListView):
    model = Stream
    template_name = 'schools/stream_list.html'
    context_object_name = 'streams'

    def get_queryset(self):
        return Stream.objects.filter(school=self.request.user.school)


class StreamCreateView(LoginRequiredMixin, CreateView):
    model = Stream
    form_class = StreamForm
    template_name = 'schools/stream_form.html'
    success_url = reverse_lazy('schools:stream_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        messages.success(self.request, "Stream created successfully.")
        return super().form_valid(form)


class StreamUpdateView(LoginRequiredMixin, UpdateView):
    model = Stream
    form_class = StreamForm
    template_name = 'schools/stream_form.html'
    success_url = reverse_lazy('schools:stream_list')

    def get_queryset(self):
        return Stream.objects.filter(school=self.request.user.school)

    def form_valid(self, form):
        messages.success(self.request, "Stream updated successfully.")
        return super().form_valid(form)


class StreamDeleteView(LoginRequiredMixin, DeleteView):
    model = Stream
    success_url = reverse_lazy('schools:stream_list')

    def get_queryset(self):
        return Stream.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Stream deleted successfully.")
        return super().delete(request, *args, **kwargs)


# --- Subject Views ---

class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'schools/subject_list.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        return Subject.objects.filter(school=self.request.user.school)


class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'schools/subject_form.html'
    success_url = reverse_lazy('schools:subject_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        messages.success(self.request, "Subject created successfully.")
        return super().form_valid(form)


class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'schools/subject_form.html'
    success_url = reverse_lazy('schools:subject_list')

    def get_queryset(self):
        return Subject.objects.filter(school=self.request.user.school)

    def form_valid(self, form):
        messages.success(self.request, "Subject updated successfully.")
        return super().form_valid(form)


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy('schools:subject_list')

    def get_queryset(self):
        return Subject.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Subject deleted successfully.")
        return super().delete(request, *args, **kwargs)


# --- Classroom Views ---

class ClassroomListView(LoginRequiredMixin, ListView):
    model = Classroom
    template_name = 'schools/classroom_list.html'
    context_object_name = 'classrooms'

    def get_queryset(self):
        return Classroom.objects.filter(school=self.request.user.school).select_related('teacher')


class ClassroomCreateView(LoginRequiredMixin, CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'schools/classroom_form.html'
    success_url = reverse_lazy('schools:classroom_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        messages.success(self.request, "Classroom created successfully.")
        return super().form_valid(form)


class ClassroomUpdateView(LoginRequiredMixin, UpdateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'schools/classroom_form.html'
    success_url = reverse_lazy('schools:classroom_list')

    def get_queryset(self):
        return Classroom.objects.filter(school=self.request.user.school)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Classroom updated successfully.")
        return super().form_valid(form)


class ClassroomDeleteView(LoginRequiredMixin, DeleteView):
    model = Classroom
    success_url = reverse_lazy('schools:classroom_list')

    def get_queryset(self):
        return Classroom.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Classroom deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ─── ExamType Views ──────────────────────────────────────────────

class ExamTypeListView(LoginRequiredMixin, ListView):
    model = ExamType
    template_name = 'schools/examtype_list.html'
    context_object_name = 'examtypes'

    def get_queryset(self):
        return ExamType.objects.filter(school=self.request.user.school)


class ExamTypeCreateView(LoginRequiredMixin, CreateView):
    model = ExamType
    form_class = ExamTypeForm
    template_name = 'schools/examtype_form.html'
    success_url = reverse_lazy('schools:examtype_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        messages.success(self.request, "Exam type created successfully.")
        return super().form_valid(form)


class ExamTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = ExamType
    form_class = ExamTypeForm
    template_name = 'schools/examtype_form.html'
    success_url = reverse_lazy('schools:examtype_list')

    def get_queryset(self):
        return ExamType.objects.filter(school=self.request.user.school)

    def form_valid(self, form):
        messages.success(self.request, "Exam type updated successfully.")
        return super().form_valid(form)


class ExamTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = ExamType
    success_url = reverse_lazy('schools:examtype_list')

    def get_queryset(self):
        return ExamType.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Exam type deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ─── Exam Views ──────────────────────────────────────────────────

class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'schools/exam_list.html'
    context_object_name = 'exams'

    def get_queryset(self):
        return Exam.objects.filter(school=self.request.user.school).select_related('exam_type', 'classroom', 'subject')


class ExamCreateView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'schools/exam_form.html'
    success_url = reverse_lazy('schools:exam_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        messages.success(self.request, "Exam created successfully.")
        return super().form_valid(form)


class ExamUpdateView(LoginRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'schools/exam_form.html'
    success_url = reverse_lazy('schools:exam_list')

    def get_queryset(self):
        return Exam.objects.filter(school=self.request.user.school)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Exam updated successfully.")
        return super().form_valid(form)


class ExamDeleteView(LoginRequiredMixin, DeleteView):
    model = Exam
    success_url = reverse_lazy('schools:exam_list')

    def get_queryset(self):
        return Exam.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Exam deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ─── GradeScale Views ────────────────────────────────────────────

class GradeScaleListView(LoginRequiredMixin, ListView):
    model = GradeScale
    template_name = 'schools/gradescale_list.html'
    context_object_name = 'gradescales'

    def get_queryset(self):
        return GradeScale.objects.filter(school=self.request.user.school)


class GradeScaleCreateView(LoginRequiredMixin, CreateView):
    model = GradeScale
    form_class = GradeScaleForm
    template_name = 'schools/gradescale_form.html'
    success_url = reverse_lazy('schools:gradescale_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        messages.success(self.request, "Grade scale created successfully.")
        return super().form_valid(form)


class GradeScaleUpdateView(LoginRequiredMixin, UpdateView):
    model = GradeScale
    form_class = GradeScaleForm
    template_name = 'schools/gradescale_form.html'
    success_url = reverse_lazy('schools:gradescale_list')

    def get_queryset(self):
        return GradeScale.objects.filter(school=self.request.user.school)

    def form_valid(self, form):
        messages.success(self.request, "Grade scale updated successfully.")
        return super().form_valid(form)


class GradeScaleDeleteView(LoginRequiredMixin, DeleteView):
    model = GradeScale
    success_url = reverse_lazy('schools:gradescale_list')

    def get_queryset(self):
        return GradeScale.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Grade scale deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ─── Grade Views ─────────────────────────────────────────────────

class GradeListView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = 'schools/grade_list.html'
    context_object_name = 'grades'

    def get_queryset(self):
        return Grade.objects.filter(school=self.request.user.school).select_related('exam', 'student', 'graded_by')


class GradeCreateView(LoginRequiredMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'schools/grade_form.html'
    success_url = reverse_lazy('schools:grade_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        form.instance.graded_by = Teacher.objects.filter(school=self.request.user.school, email=self.request.user.email).first()
        messages.success(self.request, "Grade recorded successfully.")
        return super().form_valid(form)


class GradeUpdateView(LoginRequiredMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'schools/grade_form.html'
    success_url = reverse_lazy('schools:grade_list')

    def get_queryset(self):
        return Grade.objects.filter(school=self.request.user.school)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Grade updated successfully.")
        return super().form_valid(form)


class GradeDeleteView(LoginRequiredMixin, DeleteView):
    model = Grade
    success_url = reverse_lazy('schools:grade_list')

    def get_queryset(self):
        return Grade.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Grade deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ─── FeeCategory Views ───────────────────────────────────────────

class FeeCategoryListView(LoginRequiredMixin, ListView):
    model = FeeCategory
    template_name = 'schools/feecategory_list.html'
    context_object_name = 'feecategories'

    def get_queryset(self):
        return FeeCategory.objects.filter(school=self.request.user.school)


class FeeCategoryCreateView(LoginRequiredMixin, CreateView):
    model = FeeCategory
    form_class = FeeCategoryForm
    template_name = 'schools/feecategory_form.html'
    success_url = reverse_lazy('schools:feecategory_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        messages.success(self.request, "Fee category created successfully.")
        return super().form_valid(form)


class FeeCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = FeeCategory
    form_class = FeeCategoryForm
    template_name = 'schools/feecategory_form.html'
    success_url = reverse_lazy('schools:feecategory_list')

    def get_queryset(self):
        return FeeCategory.objects.filter(school=self.request.user.school)

    def form_valid(self, form):
        messages.success(self.request, "Fee category updated successfully.")
        return super().form_valid(form)


class FeeCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = FeeCategory
    success_url = reverse_lazy('schools:feecategory_list')

    def get_queryset(self):
        return FeeCategory.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Fee category deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ─── FeeStructure Views ──────────────────────────────────────────

class FeeStructureListView(LoginRequiredMixin, ListView):
    model = FeeStructure
    template_name = 'schools/feestructure_list.html'
    context_object_name = 'feestructures'

    def get_queryset(self):
        return FeeStructure.objects.filter(school=self.request.user.school).select_related('fee_category')


class FeeStructureCreateView(LoginRequiredMixin, CreateView):
    model = FeeStructure
    form_class = FeeStructureForm
    template_name = 'schools/feestructure_form.html'
    success_url = reverse_lazy('schools:feestructure_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        messages.success(self.request, "Fee structure created successfully.")
        return super().form_valid(form)


class FeeStructureUpdateView(LoginRequiredMixin, UpdateView):
    model = FeeStructure
    form_class = FeeStructureForm
    template_name = 'schools/feestructure_form.html'
    success_url = reverse_lazy('schools:feestructure_list')

    def get_queryset(self):
        return FeeStructure.objects.filter(school=self.request.user.school)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Fee structure updated successfully.")
        return super().form_valid(form)


class FeeStructureDeleteView(LoginRequiredMixin, DeleteView):
    model = FeeStructure
    success_url = reverse_lazy('schools:feestructure_list')

    def get_queryset(self):
        return FeeStructure.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Fee structure deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ─── FeePayment Views ────────────────────────────────────────────

class FeePaymentListView(LoginRequiredMixin, ListView):
    model = FeePayment
    template_name = 'schools/feepayment_list.html'
    context_object_name = 'feepayments'
    paginate_by = 50

    def get_queryset(self):
        qs = FeePayment.objects.filter(school=self.request.user.school).select_related('student', 'fee_structure')

        search = self.request.GET.get('search', '').strip()
        status = self.request.GET.get('status', '').strip()
        method = self.request.GET.get('method', '').strip()

        if search:
            qs = qs.filter(
                Q(student__first_name__icontains=search) |
                Q(student__last_name__icontains=search) |
                Q(student__roll_number__icontains=search) |
                Q(transaction_id__icontains=search)
            )
        if status:
            qs = qs.filter(status=status)
        if method:
            qs = qs.filter(payment_method=method)

        qs = qs.annotate(
            due_amount=Coalesce(
                F('fee_structure__amount') - F('amount_paid'),
                Value(Decimal('0.00')),
                output_field=DecimalField()
            )
        )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'search': self.request.GET.get('search', ''),
            'status_filter': self.request.GET.get('status', ''),
            'method_filter': self.request.GET.get('method', ''),
        })
        qs = FeePayment.objects.filter(school=self.request.user.school)
        ctx['total_collected'] = qs.filter(status='paid').aggregate(s=Sum('amount_paid'))['s'] or Decimal('0.00')
        ctx['total_due'] = qs.aggregate(
            s=Sum(Coalesce(F('fee_structure__amount'), Value(Decimal('0.00')))) - Sum('amount_paid')
        )['s'] or Decimal('0.00')
        ctx['payment_count'] = qs.count()
        return ctx


class FeePaymentCreateView(LoginRequiredMixin, CreateView):
    model = FeePayment
    form_class = FeePaymentForm
    template_name = 'schools/feepayment_form.html'
    success_url = reverse_lazy('schools:feepayment_list')

    def get_initial(self):
        initial = super().get_initial()
        school = self.request.user.school
        student_id = self.request.GET.get('student')
        fee_structure_id = self.request.GET.get('fee_structure')
        if student_id:
            try:
                student = Student.objects.get(pk=student_id, school=school)
                initial['student'] = student.pk
            except Student.DoesNotExist:
                pass
        if fee_structure_id:
            try:
                fs = FeeStructure.objects.get(pk=fee_structure_id, school=school)
                initial['fee_structure'] = fs.pk
                initial['amount_paid'] = fs.amount
            except FeeStructure.DoesNotExist:
                pass
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        messages.success(self.request, "Fee payment recorded successfully.")
        return super().form_valid(form)


class FeePaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = FeePayment
    form_class = FeePaymentForm
    template_name = 'schools/feepayment_form.html'
    success_url = reverse_lazy('schools:feepayment_list')

    def get_queryset(self):
        return FeePayment.objects.filter(school=self.request.user.school)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Fee payment updated successfully.")
        return super().form_valid(form)


class FeePaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = FeePayment
    success_url = reverse_lazy('schools:feepayment_list')

    def get_queryset(self):
        return FeePayment.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Fee payment deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ─── Student Fee Dues ────────────────────────────────────────────

class StudentFeeDuesView(LoginRequiredMixin, ListView):
    template_name = 'schools/student_fee_dues.html'
    context_object_name = 'students'

    def get_queryset(self):
        school = self.request.user.school
        qs = Student.objects.filter(school=school)
        search = self.request.GET.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(roll_number__icontains=search) |
                Q(admission_number__icontains=search)
            )
        return qs[:20]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search'] = self.request.GET.get('search', '')
        ctx['selected_student'] = None
        ctx['fee_details'] = []
        ctx['total_due'] = Decimal('0.00')
        ctx['total_paid'] = Decimal('0.00')
        ctx['overall_total'] = Decimal('0.00')

        student_id = self.request.GET.get('student_id', '').strip()
        if student_id:
            try:
                student = Student.objects.get(pk=student_id, school=self.request.user.school)
                ctx['selected_student'] = student
                fee_structures = FeeStructure.objects.filter(
                    school=self.request.user.school, is_active=True
                )
                details = []
                total_due = Decimal('0.00')
                total_paid = Decimal('0.00')
                for fs in fee_structures:
                    payments = FeePayment.objects.filter(student=student, fee_structure=fs)
                    paid_agg = payments.aggregate(s=Sum('amount_paid'))['s'] or Decimal('0.00')
                    due = max(fs.amount - paid_agg, Decimal('0.00'))
                    total_due += due
                    total_paid += paid_agg
                    if paid_agg >= fs.amount:
                        status = 'paid'
                    elif paid_agg > 0:
                        status = 'partial'
                    else:
                        status = 'unpaid'
                    details.append({
                        'fee_structure': fs,
                        'paid': paid_agg,
                        'due': due,
                        'status': status,
                    })
                ctx['fee_details'] = details
                ctx['total_due'] = total_due
                ctx['total_paid'] = total_paid
                ctx['overall_total'] = total_due + total_paid
            except Student.DoesNotExist:
                pass
        return ctx


# ─── Attendance Views ────────────────────────────────────────────

class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'schools/attendance_list.html'
    context_object_name = 'attendance_records'

    def get_queryset(self):
        return Attendance.objects.filter(school=self.request.user.school).select_related('student', 'classroom', 'marked_by')


class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'schools/attendance_form.html'
    success_url = reverse_lazy('schools:attendance_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.pop('instance', None)
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        form.instance.marked_by = Teacher.objects.filter(school=self.request.user.school, email=self.request.user.email).first()
        messages.success(self.request, "Attendance recorded successfully.")
        return super().form_valid(form)


class AttendanceUpdateView(LoginRequiredMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'schools/attendance_form.html'
    success_url = reverse_lazy('schools:attendance_list')

    def get_queryset(self):
        return Attendance.objects.filter(school=self.request.user.school)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school'] = self.request.user.school
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Attendance updated successfully.")
        return super().form_valid(form)


class AttendanceDeleteView(LoginRequiredMixin, DeleteView):
    model = Attendance
    success_url = reverse_lazy('schools:attendance_list')

    def get_queryset(self):
        return Attendance.objects.filter(school=self.request.user.school)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Attendance record deleted successfully.")
        return super().delete(request, *args, **kwargs)



