test:
	$(MAKE) build && $(MAKE) run && $(MAKE) clean

build:
	cd ../../../src/msg && $(MAKE) clean_c; \
	cd ../../tests/msg_tests/c_tests; \
	gcc -o msg_tests.bin -std=gnu11 *.c ../../../src/msg/*.c -I../../../p3_7env/include/python3.7m -Werror -Wall -undefined dynamic_lookup; \

run:
	./msg_tests.bin

clean:
	rm msg_tests.bin


.PHONY: test build run clean