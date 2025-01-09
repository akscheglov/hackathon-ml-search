#!make
include .settings

python = python
pip = pip

env_name = .venv
llamafile_path = llamafile/${LLAMAFILE_NAME}

requirements-restore:
	${python} --version
	${pip} --version
	${python} -m venv ${env_name}
	source ./${env_name}/bin/activate && ${python} -m ${pip} install -r requirements.txt

requirements-dump:
	source ./${env_name}/bin/activate && ${python} -m ${pip} freeze > requirements.txt

deptry:
	source ./${env_name}/bin/activate && deptry . --exclude ${env_name}

#####

llamafile-index:
	cd llamafile && ${python} index.py

llamafile-query:
	cd llamafile && ${python} query.py

# https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file#quickstart
llamafile-download:
ifeq (,$(wildcard ${llamafile_path}))
	@echo 'llamafile not found, downloading...'
	curl 'https://huggingface.co/Mozilla/llava-v1.5-7b-llamafile/resolve/main/${LLAMAFILE_NAME}?download=true' -o ${llamafile_path}
	chmod +x ${llamafile_path}
else
	@echo 'llamafile already exists'
endif

llamafile-start: llamafile-download
	${llamafile_path} --embedding --port ${LLAMAFILE_PORT}

#####

elastic-index: # elastic-search-start
	cd elastic && ${python} index.py

elastic-query: # elastic-search-start
	cd elastic && ${python} query.py

# https://ollama.com/download
ollama:
	ollama --version
	ollama run ${OLLAMA_MODEL}

elastic-search-start:
	docker-compose -f elastic/docker-compose.yml up -d

elastic-search-index-delete-ollama:
	curl -X "DELETE" http://localhost:9200/${OLLAMA_MODEL}_ollama_idx

elastic-search-index-backup:
	curl -X PUT "localhost:9200/_snapshot/idx_backup" -H 'Content-Type: application/json' -d'{ "type": "fs", "settings": { "location": "idx_backup" }}'
	# curl -X PUT "localhost:9200/_snapshot/idx_backup/%3Cidx_snapshot_%7Bnow%2Fd%7D%3E?pretty"
