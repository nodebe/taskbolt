# Generated by Django 4.1.7 on 2023-04-03 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_otp_alter_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otp',
            old_name='date_of_creation',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default='da079ab03db04036b7f3d82611c1d10e', max_length=36, primary_key=True, serialize=False),
        ),
    ]
