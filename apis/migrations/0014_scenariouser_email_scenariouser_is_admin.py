# Generated by Django 4.1.5 on 2023-02-05 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0013_rename_email_scenariouser_user_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenariouser',
            name='email',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='scenariouser',
            name='is_admin',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
