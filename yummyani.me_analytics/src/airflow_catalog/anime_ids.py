import os
from dotenv import load_dotenv
from api_clients.yani_api_client import RequestsAnimeMain
from database.schema import create_anime_ids_table
from database.connection import PostgresDB 
from collector import collect_anime_ids_by_api

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

    create_anime_ids_table(posgdb.cursor)
    collect_anime_ids_by_api(posgdb.cursor, y_req=req_class)
    # print('working')

    posgdb.close()

if __name__ == '__main__':
    main()