# Generated by Django 2.2.6 on 2019-10-30 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0003_user_looking_for_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='cohort',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
