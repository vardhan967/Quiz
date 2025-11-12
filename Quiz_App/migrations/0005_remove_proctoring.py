from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz_App', '0004_examsession_proctorcapture'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProctorCapture',
        ),
        migrations.DeleteModel(
            name='ExamSession',
        ),
    ]
