import requests
import time

class RequestsAnimeMain:
    def __init__(self, x_token):
        self.headers = {
            "X-Application": x_token,
            "Accept": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def request_anime_ids(self, year, status, skip, skip_limit, retrays=3):

        for i in range(retrays):
            try:
                response = self.session.get(
                    f'https://api.yani.tv/anime/', 
                    params={'limit': skip_limit,
                            'offset': skip,
                            'status': status,
                            'from_year': year,
                            'to_year': year
                            },
                    timeout=10 
                )

                if response.status_code == 200:
                    data = response.json()
                    anime_ids = data.get('response', {})
                    return anime_ids
                
            except Exception as exc:
                print(f'Ошибка: {exc}')
                time.sleep(10 * (i + 1))
        
        return None

    def request_anime_data(self, anime_id, retrays=3):

        for i in range(retrays):
            try:
                response = self.session.get(
                    f'https://api.yani.tv/anime/{anime_id}', 
                    params={'limit': 1, 'offset': 0},
                    timeout=10 
                )

                if response.status_code == 200:
                    data = response.json()
                    main_inf = data.get('response', {})
                    return main_inf
                
            except Exception as exc:
                print(f'Ошибка: anime_id {anime_id}: {exc}')
                time.sleep(10 * (i + 1))
        
        return None
    
    def request_anime_rates_distrb(self, anime_id, retrays=3):
        for i in range(retrays):
            try:
                response = self.session.get(
                    f'https://api.yani.tv/anime/{anime_id}/rates', 
                    params={'limit': 1, 'offset': 0},
                    timeout=10 
                )

                if response.status_code == 200:
                    data = response.json()
                    anime_rates_distrb = data.get('response', {})
                    return anime_rates_distrb
                
            except Exception as exc:
                print(f'Ошибка: anime_id {anime_id}: {exc}')
                time.sleep(10 * (i + 1))
        
        return None

    def request_reccomendation(self, anime_id, retrays=3):
        for i in range(retrays):
            try:
                response = self.session.get(
                    f'https://api.yani.tv/anime/{anime_id}/recommendations', 
                    params={'limit': 20, 'offset': 0},
                    timeout=10 
                )

                if response.status_code == 200:
                    data = response.json()
                    recomends = data.get('response', {})
                    return recomends
                
            except Exception as exc:
                print(f'Ошибка: anime_id {anime_id}: {exc}')
                time.sleep(10 * (i + 1))
        
        return None
    
    def request_vidos_inf(self, anime_id, retrays=3):
        for i in range(retrays):
            try:
                response = self.session.get(
                    f'https://api.yani.tv/anime/{anime_id}/videos', 
                    params={'limit': 1, 'offset': 0},
                    timeout=10 
                )

                if response.status_code == 200:
                    data = response.json()
                    vids_info = data.get('response', {})
                    return vids_info
                
            except Exception as exc:
                print(f'Ошибка: anime_id {anime_id}: {exc}')
                time.sleep(10 * (i + 1))
        
        return None
    
    def request_comments_inf(self, anime_id, skip, skip_step, retrays=3):
        for i in range(retrays):
            try:
                response = self.session.get(
                    f'https://api.yani.tv/comments/anime/{anime_id}', 
                    params={'skip': skip,
                            'sort': 'old',
                            'limit': skip_step},
                    timeout=10 
                )

                if response.status_code == 200:
                    data = response.json()
                    comments = data.get('response', {}).get('comments', [])
                    return comments
                
            except Exception as exc:
                print(f'Ошибка: anime_id {anime_id}: {exc}')
                time.sleep(10 * (i + 1))
        
        return None


    def request_user_lists(self, anime_id, retrays=3):
            for i in range(retrays):
                try:
                    response = self.session.get(
                        f'https://api.yani.tv/anime/{anime_id}/lists', 
                        params={'limit': 1, 'offset': 0},
                        timeout=10 
                    )
    
                    if response.status_code == 200:
                        data = response.json()
                        lists = data.get('response', {})
                        return lists
                    
                except Exception as exc:
                    print(f'Ошибка: anime_id {anime_id}: {exc}')
                    time.sleep(10 * (i + 1))
            
            return None