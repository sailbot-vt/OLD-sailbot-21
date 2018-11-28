build:
	python3.7 setup.py build_ext --inplace; \

test:
	gcc -o tests.bin *.c -Werror -Wall -std=c11 -ggdb3


clean:
	rm *.bin *.o ~*; \

.PHONY: build clean test