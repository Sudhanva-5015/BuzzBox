# Generated by Django 5.0.6 on 2024-08-02 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BuzzBox', '0002_alter_profile_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(default='blank_profile _picture.png', upload_to='profile_images'),
        ),
    ]
