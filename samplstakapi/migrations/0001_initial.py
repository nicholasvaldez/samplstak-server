# Generated by Django 4.2 on 2023-05-21 01:17

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
            name='Drumkit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='img')),
            ],
        ),
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
                ('image', models.ImageField(upload_to='img')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_url', models.FileField(default='wav/none/no-wav.wav', upload_to='wav')),
                ('file_name', models.CharField(max_length=100)),
                ('drumkit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='samplstakapi.drumkit')),
                ('genre', models.ManyToManyField(related_name='genre_samples', to='samplstakapi.genre')),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='samplstakapi.instrument')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producer_samples', to='samplstakapi.producer')),
            ],
        ),
        migrations.AddField(
            model_name='drumkit',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='genre_of_drumkit', to='samplstakapi.genre'),
        ),
        migrations.AddField(
            model_name='drumkit',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drumkit_producer', to='samplstakapi.producer'),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='samplstakapi.producer')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='saved_samples', to='samplstakapi.sample')),
            ],
        ),
    ]
