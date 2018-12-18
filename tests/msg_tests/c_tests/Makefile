ifndef EXE_DIR
	EXE_DIR := $(ROOT_DIR)/bin
endif

build:
	cd $(ROOT_DIR)/src/msg; $(MAKE) clean_c
	$(MAKE) compile

test:
	$(EXE_DIR)/msg_tests.bin


CCFLAGS = -Werror -Wall

ifeq ($(CC), clang)
	CCFLAGS += -undefined dynamic_lookup
else
	CC = gcc
	CCFLAGS = -Wl,--unresolved-symbols=ignore-all
endif

compile:
	$(CC) -o $(EXE_DIR)/msg_tests.bin -std=gnu11 -ggdb3 -pthread *.c $(ROOT_DIR)/src/msg/*.c -I$(ROOT_DIR)/p3_7env/include/python3.7m $(CCFLAGS)

.PHONY: test build run clean compile