# Generated by Django 5.0.6 on 2024-07-13 17:46

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновление')),
                ('phone', models.CharField(help_text='Напишите свой номер', max_length=25, unique=True, verbose_name='Номер телефона')),
                ('token', models.CharField(default=uuid.uuid4, max_length=255, unique=True, verbose_name='Тикер для пользователя')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
    ]
