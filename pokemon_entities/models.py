from django.db import models


class PokemonElementType(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.title}"


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Имя покемона")

    title_en = models.CharField(max_length=200,
                                verbose_name="Имя покемона(английский)")

    title_jp = models.CharField(max_length=200,
                                verbose_name="Имя покемона(японский)")

    photo = models.ImageField(null=True, blank=True,
                              verbose_name="Изображение")

    description = models.TextField(verbose_name="Описание")

    element_type = models.ManyToManyField(PokemonElementType)

    previous_evolution = models.ForeignKey("self", on_delete=models.CASCADE,
                                           null=True, blank=True,
                                           related_name="previous_evolutions",
                                           verbose_name="Из кого эволюционировал")

    next_evolution = models.ForeignKey("self", on_delete=models.CASCADE,
                                       null=True, blank=True,
                                       related_name="next_evolutions",
                                       verbose_name="В кого эволюционирует")

    def __str__(self):
        return f"{self.title}"


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
                                verbose_name="Имя покемона")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(verbose_name="Появится")
    disappeared_at = models.DateTimeField(verbose_name="Исчезнет")
    level = models.IntegerField(null=True, blank=True, verbose_name="Уровень")
    health = models.IntegerField(null=True, blank=True,
                                 verbose_name="Здоровье")
    attack = models.IntegerField(null=True, blank=True, verbose_name="Атака")
    defence = models.IntegerField(null=True, blank=True, verbose_name="Защита")
    stamina = models.IntegerField(null=True, blank=True,
                                  verbose_name="Выносливость")

    def __str__(self):
        return f"{self.pokemon}"
