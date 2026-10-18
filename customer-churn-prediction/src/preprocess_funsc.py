import re

import category_encoders as ce
import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_data(file_path):
    df = pd.read_csv(file_path)
    y = df['TARGET']
    df = df.drop(columns=['TARGET', 'ID', 'APP_EMP_TYPE', 'CLNT_JOB_POSITION_TYPE'])
    return df, y


def simple_nan_inputer(X_train, X_test, y_train, cat_imputer=None, cat_encoder=None, num_imputer=None, num_scaler=None):
    if cat_imputer is None:
        cat_imputer = SimpleImputer(strategy='most_frequent')
    if cat_encoder is None:
            cat_encoder = ce.BaseNEncoder()
    if num_imputer is None:
            num_imputer = SimpleImputer(strategy='median')
    if num_scaler is None:
            num_scaler = StandardScaler()
    
    cat_pipline = Pipeline([
        ('cat_imputer', cat_imputer),
        ('cat_encoder', cat_encoder),
    ])

    num_pipline = Pipeline([
        ('num_imputer', num_imputer),
        ('num_scaler', num_scaler),
    ])

    prep = ColumnTransformer(
        transformers=[
            ('num', num_pipline, make_column_selector(dtype_include=['number'])),
            ('cat', cat_pipline, make_column_selector(dtype_include=['str']))
        ],
        verbose_feature_names_out=False,
    ).set_output(transform='pandas')

    X_train_new = prep.fit_transform(X_train, y_train)
    X_test_new = prep.transform(X_test)
    return X_train_new, X_test_new


def feat_plot(lr, lgbm):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    top_n = 20

    lr_sort = np.argsort(abs(lr.coef_[0]))[-top_n:]
    lr_x = lr.feature_names_in_[lr_sort]
    lr_y = abs(lr.coef_[0])[lr_sort]
    ax[0].bar(x=lr_x, height=lr_y)
    ax[0].set_xticks(ticks=range(len(lr_x)), labels=lr_x, rotation=90)
    ax[0].set_title('коэффициенты лог.регрессии')

    lgbm_sort = np.argsort(lgbm.feature_importances_)[-top_n:]
    lgbm_x = lgbm.feature_names_in_[lgbm_sort]
    lgbm_y = lgbm.feature_importances_[lgbm_sort]
    ax[1].bar(x=lgbm_x, height=lgbm_y)
    ax[1].set_xticks(ticks=range(len(lgbm_x)), labels=lgbm_x, rotation=90)
    ax[1].set_title('важность фичей из lgbm')

    plt.tight_layout()
    plt.show()


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

def add_na_ind_num_cols(df):
    dfc = df.copy()
    new_df = pd.DataFrame()
    num_cols = dfc.select_dtypes(['number']).columns.to_list()
    for i in num_cols:
        if dfc[i].isna().sum() > 0:
            new_df[f'na_{i}'] = dfc[i].isna().astype('int')
    return new_df


class preprocessing:
    '''
    бинарные фичи кодируются как (1) и (-1) с заменой пропусков на (0) \n
    фичи только с пропусками и одним значением удаляются \n
    колоки APP_EDUCATION и APP_MARITAL_STATUS приводятся к нижнему регистру \n
    в колонке с доверенными лицами варианты кодируются с русског яз. на англ. \n
    + обработка  названий профессий
    '''
    def __init__(self, cat_ecnoder=None, num_imputer=None, num_scaler=None, add_na_ind=False):
        if cat_ecnoder is None:
            self.cat_ecnoder = ce.BinaryEncoder()
        else:    
            self.cat_ecnoder = cat_ecnoder

        if num_imputer is None:
            self.num_imputer = SimpleImputer(strategy='median')
        else:
            self.num_imputer = num_imputer

        if num_scaler is None:
            self.num_scaler = StandardScaler()
        else:
            self.num_scaler = num_scaler
        self.cat_cols = []
        self.num_cols = []

        self.add_na_ind = add_na_ind

        self.relatives_dict = {'сын':'son', 'близкий ро':'relative', 'друг':'friend',
                    'отец': 'father', 'сестра': 'sister', 'мать': 'mother', 
                    'муж': 'husband', 'брат': 'brother', 'дальний ро': 'relative', 
                    'дочь': 'daughter', 'жена':'wife'}


    def fit(self, df_in):
        df = df_in.copy()
        self.cat_cols = df.select_dtypes(['string']).columns.to_list()
        self.num_cols = df.select_dtypes(['number']).columns.to_list()

        bin_cols = ['APP_CAR', 'APP_DRIVING_LICENSE', 'APP_TRAVEL_PASS']
        self.df_bin_cols = [i for i in self.cat_cols if i in bin_cols]

        long_cat = ['APP_EDUCATION', 'APP_MARITAL_STATUS']
        self.df_long_cat = [i for i in self.cat_cols if i in long_cat]

        smt_cat = ['APP_KIND_OF_PROP_HABITATION', 'APP_POSITION_TYPE', 'APP_COMP_TYPE']
        self.smt_cat = [i for i in self.cat_cols if i in smt_cat]

        self.cols_w_2_vals = []
        for i in df.columns:
            if len(df[i].unique())==2: 
                self.cols_w_2_vals.append(i) 
                if i in self.num_cols:
                    self.cat_cols.append(i)
                    self.num_cols.remove(i)
        df[self.cols_w_2_vals] = df[self.cols_w_2_vals].astype('str')                      

        if self.cat_cols:
            df[self.cat_cols] = df[self.cat_cols].fillna('missing')
            self.cat_ecnoder.fit(df[self.cat_cols])
        if self.num_cols:
            df[self.num_cols] = self.num_imputer.fit_transform(df[self.num_cols])
            self.num_scaler.fit(df[self.num_cols])

        

    def transform(self, df):
        dfc = df.copy()
        if self.df_bin_cols:
            dfc[self.df_bin_cols] = dfc[self.df_bin_cols].replace({'Y':1, 'N':-1})
            dfc[self.df_bin_cols] = dfc[self.df_bin_cols].fillna(0)

        if self.df_long_cat:
            for i in self.df_long_cat:
                dfc[i] = dfc[i].str.lower()

        if self.cols_w_2_vals:
            # dfc = dfc.drop(columns=self.cols_w_2_vals)
            for i in self.cols_w_2_vals:
                dfc[i] = dfc[i].astype('str')

        if self.smt_cat:
            for i in self.smt_cat:
                dfc[i] = dfc[i].fillna('missing')

        if 'CLNT_TRUST_RELATION' in self.cat_cols:
            dfc['CLNT_TRUST_RELATION'] = dfc['CLNT_TRUST_RELATION'].replace(self.relatives_dict)

        if 'CLNT_JOB_POSITION' in self.cat_cols:
            dfc['CLNT_JOB_POSITION'] = dfc['CLNT_JOB_POSITION'][dfc['CLNT_JOB_POSITION'].notna()].apply(clean_text)
            dfc = normalize_job_names(dfc)

        if self.add_na_ind:
            dfc_na_cols = add_na_ind_num_cols(dfc)

        dfc[self.num_cols] = self.num_imputer.transform(dfc[self.num_cols])
        dfc[self.num_cols] = self.num_scaler.transform(dfc[self.num_cols])

        dfc[self.cat_cols] = dfc[self.cat_cols].fillna('missing')
        dfc_cat = self.cat_ecnoder.transform(dfc[self.cat_cols])
        dfc = pd.concat((dfc[self.num_cols], dfc_cat), axis=1)
        if self.add_na_ind:
            dfc = pd.concat((dfc, dfc_na_cols), axis=1)
        
        return dfc



def feature_engineering(df):
    dfc = df.copy()
    all_cols = dfc.columns
    prod_cnt_cols = [i for i in all_cols if i.startswith('CR_PROD_CNT_')]
    dfc['total_products'] = dfc[prod_cnt_cols].sum(axis=1)

    dfc['prod_rest_avg_cur_2_rest_dyn_cur'] = dfc['REST_AVG_CUR'] * dfc['REST_DYNAMIC_CUR_1M']
    dfc['prod_rest_avg_paym_2_rest_dyn_paym'] = dfc['REST_AVG_PAYM'] * dfc['REST_DYNAMIC_PAYM_1M']

    dfc['dif_rest_dyn_cur_1m_3m'] = dfc['REST_DYNAMIC_CUR_1M'] - dfc['REST_DYNAMIC_CUR_3M']
    dfc['dif_rest_dyn_paym_1m_3m'] = dfc['REST_DYNAMIC_PAYM_1M'] - dfc['REST_DYNAMIC_PAYM_3M']
    dfc['dif_dyn_paym_1m_turn_rest'] = dfc['TURNOVER_DYNAMIC_PAYM_1M'] - dfc['REST_DYNAMIC_PAYM_1M']
    
    dfc['prod_rest_avg_cur_2_rest_dyn_cur'] = dfc['SUM_TRAN_ATM_TENDENCY1M'] / (dfc['TURNOVER_DYNAMIC_CUR_1M'] + 1e-9)

    dfc['prod_rest_avg_cur_2_rest_dyn_cur'] = dfc['REST_AVG_CUR'] * dfc['REST_DYNAMIC_CUR_1M']
    dfc['prod_rest_avg_cur_2_rest_dyn_cur'] = dfc['REST_AVG_CUR'] * dfc['REST_DYNAMIC_CUR_1M']
    return dfc


def model_scores(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)
    accuracy_sc = accuracy_score(y_test, y_pred) 
    recall_sc = recall_score(y_test, y_pred)
    rocauc = roc_auc_score(y_test, y_proba[:, 1])

    print('Accuracy:', accuracy_sc)
    print('Recall:', recall_sc)
    print('ROC AUC:', rocauc)
    return accuracy_sc, recall_sc, rocauc


def models_scores(lr, lgbm, X_train_1, X_test_1, y_train, y_test, name_1, name_2, result_table):
    print('Log. Reg:')
    accuracy_sc, recall_sc, rocauc = model_scores(lr, X_train_1, X_test_1, y_train, y_test)
    result_table.loc[len(result_table), :] = {'model': name_1, 
                                            'accuracy':round(accuracy_sc, 3), 
                                            'recall':round(recall_sc, 3),
                                            'ROC AUC':round(rocauc, 3)}
    print('LGBM:')
    accuracy_sc, recall_sc, rocauc = model_scores(lgbm, X_train_1, X_test_1, y_train, y_test)
    result_table.loc[len(result_table), :] = {'model': name_2, 
                                            'accuracy':round(accuracy_sc, 3), 
                                            'recall':round(recall_sc, 3),
                                            'ROC AUC':round(rocauc, 3)}