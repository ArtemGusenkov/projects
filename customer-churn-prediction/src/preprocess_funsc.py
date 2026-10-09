import pandas as pd
import re


def load_data(file_path):
    df = pd.read_csv(file_path)
    y = df['TARGET']
    df = df.drop(columns=['TARGET', 'ID'])
    return df, y


def drop_nan_cols(df, alpha=0.5):
    '''
    дропает колонки в которых доля пропущенных значений > alpha
    '''
    alpha_count = df.shape[0] * alpha
    cols = df.isna().sum()[df.isna().sum() > alpha_count].index
    cols = list(cols)
    dfc = df.drop(columns=cols)
    return dfc


def clean_text(text_i):
    text_i = str(text_i)
    text_i = text_i.strip()
    text_i = re.sub('ё', 'е', text_i)
    text_i = re.sub('/d+', '', text_i)
    return text_i

def normalize_job_names(dfc):
    col = 'CLNT_JOB_POSITION'
    dfc[col] = dfc[col].str.lower()

    cond_3 = dfc[col].str.contains('зам')
    dfc.loc[cond_3, col] = 'заместитель'
    
    cond_1 = dfc[col].str.contains('нач')
    dfc.loc[cond_1, col] = 'начальник'

    cond_2 = dfc[col].str.contains('директ')
    dfc.loc[cond_2, col] = 'директор'

    cond_4 = dfc[col].str.contains('пом')
    dfc.loc[cond_4, col] = 'помощник'

    cond_5 = dfc[col].str.contains('менед')
    dfc.loc[cond_5, col] = 'менеджер'

    cond_5 = dfc[col].str.contains('руков')
    dfc.loc[cond_5, col] = 'руководитель'

    cond_5 = dfc[col].str.contains('инж')
    dfc.loc[cond_5, col] = 'инженер'

    return dfc


def process_nan(df):
    '''
    бинарные фичи кодируются как (1) и (-1) с заменой пропусков на (0)
    фичи только с пропусками и одним значением удаляются 
    колоки APP_EDUCATION и APP_MARITAL_STATUS приводятся к нижнему регистру
    в колонке с доверенными лицами варианты кодируются с русског яз. на англ.
    +сырая названий профессий
    '''
    dfc = df.copy()
    bin_cols = ['APP_CAR', 'APP_DRIVING_LICENSE', 'APP_TRAVEL_PASS']
    dfc[bin_cols] = dfc[bin_cols].replace({'Y':1, 'N':-1})
    dfc[bin_cols] = dfc[bin_cols].fillna(0)

    cols_w_2_vals = []
    for i in df.columns:
        if len(df[i].unique())==2: 
            cols_w_2_vals.append(i) 
    dfc = dfc.drop(columns=cols_w_2_vals)

    long_cat = ['APP_EDUCATION', 'APP_MARITAL_STATUS']
    for i in long_cat:
        dfc[i] = dfc[i].str.lower()

    relatives_dict = {'сын':'son', 'близкий ро':'relative', 'друг':'friend',
                      'отец': 'father', 'сестра': 'sister', 'мать': 'mother', 
                      'муж': 'husband', 'брат': 'brother', 'дальний ро': 'relative', 
                      'дочь': 'daughter', 'жена':'wife'}
    dfc['CLNT_TRUST_RELATION'] = dfc['CLNT_TRUST_RELATION'].replace(relatives_dict)

    # cat_cols = df.select_dtypes(['string']).columns.to_list()

    dfc['CLNT_JOB_POSITION'] = dfc['CLNT_JOB_POSITION'][dfc['CLNT_JOB_POSITION'].notna()].apply(clean_text)
    dfc = normalize_job_names(dfc)

    duble_cols = ['CLNT_JOB_POSITION_TYPE', 'APP_EMP_TYPE']
    dfc = dfc.drop(columns=duble_cols)

    return dfc


def feature_engineering(df):
    dfc = df.copy()
    all_cols = dfc.columns
    prod_cnt_cols = [i for i in all_cols if i.startswith('CR_PROD_CNT_')]
    dfc['total_products'] = dfc[prod_cnt_cols].sum(axis=1)
    return dfc