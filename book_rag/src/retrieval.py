
from qdrant_client import models

def retriever_search(qclient, bd_name, embedder, question, mode="embeddings", k=10):
    if len(question) == 0:
        raise ValueError("пустой вопрос")
    if mode not in ["bm25", "embeddings", "hybrid"]:
        raise ValueError("неправильный метод поиска чанков")
    if mode == 'bm25':
        vec_question = models.Document
        qclient.query_points(
            collection_name=bd_name,

        )


    if mode == 'embeddings':   
        vec_question = embedder.embed_query(question)

        response = qclient.query_points(
            collection_name=bd_name, 
            query=vec_question,
            limit=k,
            with_payload=True
        )
    return [{**point.payload, "score":point.score} for point in response.points]