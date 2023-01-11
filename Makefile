.PHONY: test


test: poet
	bash run_tests.sh

selected: poet
	bash selected_test.sh

run:
	bash run_develop.sh

poet:
	poetry env use $(shell which python3.7)

whichtests:
	poetry run pytest --collect-only
