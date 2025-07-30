.PHONY: setup
setup:
	@./scripts/setup.sh

.PHONY: run
run:
	@./scripts/run.sh

.PHONY: clean
clean:
	@rm -rf data/tmp
