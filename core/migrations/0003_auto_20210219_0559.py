# Generated by Django 3.1.6 on 2021-02-19 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210218_0107'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('payload', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='saved_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
