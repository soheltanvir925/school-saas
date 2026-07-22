from django.urls import path
from . import views

app_name = 'schools'

urlpatterns = [
    path('teachers/', views.TeacherListView.as_view(), name='teacher_list'),
    path('teachers/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('teachers/add/', views.TeacherCreateView.as_view(), name='teacher_add'),
    path('teachers/<int:pk>/edit/', views.TeacherUpdateView.as_view(), name='teacher_edit'),
    path('teachers/<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='teacher_delete'),
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
    path('students/add/', views.StudentCreateView.as_view(), name='student_add'),
    path('streams/', views.StreamListView.as_view(), name='stream_list'),
    path('streams/add/', views.StreamCreateView.as_view(), name='stream_add'),
    path('streams/<int:pk>/edit/', views.StreamUpdateView.as_view(), name='stream_edit'),
    path('streams/<int:pk>/delete/', views.StreamDeleteView.as_view(), name='stream_delete'),
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/add/', views.SubjectCreateView.as_view(), name='subject_add'),
    path('subjects/<int:pk>/edit/', views.SubjectUpdateView.as_view(), name='subject_edit'),
    path('subjects/<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),
    path('classrooms/', views.ClassroomListView.as_view(), name='classroom_list'),
    path('classrooms/add/', views.ClassroomCreateView.as_view(), name='classroom_add'),
    path('classrooms/<int:pk>/edit/', views.ClassroomUpdateView.as_view(), name='classroom_edit'),
    path('classrooms/<int:pk>/delete/', views.ClassroomDeleteView.as_view(), name='classroom_delete'),

    # Exam Types
    path('exam-types/', views.ExamTypeListView.as_view(), name='examtype_list'),
    path('exam-types/add/', views.ExamTypeCreateView.as_view(), name='examtype_add'),
    path('exam-types/<int:pk>/edit/', views.ExamTypeUpdateView.as_view(), name='examtype_edit'),
    path('exam-types/<int:pk>/delete/', views.ExamTypeDeleteView.as_view(), name='examtype_delete'),

    # Exams
    path('exams/', views.ExamListView.as_view(), name='exam_list'),
    path('exams/add/', views.ExamCreateView.as_view(), name='exam_add'),
    path('exams/<int:pk>/edit/', views.ExamUpdateView.as_view(), name='exam_edit'),
    path('exams/<int:pk>/delete/', views.ExamDeleteView.as_view(), name='exam_delete'),

    # Grade Scales
    path('grade-scales/', views.GradeScaleListView.as_view(), name='gradescale_list'),
    path('grade-scales/add/', views.GradeScaleCreateView.as_view(), name='gradescale_add'),
    path('grade-scales/<int:pk>/edit/', views.GradeScaleUpdateView.as_view(), name='gradescale_edit'),
    path('grade-scales/<int:pk>/delete/', views.GradeScaleDeleteView.as_view(), name='gradescale_delete'),

    # Grades
    path('grades/', views.GradeListView.as_view(), name='grade_list'),
    path('grades/add/', views.GradeCreateView.as_view(), name='grade_add'),
    path('grades/<int:pk>/edit/', views.GradeUpdateView.as_view(), name='grade_edit'),
    path('grades/<int:pk>/delete/', views.GradeDeleteView.as_view(), name='grade_delete'),

    # Fee Categories
    path('fee-categories/', views.FeeCategoryListView.as_view(), name='feecategory_list'),
    path('fee-categories/add/', views.FeeCategoryCreateView.as_view(), name='feecategory_add'),
    path('fee-categories/<int:pk>/edit/', views.FeeCategoryUpdateView.as_view(), name='feecategory_edit'),
    path('fee-categories/<int:pk>/delete/', views.FeeCategoryDeleteView.as_view(), name='feecategory_delete'),

    # Fee Structures
    path('fee-structures/', views.FeeStructureListView.as_view(), name='feestructure_list'),
    path('fee-structures/add/', views.FeeStructureCreateView.as_view(), name='feestructure_add'),
    path('fee-structures/<int:pk>/edit/', views.FeeStructureUpdateView.as_view(), name='feestructure_edit'),
    path('fee-structures/<int:pk>/delete/', views.FeeStructureDeleteView.as_view(), name='feestructure_delete'),

    # Fee Payments
    path('fee-payments/', views.FeePaymentListView.as_view(), name='feepayment_list'),
    path('fee-payments/add/', views.FeePaymentCreateView.as_view(), name='feepayment_add'),
    path('fee-payments/<int:pk>/edit/', views.FeePaymentUpdateView.as_view(), name='feepayment_edit'),
    path('fee-payments/<int:pk>/delete/', views.FeePaymentDeleteView.as_view(), name='feepayment_delete'),
    path('fee-payments/student-dues/', views.StudentFeeDuesView.as_view(), name='student_fee_dues'),

    # Attendance
    path('attendance/', views.AttendanceListView.as_view(), name='attendance_list'),
    path('attendance/add/', views.AttendanceCreateView.as_view(), name='attendance_add'),
    path('attendance/<int:pk>/edit/', views.AttendanceUpdateView.as_view(), name='attendance_edit'),
    path('attendance/<int:pk>/delete/', views.AttendanceDeleteView.as_view(), name='attendance_delete'),
]
