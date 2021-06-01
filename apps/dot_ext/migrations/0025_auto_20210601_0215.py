# Generated by Django 2.2.22 on 2021-06-01 02:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dot_ext', '0024_auto_20210324_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='client_uri',
            field=models.URLField(blank=True, default='', help_text='This is typically a home/download website for the application. For example, https://www.example.org or http://www.example.org .', max_length=512, null=True, verbose_name='Client URI'),
        ),
        migrations.AlterField(
            model_name='application',
            name='description',
            field=models.TextField(blank=True, default='', help_text='This is plain-text up to 1000 characters in length.', null=True, verbose_name='Application Description'),
        ),
        migrations.AlterField(
            model_name='application',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='application',
            name='redirect_uris',
            field=models.TextField(blank=True, help_text='Multiple redirect URIs can be separated by a space or on a separate line. Read more about implementing redirect URIs in our documentation.'),
        ),
        migrations.AlterField(
            model_name='application',
            name='scope',
            field=models.ManyToManyField(to='capabilities.ProtectedCapability'),
        ),
        migrations.AlterField(
            model_name='application',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dot_ext_application', to=settings.AUTH_USER_MODEL),
        ),
    ]
