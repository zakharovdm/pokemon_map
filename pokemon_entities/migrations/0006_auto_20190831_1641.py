# Generated by Django 2.2.3 on 2019-08-31 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0005_auto_20190831_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonelementtype',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='element_type',
            field=models.ManyToManyField(blank=True, to='pokemon_entities.PokemonElementType', verbose_name='Стихия покемона'),
        ),
        migrations.AlterField(
            model_name='pokemonelementtype',
            name='title',
            field=models.CharField(max_length=30, verbose_name='Стихия покемона'),
        ),
    ]
