# Generated by Django 3.2.18 on 2023-03-20 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('last_name',), 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]