import os
from dotenv import load_dotenv
from api_clients.yani_api_client import RequestsAnimeMain
from database.schema import create_all_tables
from database.connection import PostgresDB 
from database.data import get_anime_ids_from
import collector as ycol

def main():
    load_dotenv()

    x_token = os.environ['x_token']

    bd_config = {
        'host' : os.environ['host'],
        'dbname' : os.environ['postgre_bd'],
        'user' : os.environ['user'],
        'password' : os.environ['psw']
    } 

    posgdb = PostgresDB(bd_config)
    posgdb.open_conn()
    req_class = RequestsAnimeMain(x_token)

    create_all_tables(posgdb.cursor)
    ycol.collect_anime_ids_by_api(posgdb.cursor, y_req=req_class)

    anime_ids = get_anime_ids_from(posgdb.cursor)

    for ani_id in anime_ids:
        ycol.collect_anime_main(ani_id, req_class, posgdb.cursor)
        ycol.collect_rates_distrb(ani_id, req_class, posgdb.cursor)
        ycol.collect_recomends(ani_id, req_class, posgdb.cursor)
        ycol.collect_videos(ani_id, req_class, posgdb.cursor)
        ycol.collect_comments(ani_id, req_class, posgdb.cursor)
        break

    posgdb.close()

if __name__ == '__main__':
    main()