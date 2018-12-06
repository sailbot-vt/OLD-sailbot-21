test:
	$(MAKE) build && $(MAKE) run && $(MAKE) clean

build:
	gcc -o msg_tests.bin -std=c11 -Werror -Wall *.c ../../../src/msg/*.c -lpython3.7

run:
	./msg_tests.bin

clean:
	rm msg_tests.bin


.PHONY: test build run clean