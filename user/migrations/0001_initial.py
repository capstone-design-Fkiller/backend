# Generated by Django 4.2 on 2023-04-17 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('major', models.IntegerField(default=0)),
                ('penalty', models.BooleanField(default=False)),
                ('penalty_start_date', models.DateTimeField(blank=True, null=True)),
                ('penalty_end_date', models.DateTimeField(blank=True, null=True)),
                ('id_card_img', models.TextField(default='')),
                ('is_valid', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]