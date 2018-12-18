test:
	$(MAKE) build && $(MAKE) run && $(MAKE) clean

build:
	cd ../../../src/msg; $(MAKE) clean_c
	$(MAKE) compile

run:
	./msg_tests.bin

clean:
	-rm msg_tests.bin

CC = gcc
CCFLAGS = -Werror -Wall

ifeq (, $(shell which clang))
	CCFLAGS += --no-allow-shlib-undefined
else
	CC = clang
	CCFLAGS += -undefined dynamic_lookup
endif

compile:
	$(CC) -o msg_tests.bin -std=gnu11 *.c ../../../src/msg/*.c -I../../../p3_7env/include/python3.7m $(CCFLAGS)


.PHONY: test build run clean compile