from vectors_bd import bd_pipeline, embedder, create_q_client
from retrieval import retriever_search
from answer_forming import answer_question, answ_print
from dotenv import load_dotenv
import json
import pandas as pd

BD_NAME='Sherlock_books'

def retrieval_metrics(answer_ids, retrieved_ids, k=5):
    if type(answer_ids) == int:
        answer_ids = [answer_ids]
    if retrieved_ids == []:
        return {'recall@k':None, 'precision@k':None, 'hit@k':None, 'mean_reciprocal_rank':None}
    if k > len(retrieved_ids):
        k = len(retrieved_ids)
    retrieved_ids = retrieved_ids[:k]
    union_lists = [id for id in retrieved_ids if id in answer_ids]
    recall = len(union_lists) / len(answer_ids)
    precision = len(union_lists) / k
    hit_rate = (1 if union_lists!=[] else 0)
    if union_lists != []:
        for rank, id in enumerate(retrieved_ids, 1):
            if id in answer_ids:
                mrr = 1 / rank
    else:
        mrr = None
    return {
        f'recall@{k}': recall,
        f'precision@{k}': precision,
        f'hit@{k}': hit_rate,
        f'mean_reciprocal_rank': mrr
    }

def eval_retriever(k=5):
    load_dotenv()

    q_client = create_q_client()
    emb = embedder()

    with open(r'../eval_dataset/golden_dataset.jsonl', 'r', encoding='utf-8') as file:
        df = pd.DataFrame(columns=[f'recall@{k}', f'precision@{k}', f'hit@{k}', 'mean_reciprocal_rank'])
        for row in file.readlines():
            row_dict = json.loads(row)
            question = row_dict['question'] 
            answ_ids = row_dict['chunk_id']
            top_k_points = retriever_search(q_client, BD_NAME, emb, question)
            retrieved_ids = [point['chunk_id'] for point in top_k_points]
            metrics = retrieval_metrics(answ_ids, retrieved_ids, k=k)
            df.loc[len(df), :] = metrics
        mean_metrics = df.mean(axis=0)
        with open(r'../eval_result/eval_result.txt', 'w') as f:
            for metric in mean_metrics.index:
                f.writelines(f'{metric}: {mean_metrics[metric]*100:.2f} %\n')

if __name__ == '__main__':
    eval_retriever()