init:
	pip install -r requirements.txt --use-mirrors

test:
	nosetests tests --logging-level=WARN