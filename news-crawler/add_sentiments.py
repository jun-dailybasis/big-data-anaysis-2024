import pdb
import json
import requests
import pandas as pd

from config import *
from transformers import pipeline

def fetch_missing_sentiments():

    query = {
            "query":{
                "bool":{
                "must_not": [
                    {
                        "exists": {
                        "field": "sentiment"
                        }
                    }
                    ]
                }
            }
        }
    
    query = json.dumps(query)

    resp = requests.get(
        f"{OPENSEARCH_URL}/news/_search",
        headers = OPENSEARCH_HEADERS,
        data = query,
        auth = OPENSEARCH_AUTH
    )

    # print(resp)

    assert resp.status_code == 200 # 안정장치 #assert 뒤에 있는 조건이 아니면 에러 던지고 던져라. 

    results = resp.json()

    hits = results['hits']['hits']

    docs = [{'id': x['_id'], **x['_source']} for x in hits]

    if len(docs) == 0:
        return pd.DataFrame() # 마지막에서 에러가 날거다

    df = pd.DataFrame(docs)
    df = df[['id','title']]## 대괄호로 뽑기. 

    return df


def upload_to_server(df):
    # iterrows: iterate over rows
    for idx, row in df.iterrows():

        body = {
            "doc" : {
                "sentiment" : row['label']
            }
        }

        body = json.dumps(body)

        resp = requests.post(
            f"{OPENSEARCH_URL}/news/_update/{row['id']}", #_doc 기존 지우고 새로 넣어라. update는 기존에다가 추가해. 
            headers = OPENSEARCH_HEADERS,
            data = body, 
            auth = OPENSEARCH_AUTH
        )

        assert resp.status_code == 200
        # pdb.set_trace()

        # pass

if __name__ == '__main__':
    classifier = pipeline('sentiment-analysis', model='snunlp/KR-FinBert-SC',  device ='mps') #mps: 맥 devide ='mps',
    #서울대. 경제 분석에 좋다. Finbert!

    while True:
        df = fetch_missing_sentiments() #안되는것만 골라줘. 그래서 괜찮아. 

        if df.empty:
            break

        titles = df['title'].tolist()
        sentiments = classifier(titles) # 쉽게 쓴다. 

        df_sents = pd.DataFrame(sentiments)
        df_sents = df_sents[['label']]

        df = df.join(df_sents)

        upload_to_server(df)
