from pydantic import BaseModel

from dotenv import load_dotenv
import random

from langchain.chat_models import init_chat_model
from langchain_openrouter import ChatOpenRouter
from langchain.messages import HumanMessage, SystemMessage

from vectors_bd import create_q_client

COLLECTION_NAME='Sherlock_books'

def random_chunks(n=100):
    chunks_list = []
    chunks_ids_set = set()
    qclient = create_q_client()
    n_chunks = qclient.count(collection_name=COLLECTION_NAME, exact=True).count
    ids_chinks = [random.randint(0, n_chunks) for _ in range(n)]
    for i in ids_chinks:
        if i not in chunks_ids_set:
            chunks_ids_set.add(i)
            pload = qclient.retrieve(collection_name=COLLECTION_NAME, ids=[i], with_payload=True)[0].payload
            chunks_list.append(pload)
    return chunks_list


def llm_question_generation(chunks_list):
    load_dotenv()

    class GeneratedQuestions(BaseModel):
        question: str
        chunk_answer: str
        chunk_id: int
        chunk_chapter: str
        chunk_title: str

    prompt = '''
    - на вход ты получаешь текст чанка
    - на основе текста чанка ты составляешь вопрос, так чтобы ответ можно было найэти в этом фрагменте
    - для генерации вопроса можешь использовать только переданный фрагмент текста
    - придуманный вопрос должен полностью основываться на переданном фрагменте
    - вопрос должены быть понятен без прочтения фрагмента
    - не составляй вопросы в виде "... в этом фрагменте ...?", вопрос должен быть самодостаточным и понятным 
    - не используй свою память, ничего не придумывай и ничего не добавляй
    '''

    llm = init_chat_model(model='openrouter:openai/gpt-5-nano')

    output = []

    for chunk_dict in chunks_list:
        response = llm.invoke([SystemMessage(prompt), HumanMessage(chunk_dict['text'])])
        res = GeneratedQuestions(
            question=response.content,
            chunk_answer=chunk_dict['text'],
            chunk_id=chunk_dict['chunk_id'], 
            chunk_chapter=chunk_dict['chapter'],
            chunk_title=chunk_dict['title']
        )
        output.append(res.model_dump_json(ensure_ascii=False))
    return output


def save_2_json(data_list):
    with open(r'../eval_dataset/golden_dataset.jsonl', 'w', encoding='utf-8') as f:
        for row in data_list:
            f.write(row+'\n')


def create_golden_dataset(n=100):
    chunk_list = random_chunks(n=n)
    resp = llm_question_generation(chunk_list)
    save_2_json(resp)