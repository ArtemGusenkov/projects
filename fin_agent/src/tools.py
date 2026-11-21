import requests
import pandas as pd
from langchain.tools import tool
from datetime import date, timedelta


def request_stocks_info(ticker: str, interval:int, start_date: str, end_date:str) -> pd.DataFrame:
    '''
    Функция для получения данных котировок акции с перезанным тикером   
    входные данные:  
        - ticker: тикер акции  
        - interval: интервал свеч (24 = 1 день, 7 = 1 неделя, 31 = 1 месяц)  
        - start_date: дата начала данных  
        - end_date: дата конца данных   
        формат дат: 'YYYY-MM-DD'
    выходные данные:
        pandas dataframe
    '''

    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json"

    params = {
            'from': start_date,
            'till': end_date,
            'interval': interval
        }
    response = requests.get(url, params=params)
    data = response.json()
    candles_data = data['candles']
    df = pd.DataFrame(candles_data['data'], columns=candles_data['columns'])
    numeric_cols = ['open', 'close', 'high', 'low', 'value', 'volume']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
    df['begin'] = pd.to_datetime(df['begin'])

    return df

@tool
def get_today_date():
    '''
    функция для получения даты текущего дня
    '''
    today = date.today().isoformat()
    print(str(today))
    return today


@tool
def get_custom_date(n_days):
    '''
    функция для получения даты отсчитывая несколько дней назад от текущей даты
    '''
    today = get_today_date()
    past_date = (today - timedelta(days=n_days)).isoformat()
    print(past_date)
    return past_date


@tool
def mean_stock_price(ticker, interval, start_date, end_date) -> str:
    '''
    простая средняя цена акции
    Рассчитать среднее арифметическое close полученных свечей
    Даты: YYYY-MM-DD. Интервал 24 соответствует дневным свечам
    '''
    df = request_stocks_info(ticker, interval, start_date, end_date)
    if df.empty:
        return "За указанный период свечи не найдены"
    
    # mean_price = df['close'].mean()
    return (
        f"Тикер: {ticker}. Среднее close полученных свечей: "
        f"{df['close'].mean():.2f}. Количество свечей: {len(df)}."
    )


@tool
def simple_stock_price(ticker: str, interval:int, start_date: str, end_date:str) -> str:
    '''
    простой вывод цены акции
    Получить close последней доступной свечи за указанный период
    Даты: YYYY-MM-DD. Интервал 24 соответствует дневным свечам
    Args:
        ticker: Тикер акции, например SBER.
        interval: Интервал свечей; 24 — дневные свечи (24 = 1 день, 7 = 1 неделя, 31 = 1 месяц)  
        start_date: Начальная дата в формате YYYY-MM-DD.
        end_date: Конечная дата в формате YYYY-MM-DD.
    '''
    print(f'{ticker}, {interval}, {start_date}, {end_date}')
    df = request_stocks_info(ticker, interval, start_date, end_date)
    if df.empty:
        return "За указанный период свечи не найдены"

    return (
        f'''Тикер: {ticker}. Начало последней полученной свечи: 
        {df['begin']}. Значение close: {df['close']}'''
    )