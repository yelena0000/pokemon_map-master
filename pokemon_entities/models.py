from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Покемон"""
    title = models.CharField(
        max_length=200,
        verbose_name='Название (рус)'
    )
    title_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Название (англ)'
    )
    title_jp = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Название (яп)'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to='pokemons',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='Из кого эволюционировал'
    )

    def __str__(self):
        return (
            f"{self.title},"
            f"{self.title_en},"
            f"{self.title_jp},"
            f"{self.description}"
        )


class PokemonEntity(models.Model):
    """Параметры покемона"""
    pokemon = models.ForeignKey(
        'Pokemon',
        on_delete=models.CASCADE,
        verbose_name='Покемон'
    )
    latitude = models.FloatField(
        verbose_name='Широта'
    )
    longitude = models.FloatField(
        verbose_name='Долгота'
    )
    appeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время появления'
    )
    disappeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время исчезновения'
    )
    level = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Уровень'
    )
    health = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Здоровье'
    )
    strength = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Атака'
    )
    defense = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Защита'
    )
    stamina = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Выносливость'
    )

    def __str__(self):
        return (
            f"{self.pokemon.title},"
            f"{self.latitude},"
            f"{self.longitude}),"
            f"{self.appeared_at},"
            f"{self.disappeared_at},"
            f"{self.level},"
            f"{self.health},"
            f"{self.strength},"
            f"{self.defense},"
            f"{self.stamina}"
        )
