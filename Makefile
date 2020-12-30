SHELL := /bin/bash
# Top level Makefile
# list python targets in TARGETS
# supports 'make test' and 'make clean' targets
# Thanks https://lackof.org/taggart/hacking/make-example/

TARGETS = generator parser
# the sets of directories to do various things in
TESTDIRS = $(TARGETS:%=test-%)
CLEANDIRS = $(TARGETS:%=clean-%)
INITDIRS = $(TARGETS:%=init-%)
BUILDDIRS = $(TARGETS:%=build-%)

test: $(TESTDIRS)
$(TESTDIRS): 
	$(MAKE) -C $(@:test-%=%) test

clean: $(CLEANDIRS)
	- rm -f apt
	- rm -rf venv
$(CLEANDIRS): 
	$(MAKE) -C $(@:clean-%=%) clean

init: $(INITDIRS) apt
$(INITDIRS):
	$(MAKE) -C $(@:init-%=%) init

build: $(BUILDDIRS)
$(BUILDDIRS):
	$(MAKE) -C $(@:build-%=%) build

apt:
	sudo apt install awscli
	echo "Remove me to rerun apt" > apt


.PHONY: subdirs $(TESTDIRS)
.PHONY: subdirs $(CLEANDIRS)
.PHONY: subdirs $(INITDIRS)
.PHONY: all init clean test

config: apt
	@./configure.sh
