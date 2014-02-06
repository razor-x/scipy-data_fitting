docs:
	@pdoc --html --html-dir ./docs --overwrite ./scipy_data_fitting

examples:
	@$(foreach x,$(wildcard examples/*.py),python $(x);)

release: docs
	@python setup.py register sdist bdist_egg upload
	@python setup.py upload_docs --upload-dir ./docs/scipy_data_fitting

test:
	@nosetests

.PHONY: docs examples test

