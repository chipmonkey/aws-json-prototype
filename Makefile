SHELL := /bin/bash
# Top level Makefile
# list python targets in TARGETS
# Thanks https://lackof.org/taggart/hacking/make-example/

help:
	@echo "Requires make, which, since you see this, you probably have"
	@echo ""
	@echo "'make config' to change defaults"
	@echo "'make init' to set up environment dependencies"
	@echo "'make build' to, um, build"
	@echo "'make test' to run tests"
	@echo "'make deploy' deploy to AWS (will fail if stack exists)"
	@echo "'make update' for non-destructive subsequent deploys" 
	@echo "'make wipe' to delete stack from AWS (will fail if S3 not empty)" 

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

wipe:
	( cd ./parser && $(MAKE) deploy-aws )
	( cd ./deployment/aws && ./wipe_stack.sh )

deploy:
	( cd ./parser && $(MAKE) deploy-aws )
	( cd ./deployment/aws && ./deploy_stack.sh )

update:
	( cd ./parser && $(MAKE) deploy-aws )
	( cd ./deployment/aws && ./update_stack.sh )
