# Top level Makefile
# list python targets in TARGETS
# supports 'make test' and 'make clean' targets
# Thanks https://lackof.org/taggart/hacking/make-example/

TARGETS = generator parser
# the sets of directories to do various things in
TESTDIRS = $(TARGETS:%=test-%)
CLEANDIRS = $(DIRS:%=clean-%)

test: $(TESTDIRS)
$(TESTDIRS): 
	$(MAKE) -C $(@:test-%=%) test

clean: $(CLEANDIRS)
$(CLEANDIRS): 
	$(MAKE) -C $(@:clean-%=%) clean


.PHONY: subdirs $(TESTDIRS)
.PHONY: subdirs $(CLEANDIRS)
.PHONY: all install clean test
