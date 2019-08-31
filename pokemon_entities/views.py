import folium

from django.shortcuts import render, get_object_or_404

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
            pok_entity.pokemon.title,
            request.build_absolute_uri(pok_entity.pokemon.photo.url))

    pokemon_info = {
        'pokemon_id': pokemon.id,
        'img_url': pokemon.photo.url,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description
    }
    try:
        if pokemon.previous_evolution:
            pokemon_on_page = {
                **pokemon_info,
                'previous_evolution': {
                    'title_ru': pokemon.previous_evolution.title,
                    'pokemon_id': pokemon.previous_evolution.id,
                    'img_url': pokemon.previous_evolution.photo.url},
                'next_evolution': {
                    'title_ru': pokemon.next_evolutions.get().title,
                    'pokemon_id': pokemon.next_evolutions.get().id,
                    'img_url': pokemon.next_evolutions.get().photo.url}
            }

        else:
            pokemon_on_page = {
                **pokemon_info,
                'next_evolution': {
                    'title_ru': pokemon.next_evolutions.get().title,
                    'pokemon_id': pokemon.next_evolutions.get().id,
                    'img_url': pokemon.next_evolutions.get().photo.url}
            }
    except Pokemon.DoesNotExist:
            pokemon_on_page = {
                **pokemon_info,
                'previous_evolution': {
                    'title_ru': pokemon.previous_evolution.title,
                    'pokemon_id': pokemon.previous_evolution.id,
                    'img_url': pokemon.previous_evolution.photo.url}
            }

    return render(request, "pokemon.html",
                  context={'map': folium_map._repr_html_(),
                           'pokemon': pokemon_on_page})
