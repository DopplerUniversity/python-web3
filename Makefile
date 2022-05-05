.PHONY: deps
deps: ve
	./ve/bin/pip check \
		|| ./ve/bin/pip install -r requirements.txt

ve:
	python -m venv ve

.PHONY: accounts get-txn balance latest-block
accounts get-txn balance latest-block: deps
	./ve/bin/python script.py $@
