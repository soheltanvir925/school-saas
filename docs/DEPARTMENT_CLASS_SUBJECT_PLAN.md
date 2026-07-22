# Department / Class / Subject Implementation Plan

## Current State

| Feature | Current State | Problem |
|---------|--------------|---------|
| Department | CharField on Teacher (free text) | No dedicated model, no management UI |
| Class/Classroom | Has name, capacity, teacher | Has no subjects assigned |
| Subject | Standalone model with name, code | Not linked to any classroom |

## Step 1 — Create Department Model

```python
class Department(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    head = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='head_of_department')

    class Meta:
        unique_together = ('school', 'name')
```

- Convert Teacher.department from CharField to ForeignKey(Department)
- Department CRUD views + URLs + templates
- Register in admin

## Step 2 — Link Subjects to Classrooms (M2M)

Add to Classroom model:
```python
subjects = models.ManyToManyField(Subject, related_name='classrooms', blank=True)
```

## Step 3 — CRUD Views

### Departments
| URL | View | Purpose |
|-----|------|---------|
| departments/ | DepartmentListView | List all departments |
| departments/add/ | DepartmentCreateView | Add new department |
| departments/<pk>/edit/ | DepartmentUpdateView | Edit department |
| departments/<pk>/delete/ | DepartmentDeleteView | Delete department |

### Subjects
| URL | View | Purpose |
|-----|------|---------|
| subjects/ | SubjectListView | List subjects |
| subjects/add/ | SubjectCreateView | Add new subject |
| subjects/<pk>/edit/ | SubjectUpdateView | Edit subject |
| subjects/<pk>/delete/ | SubjectDeleteView | Delete subject |

### Classrooms (update existing)
| URL | View | Update |
|-----|------|--------|
| classrooms/ | ClassroomListView | Add subject multi-select |
| classrooms/add/ | ClassroomCreateView | Add subject multi-select |
| classrooms/<pk>/edit/ | ClassroomUpdateView | Add subject multi-select |

## Step 4 — Update Forms

- TeacherForm → department becomes a dropdown of Department objects
- TeacherForm.save() → assign department FK
- ClassroomForm → add MultiSelect for subjects
- StudentForm → no change needed

## Step 5 — Update Templates

- teacher_form.html → department dropdown
- teacher_list.html → show department name
- New: department_list.html, department_form.html
- New: subject_list.html, subject_form.html
- classroom_form.html → multi-select subjects
