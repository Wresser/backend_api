# Generated by Django 3.2.3 on 2021-05-23 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210523_1607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='petition',
            old_name='votes',
            new_name='voters',
        ),
    ]
