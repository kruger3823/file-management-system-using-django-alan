# Generated by Django 2.1.9 on 2022-11-05 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep_name', models.CharField(choices=[('mca', 'MCA'), ('eee', 'EEE'), ('cse', 'CSE'), ('ncc', 'NCC')], max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Department'),
        ),
    ]