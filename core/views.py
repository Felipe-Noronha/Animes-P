from django.shortcuts import render, redirect
import requests
from googletrans import Translator
from django.http import HttpResponse, HttpResponseServerError
from django.template import loader, TemplateDoesNotExist
from .models import Anime
from .forms import AnimeSearchForm
from .utils import get_top_animes


def random_page(request):
    try:
        api_url = "https://api.jikan.moe/v4/random/anime"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()

            if data and 'data' in data and 'title' in data['data']:
                translator = Translator()
                raw_synopsis = data['data'].get('synopsis', '')
                
                # Limita a sinopse a 300 caracteres
                max_synopsis_length = 300
                limited_synopsis = raw_synopsis[:max_synopsis_length] + ('...' if len(raw_synopsis) > max_synopsis_length else '')

                translated_synopsis = translator.translate(limited_synopsis, dest='pt').text

                anime, created = Anime.objects.get_or_create(
                    title=data['data']['title'],
                    defaults={'synopsis': translated_synopsis, 'genre': ', '.join(genre['name'] for genre in data['data'].get('genres', [])),
                              'trailer_url': data['data'].get('trailer', {}).get('embed_url', '')}
                )

                animes = Anime.objects.all()

                return render(request, 'core/random_page.html', {'animes': animes, 'image_info': data['data'].get('images', {}),
                                                                'title': data['data'].get('title', ''),
                                                                'synopsis': translated_synopsis,
                                                                'trailer_embed_url': data['data'].get('trailer', {}).get('embed_url', '')})
            else:
                return render(request, 'core/error.html', {'error_message': 'Formato de dados inválido da API'})
        else:
            return render(request, 'core/error.html', {'error_message': 'Falha ao obter dados da API'})
    except Exception as e:
        # Se ocorrer algum erro durante a execução do código
        try:
            # Tenta carregar o template de erro
            error_template = loader.get_template('core/error.html')
            # Se o template existir, renderiza com a mensagem de erro
            return HttpResponseServerError(error_template.render({'error_message': str(e)}))
        except TemplateDoesNotExist:
            # Se o template de erro não existir, fornece uma resposta simples com a mensagem de erro
            return HttpResponseServerError(f"Erro: {str(e)}")


def home(request):
    # Obtém os principais animes usando a função get_top_animes
    top_animes = get_top_animes()

    # Verifique se a chamada à API foi bem-sucedida
    if top_animes and 'data' in top_animes:
        return render(request, 'core/home.html', {'top_animes': top_animes['data']})
    else:
        # Trate o erro de chamada à API de acordo
        return render(request, 'core/error.html', {'error_message': 'Erro ao obter os principais animes'})




def search_anime(request):
    query = request.GET.get('query', '')
    sfw = request.GET.get('sfw', 'true')  # Valor padrão 'true' se não estiver presente
    unapproved = request.GET.get('unapproved', 'false')  # Valor padrão 'false' se não estiver presente

    # Construa a URL da API com os parâmetros da consulta
    api_url = f"https://api.jikan.moe/v4/anime?q={query}&sfw={sfw}&unapproved={unapproved}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return render(request, 'core/search_results.html', {'animes': data.get('data', [])})
        else:
            return render(request, 'core/error.html', {'error_message': 'Falha ao obter dados da API'})
    except Exception as e:
        return render(request, 'core/error.html', {'error_message': str(e)})
    
