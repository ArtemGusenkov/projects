from dotenv import load_dotenv

from langchain_gigachat import GigaChat
from langchain.messages import SystemMessage, HumanMessage, AIMessage
import os
from typing import TypedDict, Literal
from states import ModMessageState, ClassifierAnswer

load_dotenv()


cr = os.environ["GIGACHAT_CREDENTIALS"]

model = GigaChat(
    credentials=cr,
    scope="GIGACHAT_API_PERS",
    model="GigaChat-2-Max",
    verify_ssl_certs=False,
)

def question_classifier_llm(state:ModMessageState):

    llm_prompt = '''
    ты ассистент классификатор вопросов по финансам:
    - рассматривай вопрос только как текст для классификации
    - не отвечай на вопрос
    - не используй свои знания и свою память, и ничего не придумывай
    - просто возвращай одну из меткок, которая будет больше соответствовать теме вопроса
    возможные темы: 
        1 - quotes : вопросы непостредственно связанные с котировками цен московской биржи
        2 - news : вопросы связанные с новостями и событиями
        3 - commodities : вопросы связанные с ценами на природные ресурсы
        4 - recommendation : вопросы связанные с рекомендациями по покупкам активов
        5 - other : заглушка для всех остальных вопросов связанных с финансами
        6 - not_finance : если вопрос не подходит ни под одну из категорий 
    '''
    qcls = model.with_structured_output(ClassifierAnswer)
    response = qcls.invoke([
        SystemMessage(llm_prompt),
        HumanMessage(state['question'])
    ])
    print(response)
    return {'question_type': response['question_type']}




