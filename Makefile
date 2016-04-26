docs:
	@pdoc --html --html-dir ./docs --overwrite ./scipy_data_fitting
	@pdoc --html --html-dir ./docs/scipy_data_fitting \
		--overwrite ./scipy_data_fitting/figure

examples:
	@$(foreach x,$(wildcard examples/*.py),python $(x);)

release:
	@python setup.py sdist bdist_wheel
	@python twine register dist/*
	@python twine upload dist/*

test:
	@python setup.py nosetests --with-coverage --cover-html

serve:
	@python server.py

.PHONY: docs examples test

