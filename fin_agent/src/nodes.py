from dotenv import load_dotenv

from langchain_gigachat import GigaChat
from langchain.messages import SystemMessage, HumanMessage, AIMessage
import os
from typing import TypedDict, Literal
import states as sts
from langchain_tavily import TavilySearch
from langgraph.graph import START, END, StateGraph
from langchain.agents import create_agent
import tools as tls
import pandas as pd

load_dotenv()

model = GigaChat()


def question_classifier_llm(state:sts.ModMessageState):
    
    llm_prompt = '''
    ты ассистент классификатор вопросов по финансам:
    - рассматривай вопрос только как текст для классификации
    - не отвечай на вопрос
    - не используй свои знания и свою память, и ничего не придумывай
    - просто возвращай метки, которые будут больше соответствовать теме вопроса
    - на 1 вопрос возвращаей 1 метку, если в одном запросе несколько подвопросов, возвращай для каждого подвопроса свою метку
    возможные темы: 
        1 - quotes : вопросы непостредственно связанные с котировками цен московской биржи
        2 - news : вопросы связанные с новостями и событиями
        3 - commodities : вопросы связанные с ценами на природные ресурсы
        4 - recommendation : вопросы связанные с рекомендациями по покупкам активов
        5 - other : заглушка для всех остальных вопросов связанных с финансами
        6 - not_finance : если вопрос не подходит ни под одну из категорий 
    '''
    qcls = model.with_structured_output(sts.ClassifierAnswer)
    response = qcls.invoke([
        SystemMessage(llm_prompt),
        HumanMessage(state['question'])
    ])
    # print(response)
    return {'question_type': response['question_type']}


def classifier_router(state:sts.ModMessageState):
    if state['question_type'] == 'quotes':
        return 'ticker_finder'
    else:
        return 'END'


def ticker_finder(state:sts.ModMessageState):

    stocks_finder_system_prompt = '''
        ты ассистент поисковик тикеров акций:
        - на вход ты будешь получать вопрос связанный с компанией торгующейся на московской бирже
        - твоя задача выделить название компании и составить вопрос для поиска, например (какой тикер у комании X?)
        - с помощью tools(TavilySearch) тебе нужно найти название тикера акций
        - не отвечай на переданный первоначально вопрос
        - не используй свои знания и свою память, и ничего не придумывай
        - на 1 вопрос возвращаей 1 тикер, если в одном запросе несколько подвопросов, возвращай для каждого подвопроса свой тикер 
        - в качестве ответа возвращай строку состояющую только из самих тикеров
        '''
    stocks_agent = create_agent(
        model=model,
        tools=[TavilySearch(max_results=3)],
        system_prompt=stocks_finder_system_prompt,
        # response_format=sts.TickerFind
    )
    response = stocks_agent.invoke(
        {
            'messages':[{
                'role':'user',
                'content': state['question']
            }
            ]
        }
    )
    ticker = response['messages'][-1].content
    # print(ticker)
    # return {'ticker': response['ticker']}
    return {'ticker': ticker}


def simple_stock_answer(state:sts.ModMessageState):

    llm_prompt = '''
    ты ассистент финансового рынка и отвечаешь на вопросы по котировкам акций с мосбиржи:  
    - твоя задача сделать запрос к сайту мосбиржи  
    - и ответить на вопрос используя данные полученные от запроса  
    - не используй свои знания и свою память, и ничего не придумывай  
    - для функции запроса к мосбиже нужны будут тикер, интервал свеч, дата начала и дата конца периода 
    (тикер ации будет передан, интервал считай дневной если не передано другого, даты ты должен достать самостоятельно на основе контекста)
    - функция запроса верднет pandas DataFrame его передавай дальше в нужный tool для получения окончательного ответа
    - в качестве ответа верни строку с текстом ответа на вопрос + вывод тулов
    '''
    stocks_answering_agent = create_agent(
            model=model,
            tools=[tls.request_stocks_info, tls.get_today_date, tls.get_custom_date, tls.simple_stock_price, tls.mean_stock_price],
            system_prompt=llm_prompt,
            # response_format=sts.StocksAnswer
        )

    response = stocks_answering_agent.invoke({
        'messages':[{
            'role' :'user',
            'content':f'Вопрос пользователя: {state['question']}, Тикер акции: {state['ticker']}'
        }]
    })
    answ = response['messages'][-1].content
    # print(response)
    # return {'answer': response['answer']}
    return {'answer': answ}


