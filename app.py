from flask import Flask, request, Response
import json

import jieba
import jieba.analyse

from elasticsearch import Elasticsearch

es = Elasticsearch(
    ['192.168.1.29'],
    port=9200
)

app = Flask(__name__, static_url_path='')

def get_context(query, es):
    tagList = jieba.analyse.extract_tags(query, topK = 8)
    doc = {
        "query": {
        "function_score": {
            "query":{
            "dis_max": {
            "queries": [
                { "match": { "query": {"query":query,"boost":2.5}}},
                { "match": { "answer": {"query":','.join(tagList),"boost":2}}},
                { "match": { "query_tag": {"query":query}}},
                { "match": { "answer_tag": {"query":','.join(tagList)}}},
            ],
                "tie_breaker": 0.4
            }},
            "score_mode": "sum",
            "boost_mode": "multiply"}
    }}

    results = es.search(index='0616', doc_type='_doc', body=doc, size=1)['hits']['hits']
    context = []
    for res in results:
        context.append(res['_source']['answer'])
    return context[0]

@app.route("/api")
def model_1():
    query = request.args.get('text', '')
    print(query)
    context = get_context(query, es)
    return Response(json.dumps({'status':"ok", 'message':context, 'query':query},ensure_ascii=False), mimetype="application/json")

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1234, debug=True)
