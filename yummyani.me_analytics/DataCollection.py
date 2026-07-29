import funcs_yum as fy
from settings import x_token, s_token, host, postgre_bd, user, psw

def main():
    posgdb = fy.PostgresDB(host, postgre_bd, user, psw)

    req_class = fy.RequestsAnimeMain(x_token, s_token)

    fdc = fy.DataCollector(posgdb, req_class)

    # posgdb.create_anime_ids_table()

    # fdc.collect_anime_ids_by_api()

    anime_ids = posgdb.get_anime_ids_from(10882)

    # posgdb.create_anime_main_table()
    # posgdb.create_anime_ratings_table()
    # posgdb.create_anime_genres_table()
    # posgdb.create_anime_min_ages_table()
    # posgdb.create_anime_other_ids_table()
    # posgdb.create_anime_viewing_orders_table()
    # posgdb.create_anime_creators_table()
    # posgdb.create_anime_studios_table()
    # posgdb.create_anime_other_titles_table()
    # posgdb.create_anime_ratings_distributions_table()
    # posgdb.create_anime_recommendations_table()
    # posgdb.create_anime_videos_table()
    # posgdb.create_anime_comments_table()

    for ani_id in anime_ids:
        fdc.collect_anime_main(ani_id)
        fdc.collect_rates_distrb(ani_id)
        fdc.collect_recomends(ani_id)
        fdc.collect_videos(ani_id)
        fdc.collect_comments(ani_id)

    posgdb.close()

if __name__ == '__main__':
    main()