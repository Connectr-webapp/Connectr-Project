# Generated by Django 3.2.21 on 2023-11-21 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unreadmessage',
            name='conversation',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='messaging.conversation'),
        ),
    ]
