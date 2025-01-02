import pdb
import datetime as dt

import numpy as np
import pandas as pd
import requests
import json
from config import *

from dateutil.relativedelta import relativedelta
from openai import OpenAI  #Langchain 안쓰고 직접 만들어봅시다. 

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


PAGE_SIZE = 100
TARGET_DATE ='2024-09-01'

def fetch_news_docs():
    print('Fetch news docs from open search server....... ')

    date_to = dt.datetime.fromisoformat(TARGET_DATE) + relativedelta(days = 1)

    query ={
        "query" : {
            "range":{
                "created_at": {
                    "gte" : TARGET_DATE,
                    "lt" : date_to.isoformat(),
                }
            }
        },
        "size" : PAGE_SIZE
    }
    
    for p in range(2):
        print(f'-page {p}')
        
        query['from'] = p*PAGE_SIZE
    

        resp = requests.get(
            url = f"{OPENSEARCH_URL}/news/_search",
            data = json.dumps(query),
            headers = OPENSEARCH_HEADERS,
            auth = OPENSEARCH_AUTH
        )

        # print(resp.status_code)
        
        results = json.loads(resp.content)
        hits = results['hits']['hits']

        # print(len(hits))


        if( len(hits) == 0):
            break 


        for x in hits:
            
            doc = {
                'doc_id' : x['_id'],
                **x['_source'], # 가을학기 때 했던 내용

            }

            if len(doc['body']) < 200:
                continue


            yield doc            # 가을학기 때 했던 내용
            
#Embedding  vector 만들기
def get_embedding_vectors(df):

    print()
    print('GET embedding vectors via OpenAI......... ')

    client = OpenAI(api_key='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')

    embeddings = []

    titles = df['title'].tolist()

    # 500개 까지만 embedding vector 만들어 주더라. 

    for i in range(0, len(df), PAGE_SIZE):
        print(f'- index{i}')
        
        resp = client.embeddings.create(
            model = "text-embedding-3-large",
            input = titles[i: i + PAGE_SIZE],


        )


        embeddings += [x.embedding for x in resp.data]

    embeddings = np.array(embeddings)
    # embeddings 행렬


    print(f" - Embedding shape : {embeddings.shape}")

    return embeddings


def cluster_news_topics(df, embeds):
    
    print()
    print("Cluster news articles into tpics...")

    ## 1) 기본 IDEA -> but, cluster 갯수를 모른다.
    # n_clusters = int(len(df) / 5)
    # clusterer = KMeans(n_clusters=n_clusters, n_init= 'auto')
    # cluster_labels = clusterer.fit_predict(embeds) # 기계는 vector를 본다.

    ## 2) 가장 좋은 cluster 찾아보기 
    # 정치는 중복이 많아 줄여도 괜찮다. 
    # 경제는 다양하다.. 클러스터링이 잘 안되긴 한다. 
    range_n_clusters = int(len(df) / 5) + np.arange(10) 


    best_silhoutte = -1
    best_clusterer = None

    for i in range(5):

        print(f"(Iteration # {i})")

        for n_clusters in range_n_clusters:
            clusterer = KMeans(n_clusters=n_clusters, n_init= 'auto')
            cluster_labels = clusterer.fit_predict(embeds) # 기계는 vector를 본다.

            silhoutte = silhouette_score(embeds, cluster_labels)

            print(f" - n_clusters : {n_clusters}, silhoutte: {silhoutte:.4f}")

            if silhoutte > best_silhoutte:
                best_silhoutte = silhoutte
                best_clusterer = clusterer



    print()
    print(f"* Best n_clusters: {best_clusterer.n_clusters}")

    similarities = []

    for i in df.index:
        x = best_clusterer.labels_[i]
        center = best_clusterer.cluster_centers_[x]
        sim = np.dot(embeds[i], center)

        similarities.append(sim)

    df['topic'] = best_clusterer.labels_
    df['similarity'] = similarities

    return df


def generate_topic_summary(df):
    print()
    print("Generating topic summaries......")

    client = OpenAI(api_key='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')

    df = df.sort_values('similarity', ascending = False)

    topics = df['topic'].drop_duplicates().tolist()

    for i in topics:
        chunk = df.loc[df['topic'] == i ]

        if len(chunk) <= 2:
            continue

        print(f"Topic {i} (docs: {len(chunk)})")

        print(f"Sources:")

        for _, x in chunk.iterrows():
            print(f"-{x['title']} ({x['publisher']})")

        doc = chunk.iloc[0]

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "다음 뉴스 기사를 500자 이내로 요약해줘."},
                {"role": "user", "content": doc['body']}
            ],
        )

        summary = resp.choices[0].message.content.strip()
        
        print("Summary : ")
        print(summary)

        resp = client.embeddings.create(
             model = "text-embedding-3-large",
             input = summary,

        )

        embed = resp.data[0].embedding

        topic_id = f"topic -{TARGET_DATE} - {i:04d}"
        body = {
            'date': TARGET_DATE,
            'title': doc['title'],
            'summary' : summary,
            'sources' : chunk['doc_id'].tolist(),
            'embed' : embed,
            'sources': chunk['doc_id'].tolist(),
            'no_resources' : len(chunk),

        }

        resp = requests.put(
            url = f"{OPENSEARCH_URL}/topics/_doc/{topic_id}",
            data = json.dumps(body),
            headers = OPENSEARCH_HEADERS,
            auth = OPENSEARCH_AUTH,
        )

        assert resp.status_code >= 200 and resp.status_code < 300

        print()
        

        
if __name__ == '__main__':

    docs = fetch_news_docs()
    #    print(docs) : 꺼내오기 전.. 

    df = pd.DataFrame(docs) 
    # print(df)

    embeds = get_embedding_vectors(df)

    df = cluster_news_topics(df, embeds)

    generate_topic_summary(df)

    print('** COMPLETEd!! ** ')
    