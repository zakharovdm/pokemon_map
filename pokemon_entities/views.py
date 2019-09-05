import folium

from django.shortcuts import render, get_object_or_404
from django.db import connection

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, level, health, attack, defence,
                stamina, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(f"""Уровень: {level}
                               Здоровье: {health}
                               Атака: {attack}
                               Защита: {defence}
                               Выносливость: {stamina}"""),
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entity = PokemonEntity.objects.select_related('pokemon').all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pok_entity in pokemon_entity:
        add_pokemon(
            folium_map, pok_entity.latitude, pok_entity.longitude,
            pok_entity.pokemon.title, pok_entity.level, pok_entity.health,
            pok_entity.attack, pok_entity.defence, pok_entity.stamina,
            request.build_absolute_uri(pok_entity.pokemon.photo.url))

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        if pokemon.photo:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': pokemon.photo.url,
                'title_ru': pokemon.title,
            })
        else:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title,
            })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    req_pokemon = PokemonEntity.objects.select_related('pokemon').filter(pokemon=pokemon)
    for pok_entity in req_pokemon:
        add_pokemon(
            folium_map, pok_entity.latitude, pok_entity.longitude,
            pok_entity.pokemon.title, pok_entity.level, pok_entity.health,
            pok_entity.attack, pok_entity.defence, pok_entity.stamina,
            request.build_absolute_uri(pok_entity.pokemon.photo.url))
    element_type = pokemon.element_type.all()
    elements = []
    strong_against = []
    for element in element_type:
        elements.append({
            'img': element.image.url,
            'title': element.title,
            'strong_against': strong_against
        })
        for strong_element in element.strong_against.all():
            strong_against.append(strong_element.title)
        strong_against = []
    pokemon_info = {
        'pokemon_id': pokemon.id,
        'img_url': pokemon.photo.url,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'element_type': elements
    }
    if pokemon.previous_evolution:
        previous_evolution = {
            **pokemon_info,
            'previous_evolution': {
                'title_ru': pokemon.previous_evolution.title,
                'pokemon_id': pokemon.previous_evolution.id,
                'img_url': pokemon.previous_evolution.photo.url},
        }
    else:
        previous_evolution = {}

    if pokemon.next_evolutions.exists():
        next_evolut = pokemon.next_evolutions.get()
        next_evolution = {
            **pokemon_info,
            'next_evolution': {
                'title_ru': next_evolut.title,
                'pokemon_id': next_evolut.id,
                'img_url': next_evolut.photo.url}
        }
    else:
        next_evolution = {}

    pokemon_on_page = {**previous_evolution, **next_evolution}
    return render(request, "pokemon.html",
                  context={'map': folium_map._repr_html_(),
                           'pokemon': pokemon_on_page})
