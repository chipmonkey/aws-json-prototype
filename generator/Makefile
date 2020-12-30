.PHONY: init help test reqs

objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)

help:
	@echo "Hello World!"
	@echo "'make init' to set up environment dependencies"
	@echo ""
	@echo "EVERYTHING BELOW IS NOT IMPLEMENTED:"
# @echo "'make config' to change defaults"
# @echo "'make run' to run local webserver version"
# @echo "'make build' to, um, build"
	@echo "'make test' to run tests"

apt:
	sudo apt install awscli python3-pytest
	echo "Remove me to rerun apt" > apt

init: apt venv
	( . ./venv/bin/activate; \
	  pip install pip-tools; )

install: init requirements.txt
	( . ./venv/bin/activate; \
	  pip install -r requirements.txt; )

test-install: install test-requirements.txt
	( . ./venv/bin/activate; \
	  pip install -r test-requirements.txt; )


reqs: requirements.txt $(outputs)

%.txt: %.in
	( . ./venv/bin/activate; \
	pip-compile -v --output-file $@ $< ; )

check:
	@which pip-compile > /dev/null
	@which pytest > /dev/null

clean:
	- rm -f *.txt
	- rm -rf venv
	- rm -f apt

venv:
	python3 -m venv venv

develop:
	. ./venv/bin/activate

local:
	( . ./venv/bin/activate; \
	python -m http.server; )

test: test-install lint
	( . ./venv/bin/activate; \
	coverage run --source=./generate/ -m pytest .; \
	coverage report -m --fail-under=100; )

lint:
	( . ./venv/bin/activate; \
	pylint generate/ )

build:

pep8:
	autopep8 generate/ --recursive --in-place --aggressive --pep8-passes 2000 --verbose
