build:
	python3.7 setup.py build_ext --inplace; \

clean:
	rm -rf *.bin *.o *.so ~* cython*.c build/; \

clean_c:
	rm cython*.c; \

.PHONY: build clean clean_c test