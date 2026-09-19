import os
import sys
from fb2_parser import parse_fb2

from vectors_bd import bd_pipeline, embedder, create_q_client
from db_search import search, answer_question, answ_print

from dotenv import load_dotenv

def main():
    load_dotenv()

    q_client = create_q_client()
    emb = embedder()
    question = sys.argv[1]
    top_k_points = search(q_client, 'Sherlock_books', emb, question)
    responcse = answer_question(question, top_k_points)
    answ_print(responcse)

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ошибка: ({type(exc).__name__}): {exc}")
