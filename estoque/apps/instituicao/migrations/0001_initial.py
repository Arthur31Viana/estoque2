# Generated by Django 5.0.6 on 2024-09-09 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instituicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instituicao', models.CharField(max_length=100, verbose_name='Instituição')),
                ('denominacao', models.CharField(blank=True, max_length=100, null=True, verbose_name='Denominação')),
                ('inep', models.IntegerField(unique=True, verbose_name='INEP')),
                ('diretora', models.CharField(max_length=100, verbose_name='Diretor(a)')),
                ('telefone', models.CharField(max_length=15, verbose_name='Telefone')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
            ],
            options={
                'verbose_name': 'Instituição',
                'verbose_name_plural': 'Instituições',
                'ordering': ['instituicao'],
            },
        ),
    ]
