.PHONY: format
format:
	npx prettier src/ --write

.PHONY: build
build:
	mdbook build

.PHONY: open
open:
	mdbook build --open

.PHONY: check
check:
	npx prettier src/ --check
