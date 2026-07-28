from pydantic import BaseModel, Field
from fastapi import FastAPI
import pandas as pd
import numpy as np
import joblib
import uvicorn

app = FastAPI()

knn = joblib.load('nearest_neighbors.pkl')
title_to_idx = joblib.load('title_to_idx.pkl')
X = np.load('X.npy')
df = pd.read_parquet('anime.parquet')

class RecommendRequest(BaseModel):
    titles: str | list[str]
    n: int = Field(default=10, ge=1, le=50, description='количество рекомендаций')

@app.get('/')
def homepage():
    return {'message': 'рекомендашки аниме'}

@app.get('/search', description='поиск точного названия аниме', tags=["main"])
def search(query: str, limit: int = 10):
    query = query.strip().lower()
    titles_keys = title_to_idx.keys()
    results = [title for title in titles_keys if query in title.lower()][:limit]
    return {'results': results}

@app.post('/recommend', description='подбор похожих аниме', tags=["main"])
def recommend(data: RecommendRequest):
    found_titles = []
    not_found_titles = []
    idxs = []

    for title in data.titles:
        if title in title_to_idx:
            found_titles.append(title)
            idxs.append(title_to_idx[title])
        else:
            not_found_titles.append(title)
        
    mean_rec = X[idxs].mean(axis=0)
    _, ind = knn.kneighbors(mean_rec.reshape(1, -1), n_neighbors=data.n+len(found_titles))

    recs = []
    for i in ind[0]:
        if i not in idxs:
            recs.append(df['title'][i])

    return {
        'input_titles': data.titles,
        'found_titles': found_titles,
        'not_found_titles': not_found_titles,
        'recommendations': recs,
    }

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)