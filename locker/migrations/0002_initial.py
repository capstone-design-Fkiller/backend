# Generated by Django 4.2.1 on 2023-05-10 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("locker", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="locker",
            name="owned_id",
            field=models.ForeignKey(
                blank=True,
                db_column="owned_id",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="owned_locker",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="locker",
            name="shared_id",
            field=models.ForeignKey(
                blank=True,
                db_column="shared_id",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="shared_locker",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]