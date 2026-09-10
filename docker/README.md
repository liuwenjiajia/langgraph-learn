# 本地 Milvus + Elasticsearch

给 langgraph-learn 用的本地检索后端。**仅限本地开发**：两个服务都关闭了鉴权，别暴露到公网。

## 关于 "Milvus Lite"

Milvus Lite 是**进程内嵌入式**模式，不跑 Docker —— `pip install pymilvus` 之后
`MilvusClient("./milvus_demo.db")` 就直接落一个本地文件，没有服务端。

Docker 里对应的最轻量形态是 **Standalone + 内嵌 etcd + 本地存储**，也就是这里用的方案：
单个容器搞定，不需要额外的 etcd / MinIO 容器。SDK 用法和 Milvus Lite 完全一致，
只是把 URI 从文件路径换成 `http://localhost:19530`。

| | Milvus Lite | 本目录（Standalone 内嵌 etcd） | 完整 Standalone |
|---|---|---|---|
| 容器数 | 0 | 1 | 3（milvus + etcd + minio） |
| 连接方式 | `./xxx.db` | `http://localhost:19530` | `http://localhost:19530` |
| 适合 | 单机脚本、单测 | 本地开发、多进程共享 | 贴近生产 |

## 启动

```bash
cd docker
docker compose up -d
```

首次启动 Milvus 大约需要 1～2 分钟做初始化，等健康检查转成 `healthy` 再连：

```bash
docker compose ps
```

带 Web 控制台启动（Attu + Kibana）：

```bash
docker compose --profile ui up -d
```

## 端口

| 服务 | 地址 | 说明 |
|---|---|---|
| Milvus gRPC | `localhost:19530` | SDK 连接用 |
| Milvus WebUI | http://localhost:9091/webui | 自带控制台 / `/healthz` |
| Elasticsearch | http://localhost:9200 | 无账号密码 |
| Attu | http://localhost:8000 | `--profile ui`，Milvus 图形界面 |
| Kibana | http://localhost:5601 | `--profile ui` |

端口冲突就改 `.env`，不用动 `docker-compose.yml`。

## 自检

```bash
pip install "pymilvus>=2.6" "elasticsearch>=8,<9"
python smoke_test.py
```

## 常用命令

```bash
docker compose ps                      # 状态
docker compose logs -f milvus          # 看日志
docker compose stop                    # 停止（保留数据）
docker compose down                    # 删容器（保留数据卷）
docker compose down -v                 # 连数据一起删
```

## 在代码里连接

```python
# Milvus
from pymilvus import MilvusClient
client = MilvusClient(uri="http://localhost:19530")

# 注意：Milvus 默认一致性是 Bounded，insert 之后立刻 search 可能读不到刚写的数据。
# 需要写后立即可见（比如单测）就建表时指定 Strong：
client.create_collection("demo", dimension=768, consistency_level="Strong")

# Elasticsearch
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
```

LangChain 集成：

```python
from langchain_milvus import Milvus
vs = Milvus(embedding_function=emb, connection_args={"uri": "http://localhost:19530"})

from langchain_elasticsearch import ElasticsearchStore
store = ElasticsearchStore(es_url="http://localhost:9200", index_name="demo", embedding=emb)
```

## 排查

- **Milvus 一直 unhealthy**：`docker compose logs milvus`。内存不足最常见 —— Colima 用户确认
  VM 至少 6～8GiB：`colima list`，不够就 `colima stop && colima start --cpu 4 --memory 8`。
- **Elasticsearch 启动即退出**：多半是堆内存超了，把 `.env` 里 `ES_HEAP` 调成 `512m`。
- **Milvus 起来就 panic `embedded etcd can not be used under distributed mode`**：
  v2.6 起必须带 `DEPLOY_MODE=STANDALONE` 环境变量（compose 里已经配好），
  照抄旧版 v2.5 的启动命令会踩这个。
- **插入成功但搜不到**：不是服务的问题，是默认 Bounded 一致性的可见性延迟，
  见上面「在代码里连接」的说明。
- **数据要重置**：`docker compose down -v` 后重新 `up`。
