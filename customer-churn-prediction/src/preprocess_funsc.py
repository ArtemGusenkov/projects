


def drop_nan_cols(df, alpha=0.5):
    '''
    дропает колонки в которых доля пропущенных значений > alpha
    '''
    alpha_count = df.shape[0] * alpha
    cols = df.isna().sum()[df.isna().sum() > alpha_count].index
    cols = list(cols)
    dfc = df.drop(columns=cols)
    return dfc


def feature_engineering(df):
    dfc = df.copy()
    all_cols = dfc.columns
    prod_cnt_cols = [i for i in all_cols if i.startswith('CR_PROD_CNT_')]
    dfc['total_products'] = dfc[prod_cnt_cols].sum(axis=1)
    return dfc