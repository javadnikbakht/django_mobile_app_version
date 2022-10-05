# Generated by Django 4.1.2 on 2022-10-05 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MobileAppVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=100)),
                ('platform_type', models.CharField(choices=[('ANDROID', 'android'), ('IOS', 'ios'), ('PWA', 'pwa')], max_length=10)),
                ('release_notes', models.TextField(blank=True)),
                ('link', models.URLField(max_length=255)),
                ('link_32', models.URLField(blank=True, max_length=255, null=True)),
                ('forcing_update', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('manifest', models.URLField(blank=True, max_length=255, null=True)),
                ('show_update', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Mobile App Version',
                'verbose_name_plural': 'Mobile App Version',
            },
        ),
    ]