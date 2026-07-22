from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_school_about_description_school_established_year_and_more'),
        ('schools', '0008_examtype_exam_feecategory_feestructure_feepayment_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Department',
            new_name='Stream',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='department',
            new_name='stream',
        ),
        migrations.AlterModelOptions(
            name='stream',
            options={'verbose_name': 'Stream', 'verbose_name_plural': 'Streams'},
        ),
    ]
