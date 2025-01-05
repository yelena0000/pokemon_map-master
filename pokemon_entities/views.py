import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, latitude, longitude, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [latitude, longitude],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    current_time = localtime()

    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in pokemon_entities:
        image_url = (
            request.build_absolute_uri(entity.pokemon.image.url)
            if entity.pokemon.image
            else DEFAULT_IMAGE_URL
        )
        add_pokemon(
            folium_map,
            entity.latitude,
            entity.longitude,
            image_url
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': (
                request.build_absolute_uri(pokemon.image.url)
                if pokemon.image
                else DEFAULT_IMAGE_URL
            ),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)
    for entity in pokemon_entities:
        image_url = (
            request.build_absolute_uri(pokemon.image.url)
            if pokemon.image
            else DEFAULT_IMAGE_URL
        )
        add_pokemon(
            folium_map,
            entity.latitude,
            entity.longitude,
            image_url
        )

    pokemon_data = {
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'img_url': (
            request.build_absolute_uri(pokemon.image.url)
            if pokemon.image
            else DEFAULT_IMAGE_URL
        ),
    }

    if pokemon.previous_evolution:
        pokemon_data['previous_evolution'] = {
            'title_ru': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': (
                request.build_absolute_uri(pokemon.previous_evolution.image.url)
                if pokemon.previous_evolution.image
                else DEFAULT_IMAGE_URL
            ),
        }
    next_evolution = pokemon.next_evolutions.first()

    if next_evolution:
        pokemon_data['next_evolution'] = {
            'title_ru': next_evolution.title,
            'pokemon_id': next_evolution.id,
            'img_url': (
                request.build_absolute_uri(next_evolution.image.url)
                if next_evolution.image
                else DEFAULT_IMAGE_URL
            ),
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data,
    })
