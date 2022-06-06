# Generated by Django 2.2.18 on 2022-06-03 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_delete_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now=True)),
                ('isRead', models.BooleanField(default=False)),
                ('receiver', models.CharField(max_length=100)),
                ('sender', models.CharField(max_length=100)),
            ],
        ),
    ]