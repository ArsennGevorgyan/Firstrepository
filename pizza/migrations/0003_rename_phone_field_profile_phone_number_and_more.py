# Generated by Django 4.2.7 on 2024-01-03 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0002_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='phone_field',
            new_name='phone_number',
        ),
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('client', 'Client'), ('business', 'Business')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
