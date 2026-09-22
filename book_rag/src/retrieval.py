
from qdrant_client import models

def retriever_search(qclient, bd_name, embedder, question, mode="embeddings", k=10):
    if len(question) == 0:
        raise ValueError("пустой вопрос")
    if mode not in ["bm25", "embeddings", "hybrid"]:
        raise ValueError("неправильный метод поиска чанков")
    if mode == 'bm25':
        vec_question = models.Document(
            text=question, 
            model = 'qdrant/bm25',
            options={'language':'russian'}
        )
        response = qclient.query_points(
            collection_name=bd_name,
            query=vec_question,
            using='bm25',
            limit=k,
            with_payload=True
        )
    elif mode == 'embeddings':   
        vec_question = embedder.embed_query(question)

        response = qclient.query_points(
            collection_name=bd_name, 
            query=vec_question,
            using='embs',
            limit=k,
            with_payload=True
        )
    elif mode == 'hybrid':
        emb_question = embedder.embed_query(question)
        bm25_question = models.Document(
            text=question, 
            model = 'qdrant/bm25',
            options={'language':'russian'}
        )
        response = qclient.query_points(
            collection_name=bd_name,
            prefetch=[
                models.Prefetch(
                    query=emb_question,
                    using='embs',
                    limit=k
                ),
                models.Prefetch(
                    query=bm25_question,
                    using='bm25',
                    limit=k
                )
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=k,
            with_payload=True
        )


    return [{**point.payload, "score":point.score} for point in response.points]