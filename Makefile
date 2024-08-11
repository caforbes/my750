base:
	@echo 'i am makefile'
test: cleartestdb
	pytest
cleartestdb:
	@dbmate -e TEST_DATABASE_URL drop
	@dbmate -e TEST_DATABASE_URL create
	@dbmate -e TEST_DATABASE_URL load
setupdb:
	@dbmate up
destroydb:
	@dbmate drop
