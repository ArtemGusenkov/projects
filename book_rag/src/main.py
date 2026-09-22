import os
import sys
from fb2_parser import parse_fb2

from vectors_bd import bd_pipeline, embedder, create_q_client
from retrieval import retriever_search
from answer_forming import answer_question, answ_print
from dotenv import load_dotenv

BD_NAME='Sherlock_books'

def main():
    load_dotenv()

    q_client = create_q_client()
    emb = embedder()
    args_in = sys.argv
    if len(args_in) == 2:
        question = args_in[1]
        top_k_points = retriever_search(q_client, BD_NAME, emb, question)
        responcse = answer_question(question, top_k_points)
        answ_print(responcse)
    elif len(args_in) == 3:
        mode = args_in[1]
        question = args_in[2]
        top_k_points = retriever_search(q_client, BD_NAME, emb, question, mode=mode)
        responcse = answer_question(question, top_k_points)
        answ_print(responcse)
    else:
        raise ValueError('неправильные входные данные')

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ошибка: ({type(exc).__name__}): {exc}")
