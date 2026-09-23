import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient, models

from fb2_parser import parse_fb2

TEXTS_LOCATION = r'../texts/'

def make_chunks(data, size=1000, overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size, chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return [
        {**record, "text": text}
        for record in data
        for text in splitter.split_text(record["text"])
    ]

def embedder():
    embeddings = OpenAIEmbeddings(
        model="openai/text-embedding-3-small", 
        api_key=os.environ["OPENROUTER_API_KEY"], 
        base_url="https://openrouter.ai/api/v1",
        check_embedding_ctx_length=False,
        request_timeout=5,
        max_retries=2)
    return embeddings


def create_q_client():
    q_client = QdrantClient(url='http://localhost:6333')
    return q_client

def create_bd(q_client, bd_name, vec_size=1536):
    if not q_client.collection_exists(bd_name):
        q_client.create_collection(
            bd_name, 
            vectors_config={'embs': models.VectorParams(
                size=vec_size, 
                distance=models.Distance.COSINE,
            )},
            sparse_vectors_config={'bm25': models.SparseVectorParams(
                modifier=models.Modifier.IDF
            )}
        )

def load_vecs(q_client, bd_name, chunks, emb):
    ids = [i for i in range(len(chunks))]
    batch_size = 16
    if q_client.collection_exists(bd_name):
        for i in range(0, len(chunks), batch_size):
            batch = list(zip(ids[i:i+batch_size], chunks[i:i+batch_size]))
            vecs = emb.embed_documents([
                f'{c['chapter']}\n\n{c['text']}' for _,c in batch
            ])
            q_client.upsert(
                collection_name=bd_name,
                wait=True,
                points=[
                    models.PointStruct(
                        id=id,
                        vector={
                            'embs' : vector,
                            'bm25' : models.Document(
                                text = chunk['text'],
                                model='qdrant/bm25',
                                options={"language": "russian"}
                            )
                        },
                        payload={
                            **chunk,
                            'chunk_id' : id
                        }
                    )
                    for (id, chunk), vector in zip(batch, vecs)
                ]
            )

def bd_pipeline():
    load_dotenv()
    all_books = []
    for book in os.listdir(TEXTS_LOCATION):
        output = parse_fb2(TEXTS_LOCATION + book)
        all_books.extend(output)

    all_chunks = make_chunks(all_books)
    q_client = create_q_client()
    create_bd(q_client, 'Sherlock_books')
    embeddings = embedder()
    load_vecs(q_client, 'Sherlock_books', all_chunks, embeddings)
    q_client.close()

if __name__ == '__main__':
    try:
        bd_pipeline()
    except Exception as exc:
        print(f'ошибка: {exc}')