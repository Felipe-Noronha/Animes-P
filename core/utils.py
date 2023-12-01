# Em sua views.py ou em um novo arquivo (por exemplo, utils.py)
import requests

def get_top_animes():
    api_url = "https://api.jikan.moe/v4/top/anime"
    params = {
        "type": "tv",
        "filter": "bypopularity",
        "rating": "pg13",
        "page": 1,
        "limit": 10
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        print("Dados obtidos com sucesso:", data)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erro na solicitação para obter os principais animes: {e}")
        return None
