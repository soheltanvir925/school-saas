import django.db.models.deletion
from django.db import migrations, models


def migrate_departments(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO schools_department (name, code, description, school_id)
            SELECT DISTINCT department_old, UPPER(LEFT(department_old, 20)), '', school_id
            FROM schools_teacher
            WHERE department_old IS NOT NULL AND department_old != ''
        """)
        cursor.execute("""
            UPDATE schools_teacher t
            SET department_id = d.id
            FROM schools_department d
            WHERE t.department_old = d.name AND t.school_id = d.school_id
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_school_about_description_school_established_year_and_more'),
        ('schools', '0006_teacher_city_teacher_country_teacher_date_of_birth_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='department',
            new_name='department_old',
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='core.school')),
            ],
            options={
                'unique_together': {('school', 'name')},
            },
        ),
        migrations.AddField(
            model_name='teacher',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teachers', to='schools.department'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='subjects',
            field=models.ManyToManyField(blank=True, related_name='classrooms', to='schools.subject'),
        ),
        migrations.RunPython(migrate_departments),
        migrations.RemoveField(
            model_name='teacher',
            name='department_old',
        ),
    ]
