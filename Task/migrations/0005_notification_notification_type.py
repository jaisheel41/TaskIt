# Generated by Django 5.0.2 on 2024-03-02 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Task', '0004_remove_notification_read_remove_notification_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(default='general', max_length=100),
        ),
    ]