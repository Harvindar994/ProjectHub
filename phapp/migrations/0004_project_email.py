# Generated by Django 3.2.4 on 2021-07-18 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phapp', '0003_remove_project_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='email',
            field=models.EmailField(default=None, max_length=254),
            preserve_default=False,
        ),
    ]
