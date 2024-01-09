# Generated by Django 4.2.7 on 2023-12-01 16:27

from django.db import migrations, models
import helpers.media_upload


class Migration(migrations.Migration):
    dependencies = [
        ("pizza", "0003_burger"),
    ]

    operations = [
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
                ("description", models.TextField()),
                (
                    "image",
                    models.ImageField(upload_to=helpers.media_upload.upload_restaurant),
                ),
            ],
        ),
    ]