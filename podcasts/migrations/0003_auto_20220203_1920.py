# Generated by Django 3.2.5 on 2022-02-03 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0002_alter_episode_guid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='episode',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterField(
            model_name='episode',
            name='guid',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='episode',
            name='podcast_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='episode',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]