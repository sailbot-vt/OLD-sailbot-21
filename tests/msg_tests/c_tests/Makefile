test:
	$(MAKE) build && $(MAKE) run && $(MAKE) clean

build:
	cd ../../../src/msg; $(MAKE) clean_c
	$(MAKE) compile

run:
	./msg_tests.bin

clean:
	-rm msg_tests.bin

CCFLAGS = -Werror -Wall

ifeq ($(CC), clang)
	CCFLAGS += -undefined dynamic_lookup
else
	CC = gcc
	CCFLAGS = --unresolved-symbols=ignore-all
endif

compile:
	$(CC) -o msg_tests.bin -std=gnu11 -pthread *.c ../../../src/msg/*.c -I../../../p3_7env/include/python3.7m $(CCFLAGS)

.PHONY: test build run clean compile