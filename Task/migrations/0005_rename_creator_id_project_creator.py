# Generated by Django 5.0.2 on 2024-02-27 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Task', '0004_remove_project_project_details_project_creator_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='creator_id',
            new_name='creator',
        ),
    ]
