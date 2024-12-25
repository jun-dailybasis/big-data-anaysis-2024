import json
import pdb
import requests
import pandas as pd
from config import * 

def query_news_trends(search):
    query = {
        "size": 0,
        "aggs": {
            "group_by_date": {
            "date_histogram": {
                "field": "created_at",
                "interval": "day"
        },
        }
    }
    }

    if search is not None:
        query['query'] = {
            "match" : {
                "title": search
            }

        }

    query = json.dumps(query)

    resp = requests.get(
        f"{OPENSEARCH_URL}/news/_search",
        headers = OPENSEARCH_HEADERS,
        data  = query,
        auth = OPENSEARCH_AUTH,
    )

    # print(resp)

    results = resp.json()
    # 빈도수
    buckets = buckets = results['aggregations']['group_by_date']['buckets']

    if len(buckets) == 0:
        return []
    
    df = pd.DataFrame(buckets)
    df['date'] = df['key_as_string'].str[:10]
    df = df[['date','doc_count']]

    return df.to_dict(orient = 'records')

def main(event, context):
    # params = event['queryStringParameters']
    params = event.get('queryStringParameters') #쿼리 스트링 없이 요청할 떄.. 위 줄은 에러, 이번 줄은 None으로 던져준다.

    if params:
        search = params.get('search')
    
    else:
        search = None

    trends = query_news_trends(search)

    body = {
        "message": f"News Trends: {search}",
        "trends": trends
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),

        # CORS
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        }

        
        }

    return response
