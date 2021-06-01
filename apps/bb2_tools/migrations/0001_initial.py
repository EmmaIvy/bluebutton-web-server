# Generated by Django 2.2.22 on 2021-06-01 02:15

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bluebutton', '0005_auto_20200529_1906'),
        ('dot_ext', '0025_auto_20210601_0215'),
        ('oauth2_provider', '0006_auto_20171214_2232'),
        ('accounts', '0042_auto_20210601_0215'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessTokenStats',
            fields=[
            ],
            options={
                'verbose_name': 'Access token counts by apps',
                'verbose_name_plural': 'Access token counts by apps',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('oauth2_provider.accesstoken',),
        ),
        migrations.CreateModel(
            name='ApplicationStats',
            fields=[
            ],
            options={
                'verbose_name': 'Application statistics',
                'verbose_name_plural': 'Application statistics',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dot_ext.application',),
        ),
        migrations.CreateModel(
            name='ArchivedTokenStats',
            fields=[
            ],
            options={
                'verbose_name': 'Archived token counts by apps',
                'verbose_name_plural': 'Archived token counts by apps',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dot_ext.archivedtoken',),
        ),
        migrations.CreateModel(
            name='BeneficiaryDashboard',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('bluebutton.crosswalk',),
        ),
        migrations.CreateModel(
            name='DummyAdminObject',
            fields=[
            ],
            options={
                'verbose_name': 'Splunk dashboard',
                'verbose_name_plural': 'Splunk dashboards',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('oauth2_provider.accesstoken',),
        ),
        migrations.CreateModel(
            name='MyAccessTokenViewer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('oauth2_provider.accesstoken',),
        ),
        migrations.CreateModel(
            name='MyArchivedTokenViewer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('dot_ext.archivedtoken',),
        ),
        migrations.CreateModel(
            name='MyRefreshTokenViewer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('oauth2_provider.refreshtoken',),
        ),
        migrations.CreateModel(
            name='RefreshTokenStats',
            fields=[
            ],
            options={
                'verbose_name': 'Refresh token counts by apps',
                'verbose_name_plural': 'Refresh token counts by apps',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('oauth2_provider.refreshtoken',),
        ),
        migrations.CreateModel(
            name='UserStats',
            fields=[
            ],
            options={
                'verbose_name': 'User statistics',
                'verbose_name_plural': 'User statistics',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.userprofile',),
        ),
    ]
