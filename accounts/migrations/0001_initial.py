# Generated by Django 4.2 on 2023-05-04 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("major", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Accounts",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "id",
                    models.CharField(
                        max_length=50, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("name", models.CharField(default="", max_length=20)),
                ("penalty", models.BooleanField(default=False)),
                ("penalty_start_date", models.DateTimeField(blank=True, null=True)),
                ("penalty_end_date", models.DateTimeField(blank=True, null=True)),
                ("id_card_img", models.TextField(default="")),
                ("is_valid", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "major",
                    models.ForeignKey(
                        blank=True,
                        db_column="major",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="user",
                        to="major.major",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"db_table": "accounts",},
        ),
    ]
