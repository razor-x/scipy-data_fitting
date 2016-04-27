all: lint test docs

docs:
	@pdoc --html --html-dir ./docs --overwrite ./scipy_data_fitting
	@pdoc --html --html-dir ./docs/scipy_data_fitting \
		--overwrite ./scipy_data_fitting/figure

examples:
	@$(foreach x,$(wildcard examples/*.py),python $(x);)

lint:
	@python setup.py lint

release: docs
	@rm -rf build dist
	@python setup.py sdist bdist_wheel
	@twine upload dist/*
	@python setup.py upload_docs --upload-dir ./docs/scipy_data_fitting

test:
	@python setup.py nosetests \
		--with-coverage --cover-html --cover-xml \
		--cover-package=scipy_data_fitting

serve:
	@python server.py

.PHONY: docs examples test
