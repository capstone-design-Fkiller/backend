# Generated by Django 4.2.1 on 2023-05-10 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Apply",
            fields=[("id", models.BigAutoField(primary_key=True, serialize=False)),],
        ),
        migrations.CreateModel(
            name="Priority1",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("question", models.CharField(max_length=100, unique=True)),
                ("answer", models.CharField(blank=True, max_length=100, null=True)),
                ("field_type", models.CharField(default="char", max_length=10)),
            ],
        ),
    ]