# Generated by Django 5.0 on 2023-12-21 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_signup', '0006_remove_imagemodel_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagemodel',
            old_name='image',
            new_name='image_file',
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='title',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
