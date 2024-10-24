.DEFAULT_GOAL := help
.PHONY: help lint test

SRD_DIR = khaya
TEST_DIR = tests

ci: lint typecheck test ## Run all CI checks 
.PHONY: ci

lint:  ## Run linting
	poetry run isort $(SRC_DIR) $(TEST_DIR)
	poetry run flake8 --max-line-length 120 $(SRC_DIR) $(TEST_DIR)
.PHONY: lint


typecheck: ## Run type checking
	poetry run mypy $(SRD_DIR)
.PHONY: typecheck

test: ## Run tests
	poetry run coverage run --source=$(SRD_DIR) -m pytest -v $(TEST_DIR) && poetry run coverage report -m
.PHONY: test

clean-py: ## Remove python cache files
	find . -name '__pycache__' -type d -exec rm -r {} +
	find . -name '*.pyc' -type f -exec rm {} +
	rm -rf ./*.egg-info
.PHONY: clean-py

.PHONY: help
help: ## Show help message
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/:/'`); \
	printf "%s\n\n" "Usage: make [task]"; \
	printf "%-20s %s\n" "task" "help" ; \
	printf "%-20s %s\n" "------" "----" ; \
	for help_line in $${help_lines[@]}; do \
		IFS=$$':' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf '\033[36m'; \
		printf "%-20s %s" $$help_command ; \
		printf '\033[0m'; \
		printf "%s\n" $$help_info; \
	done
