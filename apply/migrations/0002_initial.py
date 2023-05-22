# Generated by Django 4.2.1 on 2023-05-10 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("apply", "0001_initial"),
        ("locker", "0001_initial"),
        ("major", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="apply",
            name="building_id",
            field=models.ForeignKey(
                db_column="building_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="apply",
                to="locker.building",
            ),
        ),
        migrations.AddField(
            model_name="apply",
            name="major",
            field=models.ForeignKey(
                db_column="major",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="apply",
                to="major.major",
            ),
        ),
        migrations.AddField(
            model_name="apply",
            name="priority_1",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="apply_1",
                to="apply.priority1",
            ),
        ),
    ]
