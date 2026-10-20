from dotenv import load_dotenv
import psycopg as ps
import os
import pandas as pd

load_dotenv()

bd_config = {
    'host' : os.environ['host'],
    'dbname' : os.environ['postgre_bd'],
    'user' : os.environ['user'],
    'password' : os.environ['psw']
} 

def insert_data(file, sql_querry):
    df = pd.read_csv(file)
    n, m = df.shape
    for i in range(0,n,100000):
        with ps.connect(**bd_config) as con:
            with con.cursor() as cur:
                cur.executemany(sql_querry, df.iloc[i:i+100000, :].values.tolist())

def insert_transaction_data():  
    sql_querry = (
                '''
                INSERT INTO transaction_data (
                    household_key,
                    basket_id,
                    day,
                    product_id,
                    quantity,
                    sales_value,
                    store_id,
                    retail_disc,
                    trans_time,
                    week_no,
                    coupon_disc,
                    coupon_match_disc
                )
                VALUES (%s, %s, %s, %s, 
                        %s, %s, %s, %s, 
                        %s, %s, %s, %s                
                )
                ON CONFLICT (household_key, basket_id, product_id)
                DO NOTHING
                '''
                )
    insert_data(r'datasets/transaction_data.csv', sql_querry)


def insert_campaign_desc():  
    sql_querry = (
                '''
                INSERT INTO campaign_desc (
                    description,
                    campaign,
                    start_day,
                    end_day
                )
                VALUES (%s, %s, %s, %s                
                )
                ON CONFLICT (campaign)
                DO NOTHING
                '''
                )
    insert_data(r'datasets/campaign_desc.csv', sql_querry)


def insert_campaign_table():  
    sql_querry = (
                '''
                INSERT INTO campaign_table (
                    description,
                    household_key,
                    campaign
                )
                VALUES (%s, %s, %s               
                )
                ON CONFLICT (household_key, campaign)
                DO NOTHING
                '''
                )
    insert_data(r'datasets/campaign_table.csv', sql_querry)


def insert_coupon():  
    sql_querry = (
                '''
                INSERT INTO coupon (
                    coupon_upc,
                    product_id,
                    campaign
                )
                VALUES (%s, %s, %s               
                )
                ON CONFLICT (coupon_upc, campaign, product_id)
                DO NOTHING
                '''
                )
    insert_data(r'datasets/coupon.csv', sql_querry)


def insert_coupon_redempt():  
    sql_querry = (
                '''
                INSERT INTO coupon_redempt (
                    household_key,
                    day,
                    coupon_upc,
                    campaign
                )
                VALUES (%s, %s, %s, %s               
                )
                ON CONFLICT (household_key, coupon_upc)
                DO NOTHING
                '''
                )
    insert_data(r'datasets/coupon_redempt.csv', sql_querry)


def insert_hh_demographic():  
    sql_querry = (
                '''
                INSERT INTO hh_demographic (
                    classification_1,
                    classification_2,
                    classification_3,
                    classification_4,
                    classification_5,
                    classification_6,
                    classification_7,
                    household_key
                )
                VALUES (%s, %s, %s, %s, 
                        %s, %s, %s, %s              
                )
                ON CONFLICT (household_key)
                DO NOTHING
                '''
                )
    insert_data(r'datasets/hh_demographic.csv', sql_querry)


def insert_product():  
    sql_querry = (
                '''
                INSERT INTO product (
                    product_id,
                    manufacturer,
                    department,
                    brand,
                    commodity_desc,
                    sub_commodity_desc,
                    curr_size_of_product
                )
                VALUES (%s, %s, %s, %s, 
                        %s, %s, %s                
                )
                ON CONFLICT (product_id)
                DO NOTHING
                '''
                )
    insert_data(r'datasets/product.csv', sql_querry)


def insert_causal_data():  
    sql_querry = (
                '''
                INSERT INTO causal_data (
                    product_id,
                    store_id,
                    week_no,
                    display,
                    mailer
                )
                VALUES (%s, %s, %s, %s, 
                        %s               
                )
                ON CONFLICT (product_id, store_id, week_no, display)
                DO NOTHING
                '''
                )
    insert_data(r'datasets/causal_data.csv', sql_querry)



if __name__ == '__main__':
    # insert_product()
    # insert_transaction_data()
    # insert_campaign_desc()
    # insert_campaign_table()
    insert_coupon()
    insert_coupon_redempt()
    insert_hh_demographic()
    insert_causal_data()
    
    