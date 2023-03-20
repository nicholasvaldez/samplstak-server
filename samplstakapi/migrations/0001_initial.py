# Generated by Django 4.1.7 on 2023-03-20 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_url', models.FileField(default='wav/none/no-wav.wav', upload_to='wav')),
                ('file_name', models.CharField(max_length=100)),
                ('genre', models.ManyToManyField(related_name='genre_samples', to='samplstakapi.genre')),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='samplstakapi.instrument')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producer_samples', to='samplstakapi.producer')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='samplstakapi.producer')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_samples', to='samplstakapi.sample')),
            ],
        ),
    ]
