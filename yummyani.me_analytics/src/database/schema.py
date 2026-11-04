



def create_anime_ids_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS anime_ids (
        anime_id BIGINT PRIMARY KEY,
        title TEXT,
        anime_url TEXT,
        views INTEGER,
        type TEXT,
        rating_avg NUMERIC,
        n_ratings NUMERIC,
        year INTEGER
    );
    ''')
    cursor.connection.commit()

def create_anime_main_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS anime_main (
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
    cursor.connection.commit()
    
def create_anime_ratings_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS ratings (
        anime_id BIGINT PRIMARY KEY,
        y_rating_avg NUMERIC,
        count INTEGER,
        kp_rating NUMERIC,
        shikimori_rating NUMERIC,
        myanimelist_rating NUMERIC,
        worldart_rating NUMERIC
    );
    ''')
    cursor.connection.commit()

def create_anime_genres_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS genres (
        anime_id BIGINT,
        genre_id BIGINT,
        title_ru TEXT,
        title_en TEXT,
        url TEXT,
        PRIMARY KEY (anime_id, genre_id)
    );
    ''')
    cursor.connection.commit()

def create_anime_min_ages_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS min_ages (
        anime_id BIGINT,
        age_id BIGINT,
        age_ru TEXT,
        age_en TEXT,
        PRIMARY KEY (anime_id, age_id)
    );
    ''')
    cursor.connection.commit()

def create_anime_other_ids_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS other_ids (
        anime_id BIGINT PRIMARY KEY,
        myanimelist_id BIGINT,
        shikimori_id BIGINT
    );
    ''')
    cursor.connection.commit()

def create_anime_viewing_orders_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS viewing_orders (
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
    cursor.connection.commit()

def create_anime_creators_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS creators (
        anime_id BIGINT,
        creator_ids BIGINT,
        creator TEXT,
        PRIMARY KEY (anime_id, creator_ids)
    );
    ''')
    cursor.connection.commit()

def create_anime_studios_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS studios (
        anime_id BIGINT,
        studio_id BIGINT,
        studio TEXT,
        PRIMARY KEY (anime_id, studio_id)
    );
    ''')
    cursor.connection.commit()

def create_anime_other_titles_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS anime_other_titles (
        anime_id BIGINT,
        other_title TEXT,
        PRIMARY KEY (anime_id, other_title)
    );
    ''')
    cursor.connection.commit()

def create_anime_ratings_distributions_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS ratings_distributions (
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
    cursor.connection.commit()

def create_anime_recommendations_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS recommendations (
        anime_id BIGINT,
        rec_id BIGINT,
        rec_title TEXT,
        PRIMARY KEY (anime_id, rec_id)
    );
    ''')
    cursor.connection.commit()

def create_anime_videos_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS videos (
        anime_id BIGINT,
        video_id BIGINT ,
        episode_number TEXT,
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
    cursor.connection.commit()

def create_anime_comments_table(cursor):
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS comments (
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
    cursor.connection.commit()

def drop_table(cursor, table_name, tables):
    if table_name in tables:
        cursor.execute(
        f'DROP TABLE IF EXISTS {table_name}'
        )
        cursor.connection.commit()
    else:
        print('ошибка в названии таблицы')


def create_all_tables(cursor):
    create_anime_ids_table(cursor)
    create_anime_main_table(cursor)
    create_anime_ratings_table(cursor)
    create_anime_genres_table(cursor)
    create_anime_min_ages_table(cursor)
    create_anime_other_ids_table(cursor)
    create_anime_viewing_orders_table(cursor)
    create_anime_creators_table(cursor)
    create_anime_studios_table(cursor)
    create_anime_other_titles_table(cursor)
    create_anime_ratings_distributions_table(cursor)
    create_anime_recommendations_table(cursor)
    create_anime_videos_table(cursor)
    create_anime_comments_table(cursor)


def drop_all_tables():
    pass

