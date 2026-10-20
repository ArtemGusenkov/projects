from dotenv import load_dotenv
import psycopg as ps
import os
load_dotenv()

bd_config = {
    'host' : os.environ['host'],
    'dbname' : os.environ['postgre_bd'],
    'user' : os.environ['user'],
    'password' : os.environ['psw']
} 

def create_table(sql_querry):
    with ps.connect(**bd_config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_querry)


def transaction_data():
    '''
    creating transaction data table
    '''
    sql_querry = '''
                CREATE TABLE IF NOT EXISTS transaction_data (
                household_key BIGINT,
                basket_id BIGINT,
                day INT,
                product_id BIGINT REFERENCES product(product_id),
                quantity BIGINT,
                sales_value FLOAT,
                store_id BIGINT,
                retail_disc FLOAT,
                trans_time BIGINT,
                week_no INT,
                coupon_disc FLOAT,
                coupon_match_disc FLOAT,
                PRIMARY KEY (household_key, basket_id, product_id)
                );
                '''
    create_table(sql_querry)


def campaign_desc():
    '''
    creating campaign_desc table
    '''
    sql_querry = '''
                CREATE TABLE IF NOT EXISTS campaign_desc (
                description TEXT,
                campaign INT,
                start_day BIGINT,
                end_day BIGINT,
                PRIMARY KEY (campaign)
                );
                '''
    create_table(sql_querry)


def campaign_table():
    '''
    creating campaign_table table
    '''
    sql_querry = '''
                CREATE TABLE IF NOT EXISTS campaign_table (
                description TEXT,
                household_key BIGINT,
                campaign INT REFERENCES campaign_desc(campaign),
                PRIMARY KEY (household_key, campaign)
                );
                '''
    create_table(sql_querry)


def coupon():
    '''
    creating coupon table
    '''
    sql_querry = '''
                CREATE TABLE IF NOT EXISTS coupon (
                coupon_upc BIGINT,
                product_id BIGINT REFERENCES product(product_id),
                campaign INT REFERENCES campaign_desc(campaign),
                PRIMARY KEY (coupon_upc, campaign, product_id)
                );
                '''
    create_table(sql_querry)


def coupon_redempt():
    '''
    creating coupon_redempt table
    '''
    sql_querry = '''
                CREATE TABLE IF NOT EXISTS coupon_redempt (
                household_key BIGINT,
                day INT,
                coupon_upc BIGINT,
                campaign INT REFERENCES campaign_desc(campaign),
                PRIMARY KEY (household_key, coupon_upc)
                );
                '''
    create_table(sql_querry)


def hh_demographic():
    '''
    creating hh_demographic table
    '''
    sql_querry = '''
                CREATE TABLE IF NOT EXISTS hh_demographic (
                classification_1 TEXT,
                classification_2 TEXT,
                classification_3 TEXT,
                classification_4 TEXT,
                classification_5 TEXT,
                classification_6 TEXT,
                classification_7 TEXT,
                household_key BIGINT,
                PRIMARY KEY (household_key)
                );
                '''
    create_table(sql_querry)


def product():
    '''
    creating product table
    '''
    sql_querry = '''
                CREATE TABLE IF NOT EXISTS product (
                product_id BIGINT,
                manufacturer BIGINT,
                department TEXT,
                brand TEXT,
                commodity_desc TEXT,
                sub_commodity_desc TEXT,
                curr_size_of_product TEXT,
                PRIMARY KEY (product_id)
                );
                '''
    create_table(sql_querry)


def causal_data():
    '''
    creating causal_data table
    '''
    sql_querry = '''
                CREATE TABLE IF NOT EXISTS causal_data (
                product_id BIGINT,
                store_id BIGINT,
                week_no INT,
                display TEXT,
                mailer TEXT,
                PRIMARY KEY (product_id, store_id, week_no, display)
                );
                '''
    create_table(sql_querry)


def drop_table(table_name):
    with ps.connect(**bd_config) as conn:
                with conn.cursor() as cur:
                    cur.execute(f'DROP TABLE IF EXISTS {table_name} CASCADE')


def drop_all_tables():
    drop_table('transaction_data')
    drop_table('campaign_desc')
    drop_table('campaign_table')
    drop_table('coupon')
    drop_table('coupon_redempt')
    drop_table('hh_demographic')
    drop_table('product')
    drop_table('causal_data')


if __name__ == '__main__':
    product()
    transaction_data()
    campaign_desc()
    campaign_table()
    coupon()
    coupon_redempt()
    hh_demographic()
    causal_data()


    # drop_all_tables()

