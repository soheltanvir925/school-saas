# Exams / Fees / Grades / Attendance — Implementation Plan

## Architecture

All four models live in the `schools` app, following the same tenant-isolation pattern as existing models:
- Each model has a `school = ForeignKey(School)` for multi-tenant isolation
- All CRUD views filter by `request.user.school`
- All admin registrations use `SchoolScopedModelAdmin`
- All templates follow the Preskool admin template pattern

---

## 1. Exams

### Models

**ExamType** — categorization of exams (Quiz, Midterm, Final, etc.)
- school, name, description

**Exam** — individual exam instance
- school, name, exam_type (FK ExamType), classroom (FK), subject (FK)
- exam_date, start_time, end_time
- total_marks, passing_marks
- description, is_active, created_at, updated_at

### URL Structure
- exams/ → list
- exams/add/ → create
- exams/<pk>/edit/ → update
- exams/<pk>/delete/ → delete

### Dependencies
- Classroom, Subject (existing)

---

## 2. Grading

### Models

**GradeScale** — defines grade boundaries per school
- school, name (e.g. "Primary", "Secondary")
- grade_letter (A, B, C, D, F)
- min_percentage, max_percentage, grade_point, description

**Grade** — individual student grade for an exam
- school, exam (FK), student (FK)
- marks_obtained, grade_letter, grade_point, remarks
- graded_by (FK Teacher), created_at, updated_at

### URL Structure
- grades/ → list
- grades/add/ → create
- grades/<pk>/edit/ → update
- grades/<pk>/delete/ → delete

### Dependencies
- Exam, Student, Teacher

---

## 3. Fees

### Models

**FeeCategory** — types of fees (Tuition, Transport, Library, etc.)
- school, name, description

**FeeStructure** — defines fee amounts
- school, name, fee_category (FK), amount, frequency (monthly/quarterly/yearly/one-time), due_day, description, is_active

**FeePayment** — records payments made
- school, student (FK), fee_structure (FK), amount_paid, payment_date
- payment_method (cash/check/bank/online), transaction_id
- status (paid/partial/pending/overdue), remarks, created_at, updated_at

### URL Structure
- fees/ → list
- fees/add/ → create
- fees/<pk>/edit/ → update
- fees/<pk>/delete/ → delete
- fee-categories/ → CRUD
- fee-structures/ → CRUD

### Dependencies
- Student

---

## 4. Attendance

### Models

**Attendance** — daily attendance record
- school, student (FK), classroom (FK), date
- status (present/absent/late/holiday)
- marked_by (FK Teacher), remarks, created_at, updated_at

### URL Structure
- attendance/ → list (filterable by date/classroom)
- attendance/add/ → create
- attendance/<pk>/edit/ → update
- attendance/<pk>/delete/ → delete

### Dependencies
- Student, Classroom, Teacher

---

## Implementation Order

1. Models → all 4 sets of models in `schools/models.py`
2. Admin → register all in `schools/admin.py`
3. Forms → create forms in `schools/forms.py`
4. Views → create CRUD views in `schools/views.py`
5. URLs → add urlpatterns in `schools/urls.py`
6. Templates → create list + form templates for each module
7. Sidebar → update `dashboard_admin.html`, `dashboard_teacher.html`, and list templates
8. Migrations → run `migrate_tenants` management command

## Template Pattern

Each module has two templates:
- `{model}_list.html` — datatable with action buttons (edit/delete), plus "Add" button
- `{model}_form.html` — form with all fields, submit + cancel buttons

Both extend the Preskool admin layout with header, sidebar, page-wrapper, and scripts.
