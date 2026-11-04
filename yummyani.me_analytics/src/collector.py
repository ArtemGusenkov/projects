import time
import parsers.yani_parser as ypr
import database.data as ydl
import api_clients.yani_api_client as yap


def collect_anime_ids_by_api(cursor, year_begin=1900, year_end=2030, y_req:yap.RequestsAnimeMain=None):
    '''
    Заполнение таблицы anime_ids
    '''

    anime_counter = 0

    for status in range(0, 3, 1):

        if status == 0:

            for year in range(year_begin, year_end + 1, 1):
                skip = 0
                skip_step = 100

                while True:
                    anime_ids = y_req.request_anime_ids(year, status, skip, skip_step)
                    time.sleep(1.0)

                    if (anime_ids is None) or (not anime_ids):
                        break
                    else:
                        ids_list = [ypr.parse_anime_ids_request(item) for item in anime_ids]
                    
                    ydl.load_anime_ids(cursor, ids_list)
                    anime_counter += len(ids_list)
                    skip += skip_step        
        else:
            skip = 0
            skip_step = 100
            
            while True:
                year = None
                anime_ids = y_req.request_anime_ids(year, status, skip, skip_step)
                time.sleep(1.0)

                if (anime_ids is None) or (not anime_ids):
                    break
                else:
                    ids_list = [ypr.parse_anime_ids_request(item) for item in anime_ids]

                ydl.load_anime_ids(cursor, ids_list)
                anime_counter += len(ids_list)
                skip += skip_step
                        
    print(f'собрано {anime_counter} аниме')


def collect_anime_main(anime_id, y_req, cursor):
    
    main_inf = y_req.request_anime_data(anime_id)
    time.sleep(1.0)
    if (main_inf is None) or (not main_inf):
        return 0
    else:
        ydl.load_anime_main(cursor,ypr.parse_anime_main_request(anime_id, main_inf))
        ydl.load_ratings_main(cursor,ypr.parse_raings_main_request(anime_id, main_inf))
        ydl.load_genres_main(cursor,ypr.parse_genres_main_request(anime_id, main_inf))
        ydl.load_min_ages_main(cursor,ypr.parse_ages_main_request(anime_id, main_inf))
        ydl.load_other_ids_main(cursor,ypr.parse_other_ids_main_request(anime_id, main_inf))
        ydl.load_viewing_orders_main(cursor,ypr.parse_viewing_order_main_request(anime_id, main_inf))
        ydl.load_creators_main(cursor,ypr.parse_creators_main_request(anime_id, main_inf))
        ydl.load_studios_main(cursor,ypr.parse_studios_main_request(anime_id, main_inf))
        ydl.load_other_titles_main(cursor,ypr.parse_other_titles_main_request(anime_id, main_inf))
    return 1


def collect_rates_distrb(anime_id, y_req, cursor):
    anime_rates_distrb = y_req.request_anime_rates_distrb(anime_id)
    time.sleep(1.0)
    if (anime_rates_distrb is None) or (not anime_rates_distrb):
        return 0
    else:
        ydl.load_ratings_distributions(cursor, ypr.parse_rates_distrb_request(anime_id, anime_rates_distrb))
    return 1


def collect_recomends(anime_id, y_req, cursor):
    recomends = y_req.request_reccomendation(anime_id)
    time.sleep(1.0)
    if (recomends is None) or (not recomends):
        return 0
    else:
        ydl.load_recommendations(cursor, ypr.parse_reccomendation_request(anime_id, recomends))
    return 1


def collect_videos(anime_id, y_req, cursor):
    vids_info = y_req.request_vidos_inf(anime_id)
    time.sleep(1.0)
    if (vids_info is None) or (not vids_info):
        return 0
    else:
        ydl.load_videos(cursor, ypr.parse_videos_request(anime_id, vids_info))
    return 1

def collect_comments(anime_id, y_req, cursor):
    skip = 0
    skip_step = 50
    comments_counter = 0

    while True:
        comments_list = y_req.request_comments_inf(anime_id, skip, skip_step)
        time.sleep(1.0)

        if (comments_list is None) or (not comments_list):
            break
        else:
            ydl.load_comments(cursor, ypr.parse_comments_request(anime_id, comments_list))
            comments_counter += len(comments_list)
        skip += skip_step

    if comments_counter == 0:
        return 0
    else:
        print(f'аниме {anime_id}, собрано {comments_counter} комментариев')
        return 1


def collect_all_data(anime_id, y_req, cursor):
    collect_anime_main(anime_id, y_req, cursor)
    collect_rates_distrb(anime_id, y_req, cursor)
    collect_recomends(anime_id, y_req, cursor)
    collect_videos(anime_id, y_req, cursor)
    collect_comments(anime_id, y_req, cursor)
        

