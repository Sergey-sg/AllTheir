# Generated by Django 4.0.5 on 2022-06-07 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_news_category_alter_news_content_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interaction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewingNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.news')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'view',
                'verbose_name_plural': 'Views',
                'ordering': ['news', '-created'],
            },
        ),
    ]
