import jieba
import jieba.analyse
from elasticsearch import Elasticsearch
from elasticsearch import helpers


class ElasticObj:
    def __init__(self, index_name, index_type, passage_path, ip ="192.168.1.29"):
        '''
        :param index_name: 索引名称
        :param index_type: 索引类型
        :passage_path: 文章路径
        '''
        self.index_name =index_name
        self.index_type = index_type
        self.passage_path = passage_path
        self.es = Elasticsearch([ip])


    def create_index(self,index_name,index_type):
        '''
        创建索引,创建索引名称为ott，类型为ott_type的索引
        :param ex: Elasticsearch对象
        :return:
        '''
        #创建映射
        _index_mappings ={
                       "mappings":{
                          "properties":{
                             "query": {
                                  "type": "text",
                                  "analyzer": "ik_max_word",
                                  "search_analyzer":"ik_smart"
                                },
                             "answer": {
                                  "type": "text",
                                  "analyzer": "ik_max_word",
                                  "search_analyzer":"ik_smart"
                                },
                             "query_tag":{
                                "type":"text",
                                "analyzer":"ik_max_word",
                                "search_analyzer":"ik_smart"
                             },
                             "answer_tag":{
                                "type":"text",
                                "analyzer":"ik_max_word",
                                "search_analyzer":"ik_smart"
                             }
                          }
                       }
        }
        if self.es.indices.exists(index=self.index_name) is not True:
            res = self.es.indices.create(index=self.index_name, body=_index_mappings)
            print(res)

    def bulk_Index_Data(self):
        ACTIONS = []
        with open(self.passage_path) as f: 
            for line in f:
                lineList = line.strip().split("\t")
                q = lineList[0]
                a = lineList[1]
                q_tag = jieba.analyse.extract_tags(q, topK = 10)
                a_tag = jieba.analyse.extract_tags(a, topK = 10)
                action = {
                    "_index": self.index_name,
                    "_type": self.index_type,
                    "_source": {
                        "query": q,
                        "answer": a,
                        "query_tag": q_tag,
                        "answer_tag": a_tag,
                    }
                }
                ACTIONS.append(action)
        print(len(ACTIONS))
        success, _ = helpers.bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)
        print('Performed %d actions' % success)


if __name__ == '__main__':
    
    ip = "192.168.1.29"
    index_name = "0616"
    index_type = "_doc"
    obj = ElasticObj(index_name, index_type, ip=ip, passage_path='faq.txt')
    obj.create_index(index_name, index_type)
    obj.bulk_Index_Data()