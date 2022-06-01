# Generated by Django 4.0.5 on 2022-06-01 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ['dd_order'], 'verbose_name': 'Menu item', 'verbose_name_plural': 'Menu items'},
        ),
        migrations.AddField(
            model_name='menu',
            name='title_en',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='menu',
            name='title_ru',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='menu',
            name='title_uk',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='title'),
        ),
    ]