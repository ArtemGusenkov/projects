from datetime import datetime


def parse_anime_ids_request(i_anime):
    anime_id = i_anime.get('anime_id')
    title = i_anime.get('title')
    anime_url = i_anime.get('anime_url')
    views = i_anime.get('views')
    anime_type = i_anime.get('type', {}).get('name')
    rating = i_anime.get('rating', {}).get('average')
    n_rating = i_anime.get('rating').get('counters')
    anime_year = i_anime.get('year')

    row = (anime_id, title, anime_url, views, anime_type, rating, n_rating, anime_year)

    return row


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


def parse_ages_main_request(anime_id, main_inf):
    a_age_ru = main_inf.get('min_age', {}).get('title_long')
    a_age_en = main_inf.get('min_age', {}).get('title')
    a_age_id = main_inf.get('min_age', {}).get('value')

    row = (anime_id, a_age_id, a_age_ru, a_age_en)

    return row


def parse_other_ids_main_request(anime_id, main_inf):
    a_myanimelist_id = main_inf.get('remote_ids', {}).get('myanimelist_id')
    a_shikimori_id = main_inf.get('remote_ids', {}).get('shikimori_id')

    row = (anime_id, a_myanimelist_id, a_shikimori_id)

    return row

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

def parse_creators_main_request(anime_id, main_inf):
    creators_list = []
    a_creators = main_inf.get('creators', [])
    for c_itm in a_creators:
        c_id = c_itm.get('id')
        c_name = c_itm.get('title')

        row = (anime_id, c_id, c_name)
        creators_list.append(row)

    return creators_list

def parse_studios_main_request(anime_id, main_inf):
    studios_list = []
    a_studios = main_inf.get('studios', [])
    for s_itm in a_studios:
        s_id = s_itm.get('id')
        s_name = s_itm.get('title')

        row = (anime_id, s_id, s_name)
        studios_list.append(row)

    return studios_list

def parse_other_titles_main_request(anime_id, main_inf):
    titles_list = []
    a_other_anime_names = main_inf.get('other_titles', [])
    for name in a_other_anime_names:
        oth_title = name

        row = (anime_id, oth_title)
        titles_list.append(row)

    return titles_list

def parse_rates_distrb_request(anime_id, rates_distrb):
    rates_dict = {}
    for r_itm in rates_distrb:
        rates_dict[r_itm.get('rating')] = r_itm.get('count')
    
    row = [anime_id] + [rates_dict[r] for r in range(1,11)]

    return row

def parse_reccomendation_request(anime_id, recomends):
    rec_list = []
    for rec_itm in recomends:
        rec_id = rec_itm.get('anime_id')
        rec_title = rec_itm.get('title')
        
        row = (anime_id, rec_id, rec_title)
        rec_list.append(row)

    return rec_list

def parse_videos_request(anime_id, vids_info):
    vids_list = []
    for vid in vids_info:
        v_id = vid.get('video_id')
        v_number = vid.get('number')
        v_player = vid.get('data', {}).get('player')
        v_player_id = vid.get('data', {}).get('player_id')
        v_dubbing = vid.get('data', {}).get('dubbing')
        v_date = (datetime.fromtimestamp(vid.get('date')) if vid.get('date') else None)
        v_index = vid.get('index')
        v_views = vid.get('views')
        v_durations = vid.get('duration')

        row = (anime_id, v_id, v_number, v_player_id, v_player,
                v_dubbing, v_date, v_index, v_views, v_durations)
        vids_list.append(row)

    return vids_list

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