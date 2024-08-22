base:
	@echo 'i am makefile'
testall: typecheck coverage
test: cleartestdb
	pytest
coverage: cleartestdb
	@coverage run -m pytest -q
	@coverage report -m --skip-empty
	@coverage html
typecheck:
	@mypy *.py --disable-error-code=import-untyped
cleartestdb:
	@dbmate -e TEST_DATABASE_URL drop
	@dbmate -e TEST_DATABASE_URL create
	@dbmate -e TEST_DATABASE_URL load
setupdb:
	@dbmate up
destroydb:
	@dbmate drop
