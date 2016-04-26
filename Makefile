docs:
	@pdoc --html --html-dir ./docs --overwrite ./scipy_data_fitting
	@pdoc --html --html-dir ./docs/scipy_data_fitting \
		--overwrite ./scipy_data_fitting/figure

examples:
	@$(foreach x,$(wildcard examples/*.py),python $(x);)

release: docs
	@python setup.py sdist bdist_wheel
	@python twine register dist/*
	@python twine upload dist/*
	@python setup.py upload_docs --upload-dir ./docs/scipy_data_fitting

test:
	@python setup.py nosetests --with-coverage --cover-html \
		--cover-package=scipy_data_fitting

serve:
	@python server.py

.PHONY: docs examples test

