"""连通性自检：对 Milvus 和 Elasticsearch 各跑一次写入 + 检索 + 清理。

    pip install "pymilvus>=2.6" "elasticsearch>=8,<9"
    python smoke_test.py
"""

import random

MILVUS_URI = "http://localhost:19530"
ES_URL = "http://localhost:9200"
DIM = 8


def rand_vec():
    return [random.random() for _ in range(DIM)]


def check_milvus():
    from pymilvus import MilvusClient

    client = MilvusClient(uri=MILVUS_URI)
    name = "smoke_test"

    if client.has_collection(name):
        client.drop_collection(name)
    # Milvus 默认一致性是 Bounded，插入后立刻检索会读不到；自检这里要 Strong
    client.create_collection(collection_name=name, dimension=DIM, consistency_level="Strong")

    rows = [{"id": i, "vector": rand_vec(), "text": f"doc-{i}"} for i in range(20)]
    client.insert(collection_name=name, data=rows)

    hits = client.search(
        collection_name=name,
        data=[rows[0]["vector"]],
        limit=3,
        output_fields=["text"],
    )
    client.drop_collection(name)

    print(f"Milvus   OK  {MILVUS_URI}  →  命中 {len(hits[0])} 条，Top1 = {hits[0][0]['entity']['text']}")


def check_elasticsearch():
    from elasticsearch import Elasticsearch

    es = Elasticsearch(ES_URL)
    index = "smoke-test"

    if es.indices.exists(index=index):
        es.indices.delete(index=index)
    es.indices.create(
        index=index,
        mappings={
            "properties": {
                "text": {"type": "text"},
                "vector": {"type": "dense_vector", "dims": DIM, "similarity": "cosine"},
            }
        },
    )

    for i in range(20):
        es.index(index=index, id=str(i), document={"text": f"doc-{i} langgraph", "vector": rand_vec()})
    es.indices.refresh(index=index)

    full_text = es.search(index=index, query={"match": {"text": "langgraph"}}, size=3)
    knn = es.search(index=index, knn={"field": "vector", "query_vector": rand_vec(), "k": 3, "num_candidates": 20})
    es.indices.delete(index=index)

    version = es.info()["version"]["number"]
    print(
        f"Elastic  OK  {ES_URL}  →  v{version}，"
        f"全文命中 {full_text['hits']['total']['value']} 条，kNN 命中 {len(knn['hits']['hits'])} 条"
    )


if __name__ == "__main__":
    failed = False
    for label, fn in (("Milvus", check_milvus), ("Elasticsearch", check_elasticsearch)):
        try:
            fn()
        except Exception as exc:  # noqa: BLE001 - 自检脚本，打印即可
            failed = True
            print(f"{label:<8} FAIL  {type(exc).__name__}: {exc}")
    raise SystemExit(1 if failed else 0)
