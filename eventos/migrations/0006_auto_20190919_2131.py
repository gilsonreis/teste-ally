# Generated by Django 2.2.4 on 2019-09-20 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0005_auto_20190917_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='quantidade_lugares',
            field=models.PositiveIntegerField(default=100, verbose_name='Quantidade máxima'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingresso',
            name='codigo',
            field=models.CharField(blank=True, help_text='Máximo de 16 caracteres. Deixe em branco para gerar automáticamente.', max_length=16, null=True, verbose_name='Codigo do Ingresso'),
        ),
    ]