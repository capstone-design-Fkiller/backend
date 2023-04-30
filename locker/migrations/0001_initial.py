# Generated by Django 4.2 on 2023-04-30 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0001_initial"),
        ("major", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Locker",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("building_id", models.IntegerField()),
                ("is_share_registered", models.BooleanField(default=False)),
                ("start_date", models.DateTimeField(blank=True, null=True)),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                ("share_start_date", models.DateTimeField(blank=True, null=True)),
                ("share_end_date", models.DateTimeField(blank=True, null=True)),
                (
                    "major",
                    models.ForeignKey(
                        db_column="major",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="locker",
                        to="major.major",
                    ),
                ),
                (
                    "owned_id",
                    models.ForeignKey(
                        blank=True,
                        db_column="owned_id",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="owned_locker",
                        to="user.user",
                    ),
                ),
                (
                    "shared_id",
                    models.ForeignKey(
                        blank=True,
                        db_column="shared_id",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="shared_locker",
                        to="user.user",
                    ),
                ),
            ],
            options={"db_table": "locker",},
        ),
    ]
