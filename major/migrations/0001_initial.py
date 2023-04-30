# Generated by Django 4.2 on 2023-04-30 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Major",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("apply_start_date", models.DateTimeField(blank=True, null=True)),
                ("apply_end_date", models.DateTimeField(blank=True, null=True)),
                (
                    "priority_first",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "priority_second",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "priority_third",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
            options={"db_table": "major",},
        ),
    ]
