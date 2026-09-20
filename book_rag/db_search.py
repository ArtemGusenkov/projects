from vectors_bd import create_q_client
from pydantic import BaseModel, Field
from typing import Literal
from langchain_openrouter import ChatOpenRouter
from langchain.agents import create_agent
from dotenv import load_dotenv

class answer(BaseModel):
    decision: Literal['ответ найден', 'нет ответа']
    answer: str
    points: list[int] = Field(description='указывать тут только id чанков, которые подтверждают ответ')

def search(qclient, bd_name, embedder, question, k=10):
    if len(question) == 0:
        raise ValueError("пустой вопрос")

    vec_question = embedder.embed_query(question)

    response = qclient.query_points(
        collection_name=bd_name, 
        query=vec_question,
        limit=k,
        with_payload=True
    )
    return [{**point.payload, "score":point.score} for point in response.points]

def answer_question(question, points):
    load_dotenv()
    if len(points) == 0:
        return answer(decision='нет ответа', answer='ничего не нашлось', points=[])
    model_name = ChatOpenRouter(model='openai/gpt-4.1-mini', max_tokens=12000)
    agent = create_agent(model=model_name, response_format=answer, system_prompt='''
    ты услужливый библиотечный агент
    ты отвечаешь на вопросы по русскоязычным книгам о Шерлоке Холмсе
    в книге пишут Уотсон вместо распространенного Ватсон, учитывай это при ответе на вопросы
    ты можешь использовать факты только из найденых фрагментов
    ничего не придумывай и не добавляй сведений из своей памяти
    если фрагменты не подтверждают ответ на вопрос, укажи decision='нет ответа' и ответь что переданные фрагменты не помогают ответить на вопрос 
    для найденого ответа возвращай id чанков в points
    в ответе не печатай источники полностью, а кратко пересказывай с указанием id источника
    ''')
    result = agent.invoke({
        'messages':[
            {'role':'user', 'content':f'Вопрос: {question} \n Найденные отрывки: {points}'}
        ]
    })

    return result['structured_response']

def answ_print(answ):
    print('решение:',answ.decision)
    print('ответ:', answ.answer)
    if len(answ.points) != 0:
        print('источники: ')
        for i in answ.points:
            print('    chank_id:', i)




