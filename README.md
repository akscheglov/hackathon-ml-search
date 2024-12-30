# Install

Install python3 and than

```sh
make requirements-restore
```

# Try llamafile

Example from [here](https://www.llamaindex.ai/blog/using-llamaindex-and-llamafile-to-build-a-local-private-research-assistant)

Config located at `.settings` file

This will download llamafile (~4.29 GB)

First download and start llamafile

```sh
make llamafile-start
```

Create an index first

```sh
make llamafile-index
```

And query this index

```sh
make llamafile-query
```

# Try ollama and store index in elastic search

Example from [here](https://www.elastic.co/search-labs/blog/rag-with-llamaIndex-and-elasticsearch)

Config located at `.settings` file

This requires docker for elasticsearch and ollama

Install ollama [first](https://ollama.com/download)

Start ollama (will download model ~4.1 GB)

```sh
make ollama
```

Create an index first

```sh
make elastic-index
```

And query this index

```sh
make elastic-query
```

# Something other

Set something in `.settings`
- `MODEL_TYPE` to switch between `OLLAMA` and `LLAMAFILE`
- `OLLAMA_MODEL` to change ollama model to anoher

# TODO: checkhout

https://docs.llamaindex.ai/en/stable/examples/query_engine/knowledge_graph_rag_query_engine/

https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/metadata_extraction/MetadataExtractionSEC.ipynb

https://docs.llamaindex.ai/en/stable/examples/vector_stores/elasticsearch_auto_retriever/

https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/
