import requests
import cloudscraper
from bs4 import BeautifulSoup
import time
from datetime import datetime
import csv

import psycopg2

############################
# вариант сохранения данных в csv файлы

class CsvFuncs:
    def create_file_anime_2():
        '''
        создает (перезаписывает) пустой файл anime_ids
        '''

        with open("anime_ids.csv", "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "anime_id",
                "title",
                "anime_url",
                "views",
                'type',
                'rating_avg',
            ])


    def collect_anime_ids():
        '''
        Заполнение файла anime_ids.csv
        '''

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
            }

        anime_counter = 0
        page = 1

        scraper = cloudscraper.create_scraper()

        while True:

            url = f"https://old.yummyani.me/catalog?page={page}"

            try:
                response = scraper.get(
                    url,
                    timeout=30
                )

            except Exception as e:
                print("Ошибка:", e)
                time.sleep(30)
                continue

            if response.status_code != 200:
                print("Ошибка:", response.status_code, response.text)
                break

            soup = BeautifulSoup(response.text, "html.parser")

            page_anime_list = soup.select(".anime-column")


            if not page_anime_list:
                print("Больше аниме нет.")
                break

            with open("anime_ids.csv", "a", newline="", encoding="utf-8") as file:

                writer = csv.writer(file)

                for anime in page_anime_list:
                    anime_id = anime.get('data-anime-id')
                    title = anime.select('.anime-title')[0].text
                    anime_url = anime.select('.anime-title')[0].get('href')[14:]
                    views = anime.select_one(".views-count").get_text(strip=True)
                    anime_type = anime.select_one(".anime-column-info > div").get_text(strip=True)
                    rating = anime.select_one(".main-rating").get_text(strip=True)

                    writer.writerow([anime_id, title, anime_url, views, anime_type, rating])
                    anime_counter += 1

            time.sleep(2)

            page += 1

        print(f'собрано {anime_counter} аниме')


    def create_anime_main():
        '''
        создает (перезаписывает) пустой файл main.csv
        '''
        with open("files/main.csv", "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                'anime_id',
                'title',
                'description',
                'duration',
                'anime_url',
                'year',
                'season',
                'views',
                'anime_status_ru',
                'type_ru',
                'rating_place_over_all',
                'rating_place_over_category', 
                'other_anime_names',
                'creators',
                'creadors_ids',
                'studios',
                'studios_id',
                'original',
                'episodes_count',
                'comments_count',
                'lists_count'
            ])

    def create_main_ratings():
        with open("files/main_ratings.csv", "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                'anime_id',
                'rating_avg',
                'rating_counts',
                'kp_rating', 
                'shikimori_rating',
                'myanimelist_rating',
                'worldart_rating'
            ])


    def create_main_genres():
        with open("files/main_genres.csv", "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                'anime_id',
                'title_ru',
                'title_en',
                'genre_id',
                'genre_url'
            ])


    def create_min_ages():
        with open("files/min_ages.csv", "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                'anime_id',
                'age_ru',
                'age_en',
                'age_id'
            ])


    def create_other_ids():
        with open("files/other_ids.csv", "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                'ya_anime_id',
                'myanimelist_id',
                'shikimori_id'
            ])


    def create_viewing_orders():
        with open("files/viewing_orders.csv", "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                'anime_id_1',
                'anime_id_2',
                'anime_title_2',
                'anime_url_2', 
                'anime_2_status_ru',
                'anime_2_type_ru',
                'anime_2_year',
                'anime_2_rating'
            ])

class RequestsAnimeMain:

    def __init__(self, x_token, s_token):
        self.headers = {
            "X-Application": x_token,
            "Authorization": f"Bearer {s_token}",
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



############################
# вариант подгрузки в бд

class PostgresDB:
    def __init__(self, host, db, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=db,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        self.tables = [
            'anime_ids',
            'anime_main',
            'ratings',
            'genres',
            'min_ages',
            'other_ids',
            'viewing_orders',
            'creators',
            'studios',
            'anime_other_titles',
            'ratings_distributions',
            'recommendations',
            'videos',
            'comments'
        ]


    def create_anime_ids_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE anime_ids (
            anime_id BIGINT PRIMARY KEY,
            title TEXT,
            anime_url TEXT,
            views INTEGER,
            type TEXT,
            rating_avg NUMERIC,
            year INTEGER
        );
        ''')
        self.cursor.connection.commit()


    def create_anime_main_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE anime_main (
            anime_id BIGINT PRIMARY KEY,
            title TEXT,
            description TEXT,
            duration BIGINT,
            anime_url TEXT,
            year INTEGER,
            season INTEGER,
            views INTEGER,
            status_ru TEXT,
            type_ru TEXT,
            rating_all INTEGER,
            rating_category INTEGER,
            original_source TEXT,
            episodes_count INTEGER,
            comments_count INTEGER,
            lists_count INTEGER
        );
        ''')
        self.cursor.connection.commit()
        

    def create_anime_ratings_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE ratings (
            anime_id BIGINT PRIMARY KEY,
            y_rating_avg NUMERIC,
            count INTEGER,
            kp_rating NUMERIC,
            shikimori_rating NUMERIC,
            myanimelist_rating NUMERIC,
            worldart_rating NUMERIC
        );
        ''')
        self.cursor.connection.commit()

    def create_anime_genres_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE genres (
            anime_id BIGINT,
            genre_id BIGINT,
            title_ru TEXT,
            title_en TEXT,
            url TEXT,
            PRIMARY KEY (anime_id, genre_id)
        );
        ''')
        self.cursor.connection.commit()

    def create_anime_min_ages_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE min_ages (
            anime_id BIGINT,
            age_id BIGINT,
            age_ru TEXT,
            age_en TEXT,
            PRIMARY KEY (anime_id, age_id)
        );
        ''')
        self.cursor.connection.commit()

    def create_anime_other_ids_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE other_ids (
            anime_id BIGINT PRIMARY KEY,
            myanimelist_id BIGINT,
            shikimori_id BIGINT
        );
        ''')
        self.cursor.connection.commit()

    def create_anime_viewing_orders_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE viewing_orders (
            anime_id BIGINT,
            related_anime_id BIGINT,
            title TEXT,
            url TEXT,
            status_ru TEXT,
            type_ru TEXT,
            year INTEGER,
            rating NUMERIC,
            PRIMARY KEY (anime_id, related_anime_id)
        );
        ''')
        self.cursor.connection.commit()

    def create_anime_creators_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE creators (
            anime_id BIGINT,
            creator_ids BIGINT,
            creator TEXT,
            PRIMARY KEY (anime_id, creator_ids)
        );
        ''')
        self.cursor.connection.commit()

    def create_anime_studios_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE studios (
            anime_id BIGINT,
            studio_id BIGINT,
            studio TEXT,
            PRIMARY KEY (anime_id, studio_id)
        );
        ''')
        self.cursor.connection.commit()

    def create_anime_other_titles_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE anime_other_titles (
            anime_id BIGINT,
            other_title TEXT,
            PRIMARY KEY (anime_id, other_title)
        );
        ''')
        self.cursor.connection.commit()

    def create_anime_ratings_distributions_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE ratings_distributions (
            anime_id BIGINT PRIMARY KEY,
            rat_1 INTEGER,
            rat_2 INTEGER,
            rat_3 INTEGER,
            rat_4 INTEGER,
            rat_5 INTEGER,
            rat_6 INTEGER,
            rat_7 INTEGER,
            rat_8 INTEGER,
            rat_9 INTEGER,
            rat_10 INTEGER
        );
        ''')
        self.cursor.connection.commit()


    def create_anime_recommendations_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE recommendations (
            anime_id BIGINT,
            rec_id BIGINT,
            rec_title TEXT,
            PRIMARY KEY (anime_id, rec_id)
        );
        ''')
        self.cursor.connection.commit()


    def create_anime_videos_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE videos (
            anime_id BIGINT,
            video_id BIGINT ,
            episode_number INTEGER,
            player_id  INTEGER,
            player_name TEXT,
            dubbing_name TEXT,
            date TIMESTAMPTZ,
            vid_index INTEGER,
            views INTEGER,
            duration INTEGER,
            PRIMARY KEY (anime_id, video_id)
        );
        ''')
        self.cursor.connection.commit()

    def create_anime_comments_table(self):
        self.cursor.execute(
        '''
        CREATE TABLE comments (
            anime_id BIGINT,
            comment_id BIGINT,
            text TEXT,
            children_count INTEGER,
            likes INTEGER,
            dislikes INTEGER,
            time TIMESTAMPTZ,
            PRIMARY KEY (anime_id, comment_id)
        );
        ''')
        self.cursor.connection.commit()


    def drop_table(self, table_name):
        if table_name in self.tables:
            self.cursor.execute(
            f'DROP TABLE {table_name}'
            )
            self.cursor.connection.commit()
        else:
            print('ошибка в названии таблицы')

    def close(self):
        self.cursor.close()
        self.conn.close()


    def load_anime_ids(self, ids_list):
        sql_anime_ids = '''
            INSERT INTO anime_ids (
                anime_id,
                title,
                anime_url,
                views,
                type,
                rating_avg,
                year
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (anime_id)
            DO UPDATE SET
                title = EXCLUDED.title,
                anime_url = EXCLUDED.anime_url,
                views = EXCLUDED.views,
                type = EXCLUDED.type,
                rating_avg = EXCLUDED.rating_avg,
                year = EXCLUDED.year
        '''
        self.cursor.executemany(sql_anime_ids, ids_list)
        self.cursor.connection.commit()


    def load_anime_main(self, row):

        sql_operation = '''
            INSERT INTO anime_main (
                anime_id,
                title,
                description,
                duration,
                anime_url,
                year,
                season,
                views,
                status_ru,
                type_ru,
                rating_all,
                rating_category,
                original_source,
                episodes_count,
                comments_count,
                lists_count
            )
            VALUES (%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,
                    %s)
            ON CONFLICT (anime_id)
            DO UPDATE SET
                title = EXCLUDED.title,
                description = EXCLUDED.description,
                duration = EXCLUDED.duration,
                anime_url = EXCLUDED.anime_url,
                year = EXCLUDED.year,
                season = EXCLUDED.season,
                views = EXCLUDED.views,
                status_ru = EXCLUDED.status_ru,
                type_ru = EXCLUDED.type_ru,
                rating_all = EXCLUDED.rating_all,
                rating_category = EXCLUDED.rating_category,
                original_source = EXCLUDED.original_source,
                episodes_count = EXCLUDED.episodes_count,
                comments_count = EXCLUDED.comments_count,
                lists_count = EXCLUDED.lists_count
        '''
        self.cursor.execute(sql_operation, row)
        self.cursor.connection.commit()

    def load_ratings_main(self, row):

        sql_operation = '''
            INSERT INTO ratings (
                anime_id,
                y_rating_avg,
                count,
                kp_rating,
                shikimori_rating,
                myanimelist_rating,
                worldart_rating
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (anime_id)
            DO UPDATE SET
                y_rating_avg = EXCLUDED.y_rating_avg,
                count = EXCLUDED.count,
                kp_rating = EXCLUDED.kp_rating,
                shikimori_rating = EXCLUDED.shikimori_rating,
                myanimelist_rating = EXCLUDED.myanimelist_rating,
                worldart_rating = EXCLUDED.worldart_rating
        '''
        self.cursor.execute(sql_operation, row)
        self.cursor.connection.commit()


    def load_genres_main(self, rows):

        sql_operation = '''
            INSERT INTO genres (
                anime_id,
                genre_id,
                title_ru,
                title_en,
                url
            )
            VALUES (%s,%s,%s,%s,%s)
            ON CONFLICT (anime_id, genre_id)
            DO UPDATE SET
                title_ru = EXCLUDED.title_ru,
                title_en = EXCLUDED.title_en,
                url = EXCLUDED.url
        '''
        self.cursor.executemany(sql_operation, rows)
        self.cursor.connection.commit()


    def load_min_ages_main(self, row):

        sql_operation = '''
            INSERT INTO min_ages (
                anime_id,
                age_id,
                age_ru,
                age_en
                )
            VALUES (%s,%s,%s,%s)
            ON CONFLICT (anime_id, age_id)
            DO UPDATE SET
                age_ru = EXCLUDED.age_ru,
                age_en = EXCLUDED.age_en
        '''
        self.cursor.execute(sql_operation, row)
        self.cursor.connection.commit()


    def load_other_ids_main(self, row):

        sql_operation = '''
            INSERT INTO other_ids (
                anime_id,
                myanimelist_id,
                shikimori_id
            )
            VALUES (%s,%s,%s)
            ON CONFLICT (anime_id)
            DO UPDATE SET
                myanimelist_id = EXCLUDED.myanimelist_id,
                shikimori_id = EXCLUDED.shikimori_id
        '''
        self.cursor.execute(sql_operation, row)
        self.cursor.connection.commit()


    def load_viewing_orders_main(self, rows):

        sql_operation = '''
            INSERT INTO viewing_orders (
                anime_id,
                related_anime_id,
                title,
                url,
                status_ru,
                type_ru,
                year,
                rating
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (anime_id, related_anime_id)
            DO UPDATE SET
                title = EXCLUDED.title,
                url = EXCLUDED.url,
                status_ru = EXCLUDED.status_ru,
                type_ru = EXCLUDED.type_ru,
                year = EXCLUDED.year,
                rating = EXCLUDED.rating
        '''
        self.cursor.executemany(sql_operation, rows)
        self.cursor.connection.commit()


    def load_creators_main(self, rows):

        sql_operation = '''
            INSERT INTO creators (
                anime_id,
                creator_ids,
                creator
            )
            VALUES (%s,%s,%s)
            ON CONFLICT (anime_id, creator_ids)
            DO UPDATE SET
                creator = EXCLUDED.creator
        '''
        self.cursor.executemany(sql_operation, rows)
        self.cursor.connection.commit()


    def load_studios_main(self, rows):

        sql_operation = '''
            INSERT INTO studios (
                anime_id,
                studio_id,
                studio
            )
            VALUES (%s,%s,%s)
            ON CONFLICT (anime_id, studio_id)
            DO UPDATE SET
                studio = EXCLUDED.studio
        '''
        self.cursor.executemany(sql_operation, rows)
        self.cursor.connection.commit()


    def load_other_titles_main(self, rows):

        sql_operation = '''
            INSERT INTO anime_other_titles (
                anime_id,
                other_title
            )
            VALUES (%s,%s)
            ON CONFLICT (anime_id, other_title)
            DO NOTHING
        '''
        self.cursor.executemany(sql_operation, rows)
        self.cursor.connection.commit()


    def load_ratings_distributions(self, row):

        sql_operation = '''
            INSERT INTO ratings_distributions (
                anime_id,
                rat_1,
                rat_2,
                rat_3,
                rat_4,
                rat_5,
                rat_6,
                rat_7,
                rat_8,
                rat_9,
                rat_10
            )
            VALUES (
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s
            )
            ON CONFLICT (anime_id)
            DO UPDATE SET
                rat_1 = EXCLUDED.rat_1,
                rat_2 = EXCLUDED.rat_2,
                rat_3 = EXCLUDED.rat_3,
                rat_4 = EXCLUDED.rat_4,
                rat_5 = EXCLUDED.rat_5,
                rat_6 = EXCLUDED.rat_6,
                rat_7 = EXCLUDED.rat_7,
                rat_8 = EXCLUDED.rat_8,
                rat_9 = EXCLUDED.rat_9,
                rat_10 = EXCLUDED.rat_10
        '''
        self.cursor.execute(sql_operation, row)
        self.cursor.connection.commit()


    def load_recommendations(self, rows):

        sql_operation = '''
            INSERT INTO recommendations (
                anime_id,
                rec_id,
                rec_title
            )
            VALUES (%s,%s,%s)
            ON CONFLICT (anime_id, rec_id)
            DO UPDATE SET
                rec_title = EXCLUDED.rec_title
        '''
        self.cursor.executemany(sql_operation, rows)
        self.cursor.connection.commit()


    def load_videos(self, rows):

        sql_operation = '''
            INSERT INTO videos (
                anime_id,
                video_id,
                episode_number,
                player_id,
                player_name,
                dubbing_name,
                date,
                vid_index,
                views,
                duration
            )
            VALUES (
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s
            )
            ON CONFLICT (anime_id, video_id)
            DO UPDATE SET
                episode_number = EXCLUDED.episode_number,
                player_id = EXCLUDED.player_id,
                player_name = EXCLUDED.player_name,
                dubbing_name = EXCLUDED.dubbing_name,
                date = EXCLUDED.date,
                vid_index = EXCLUDED.vid_index,
                views = EXCLUDED.views,
                duration = EXCLUDED.duration
        '''
        self.cursor.executemany(sql_operation, rows)
        self.cursor.connection.commit()


    def load_comments(self, rows):

        sql_operation = '''
            INSERT INTO comments (
                anime_id,
                comment_id,
                text,
                children_count,
                likes,
                dislikes,
                time
            )
            VALUES (
                %s,%s,%s,%s,%s,%s,%s
            )
            ON CONFLICT (anime_id, comment_id)
            DO UPDATE SET
                text = EXCLUDED.text,
                children_count = EXCLUDED.children_count,
                likes = EXCLUDED.likes,
                dislikes = EXCLUDED.dislikes,
                time = EXCLUDED.time
        '''
        self.cursor.executemany(sql_operation, rows)
        self.cursor.connection.commit()


class RequestParser:
    @staticmethod
    def parse_anime_ids_request(i_anime):
        anime_id = i_anime.get('anime_id')
        title = i_anime.get('title')
        anime_url = i_anime.get('anime_url')
        views = i_anime.get('views')
        anime_type = i_anime.get('type', {}).get('name')
        rating = i_anime.get('rating', {}).get('average')
        anime_year = i_anime.get('year')

        row = (anime_id, title, anime_url, views, anime_type, rating, anime_year)

        return row

    @staticmethod
    def parse_anime_main_request(anime_id, main_inf):
        a_title = main_inf.get('title')
        a_description = main_inf.get('description')
        a_duration = main_inf.get('duration')
        a_url = main_inf.get('anime_url')
        a_year = main_inf.get('year')
        a_season = main_inf.get('season')
        a_views = main_inf.get('views')
        a_status_ru = main_inf.get('anime_status', {}).get('title')
        a_type_ru = main_inf.get('type', {}).get('name')
        a_rating_place_over_all = main_inf.get('top', {}).get('global')
        a_rating_place_over_category = main_inf.get('top', {}).get('category')
        a_original = main_inf.get('original')
        a_episodes_count = main_inf.get('episodes', {}).get('count')
        a_comments_count = main_inf.get('comments_count')
        a_lists_count = main_inf.get('lists_count')

        row = (anime_id, a_title, a_description, a_duration, a_url,
            a_year, a_season, a_views, a_status_ru, a_type_ru,
            a_rating_place_over_all, a_rating_place_over_category,
            a_original, a_episodes_count, a_comments_count, a_lists_count)
        
        return row

    @staticmethod
    def parse_raings_main_request(anime_id, main_inf):
        a_rating_avg = main_inf.get('rating', {}).get('average')
        a_rating_counts = main_inf.get('rating', {}).get('counters')
        a_kp_rating = main_inf.get('rating', {}).get('kp_rating' )
        a_shikimori_rating = main_inf.get('rating', {}).get('shikimori_rating')
        a_myanimelist_rating = main_inf.get('rating', {}).get('myanimelist_rating')
        a_worldart_rating = main_inf.get('rating', {}).get('worldart_rating')

        row = (anime_id, a_rating_avg, a_rating_counts, a_kp_rating, a_shikimori_rating,
            a_myanimelist_rating, a_worldart_rating)
        
        return row

    @staticmethod
    def parse_genres_main_request(anime_id, main_inf):
        genres_rows = []
        a_genres = main_inf.get('genres', [])
        for genre in a_genres:
            a_title_ru = genre.get('title')
            a_title_en = genre.get('alias')
            a_genre_id = genre.get('id')
            a_genre_url = genre.get('url')

            row = (anime_id, a_genre_id, a_title_ru, a_title_en, a_genre_url)
            genres_rows.append(row)

        return genres_rows

    @staticmethod
    def parse_ages_main_request(anime_id, main_inf):
        a_age_ru = main_inf.get('min_age', {}).get('title_long')
        a_age_en = main_inf.get('min_age', {}).get('title')
        a_age_id = main_inf.get('min_age', {}).get('value')

        row = (anime_id, a_age_id, a_age_ru, a_age_en)

        return row

    @staticmethod
    def parse_other_ids_main_request(anime_id, main_inf):
        a_myanimelist_id = main_inf.get('remote_ids', {}).get('myanimelist_id')
        a_shikimori_id = main_inf.get('remote_ids', {}).get('shikimori_id')

        row = (anime_id, a_myanimelist_id, a_shikimori_id)

        return row

    @staticmethod
    def parse_viewing_order_main_request(anime_id, main_inf):
        viewing_order_list = []
        a_viewing_order = main_inf.get('viewing_order', []) 
        for a_itm in a_viewing_order:
            a_id_2 = a_itm.get('anime_id')
            a_title_2 = a_itm.get('title')
            a_url_2 = a_itm.get('anime_url')
            a_2_status_ru = a_itm.get('anime_status', {}).get('title')
            a_2_type_ru = a_itm.get('type', {}).get('name')
            a_2_year = a_itm.get('year')
            a_2_rating = a_itm.get('rating')

            row = (anime_id, a_id_2, a_title_2, a_url_2, a_2_status_ru,
                   a_2_type_ru, a_2_year, a_2_rating)
            viewing_order_list.append(row)

        return viewing_order_list

    @staticmethod
    def parse_creators_main_request(anime_id, main_inf):
        creators_list = []
        a_creators = main_inf.get('creators', [])
        for c_itm in a_creators:
            c_id = c_itm.get('id')
            c_name = c_itm.get('title')

            row = (anime_id, c_id, c_name)
            creators_list.append(row)

        return creators_list

    @staticmethod
    def parse_studios_main_request(anime_id, main_inf):
        studios_list = []
        a_studios = main_inf.get('studios', [])
        for s_itm in a_studios:
            s_id = s_itm.get('id')
            s_name = s_itm.get('title')

            row = (anime_id, s_id, s_name)
            studios_list.append(row)

        return studios_list
    
    @staticmethod
    def parse_other_titles_main_request(anime_id, main_inf):
        titles_list = []
        a_other_anime_names = main_inf.get('other_titles', [])
        for name in a_other_anime_names:
            oth_title = name
  
            row = (anime_id, oth_title)
            titles_list.append(row)

        return titles_list
    
    @staticmethod
    def parse_rates_distrb_request(anime_id, rates_distrb):
        rates_dict = {}
        for r_itm in rates_distrb:
            rates_dict[r_itm.get('rating')] = r_itm.get('count')
        
        row = [anime_id] + [rates_dict[r] for r in range(1,11)]

        return row
    
    @staticmethod
    def parse_reccomendation_request(anime_id, recomends):
        rec_list = []
        for rec_itm in recomends:
            rec_id = rec_itm.get('anime_id')
            rec_title = rec_itm.get('title')
            
            row = (anime_id, rec_id, rec_title)
            rec_list.append(row)

        return rec_list
    
    @staticmethod
    def parse_videos_request(anime_id, vids_info):
        vids_list = []
        for vid in vids_info:
            v_id = vid.get('video_id')
            v_number = vid.get('number')
            v_player = vid.get('data').get('player')
            v_player_id = vid.get('data').get('player_id')
            v_dubbing = vid.get('data').get('dubbing')
            v_date = (datetime.fromtimestamp(vid.get('date')) if vid.get('date') else None)
            v_index = vid.get('index')
            v_views = vid.get('views')
            v_durations = vid.get('duration')

            row = (anime_id, v_id, v_number, v_player_id, v_player,
                   v_dubbing, v_date, v_index, v_views, v_durations)
            vids_list.append(row)

        return vids_list

    @staticmethod
    def parse_comments_request(anime_id, comments_list):
        c_list = []
        for comment in comments_list:
            com_id = comment.get('id')
            com_text = comment.get('text')
            com_childrens = comment.get('children_count')
            com_likes = comment.get('likes')
            com_dislikes = comment.get('dislikes')
            com_time = (datetime.fromtimestamp(comment.get('time')) if comment.get('time') else None)

            row = (anime_id, com_id, com_text, com_childrens,
                   com_likes, com_dislikes, com_time)
            c_list.append(row)

        return c_list


class DataCollector:
    def __init__(self, db_class:PostgresDB, request_class:RequestsAnimeMain):
        self.db_class = db_class
        self.request_class = request_class

    def collect_anime_ids_by_api(self, year_begin=1900, year_end=2030):
        '''
        Заполнение таблицы anime_ids через апи
        '''

        anime_counter = 0

        for status in range(0, 3, 1):

            if status == 0:

                for year in range(year_begin, year_end + 1, 1):
                    skip = 0
                    skip_step = 100

                    while True:
                        anime_ids = self.request_class.request_anime_ids(year, status, skip, skip_step)
                        time.sleep(1)

                        if (anime_ids is None) or (not anime_ids):
                            break
                        else:
                            ids_list = [RequestParser().parse_anime_ids_request(item) for item in anime_ids]
                        
                        self.db_class.load_anime_ids(ids_list)
                        anime_counter += len(ids_list)
                        skip += skip_step        
            else:
                skip = 0
                skip_step = 100
                
                while True:
                    year = None
                    anime_ids = self.request_class.request_anime_ids(year, status, skip, skip_step)

                    if (anime_ids is None) or (not anime_ids):
                        break
                    else:
                        ids_list = [RequestParser().parse_anime_ids_request(item) for item in anime_ids]

                    self.db_class.load_anime_ids(ids_list)
                    anime_counter += len(ids_list)
                    skip += skip_step
                    time.sleep(1)
                            
        print(f'собрано {anime_counter} аниме')


    def collect_anime_main(self, anime_id):
        
        main_inf = self.request_class.request_anime_data(anime_id)
        time.sleep(1.0)
        if (main_inf is None) or (not main_inf):
            return 0
        else:
            self.db_class.load_anime_main(RequestParser.parse_anime_main_request(anime_id, main_inf))
            self.db_class.load_ratings_main(RequestParser.parse_raings_main_request(anime_id, main_inf))
            self.db_class.load_genres_main(RequestParser.parse_genres_main_request(anime_id, main_inf))
            self.db_class.load_min_ages_main(RequestParser.parse_ages_main_request(anime_id, main_inf))
            self.db_class.load_other_ids_main(RequestParser.parse_other_ids_main_request(anime_id, main_inf))
            self.db_class.load_viewing_orders_main(RequestParser.parse_viewing_order_main_request(anime_id, main_inf))
            self.db_class.load_creators_main(RequestParser.parse_creators_main_request(anime_id, main_inf))
            self.db_class.load_studios_main(RequestParser.parse_studios_main_request(anime_id, main_inf))
            self.db_class.load_other_titles_main(RequestParser.parse_other_titles_main_request(anime_id, main_inf))
        return 1


    def collect_rates_distrb(self, anime_id):
        anime_rates_distrb = self.request_class.request_anime_rates_distrb(anime_id)
        time.sleep(1.0)
        if (anime_rates_distrb is None) or (not anime_rates_distrb):
            return 0
        else:
            self.db_class.load_ratings_distributions(RequestParser.parse_rates_distrb_request(anime_id, anime_rates_distrb))
        return 1


    def collect_recomends(self, anime_id):
        recomends = self.request_class.request_reccomendation(anime_id)
        time.sleep(1.0)
        if (recomends is None) or (not recomends):
            return 0
        else:
            self.db_class.load_recommendations(RequestParser.parse_reccomendation_request(anime_id, recomends))
        return 1


    def collect_videos(self, anime_id):
        vids_info = self.request_class.request_vidos_inf(anime_id)
        time.sleep(1.0)
        if (vids_info is None) or (not vids_info):
            return 0
        else:
            self.db_class.load_videos(RequestParser.parse_videos_request(anime_id, vids_info))
        return 1

    def collect_comments(self, anime_id):
        skip = 0
        skip_step = 50
        comments_counter = 0

        while True:
            comments_list = self.request_class.request_comments_inf(anime_id, skip, skip_step)
            time.sleep(1.0)
            comments_counter += len(comments_list)

            if (comments_list is None) or (not comments_list):
                break
            else:
                self.db_class.load_comments(RequestParser.parse_comments_request(anime_id, comments_list))
            skip += skip_step

        if comments_counter == 0:
            return 0
        else:
            print(f'аниме {anime_id}, собрано {comments_counter} комментариев')
            return 1
            

def main():
    print('тут только фунции и классы')


if __name__ == '__main__':
    main()