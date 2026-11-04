def load_anime_ids(cursor, ids_list):
    sql_anime_ids = '''
        INSERT INTO anime_ids (
            anime_id,
            title,
            anime_url,
            views,
            type,
            rating_avg,
            n_ratings,
            year
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (anime_id)
        DO UPDATE SET
            title = EXCLUDED.title,
            anime_url = EXCLUDED.anime_url,
            views = EXCLUDED.views,
            type = EXCLUDED.type,
            rating_avg = EXCLUDED.rating_avg,
            n_ratings = EXCLUDED.n_ratings,
            year = EXCLUDED.year
    '''
    cursor.executemany(sql_anime_ids, ids_list)
    cursor.connection.commit()

def get_anime_ids_from(cursor, start_anime_id=0):

    if start_anime_id:
        cursor.execute('''
            SELECT anime_id
            FROM anime_ids
            WHERE anime_id >= %s
            ORDER BY anime_id
        ''', (start_anime_id,))
    else:
        cursor.execute('''
            SELECT anime_id
            FROM anime_ids
            ORDER BY anime_id
        ''')

    return [row[0] for row in cursor.fetchall()]

def load_anime_main(cursor, row):

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
    cursor.execute(sql_operation, row)
    cursor.connection.commit()

def load_ratings_main(cursor, row):

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
    cursor.execute(sql_operation, row)
    cursor.connection.commit()

def load_genres_main(cursor, rows):

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
    cursor.executemany(sql_operation, rows)
    cursor.connection.commit()


def load_min_ages_main(cursor, row):

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
    cursor.execute(sql_operation, row)
    cursor.connection.commit()

def load_other_ids_main(cursor, row):

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
    cursor.execute(sql_operation, row)
    cursor.connection.commit()

def load_viewing_orders_main(cursor, rows):

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
    cursor.executemany(sql_operation, rows)
    cursor.connection.commit()

def load_creators_main(cursor, rows):

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
    cursor.executemany(sql_operation, rows)
    cursor.connection.commit()

def load_studios_main(cursor, rows):

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
    cursor.executemany(sql_operation, rows)
    cursor.connection.commit()

def load_other_titles_main(cursor, rows):

    sql_operation = '''
        INSERT INTO anime_other_titles (
            anime_id,
            other_title
        )
        VALUES (%s,%s)
        ON CONFLICT (anime_id, other_title)
        DO NOTHING
    '''
    cursor.executemany(sql_operation, rows)
    cursor.connection.commit()

def load_ratings_distributions(cursor, row):

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
    cursor.execute(sql_operation, row)
    cursor.connection.commit()

def load_recommendations(cursor, rows):

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
    cursor.executemany(sql_operation, rows)
    cursor.connection.commit()

def load_videos(cursor, rows):

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
    cursor.executemany(sql_operation, rows)
    cursor.connection.commit()

def load_comments(cursor, rows):

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
    cursor.executemany(sql_operation, rows)
    cursor.connection.commit()