# Generated by Django 3.2.17 on 2023-02-11 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_blatt_kurs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kursleiter',
            name='kurs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kursleiter', to='core.kurs'),
        ),
        migrations.AlterField(
            model_name='kursleiterprofile',
            name='kurs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kursleiterprofile', to='core.kurs'),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='kurs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutor', to='core.kurs'),
        ),
        migrations.AlterField(
            model_name='tutorprofile',
            name='kurs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutorprofile', to='core.kurs'),
        ),
    ]
