ADAFLAGS ?= -O2
% : %.adb
	gnat make $@ -cargs $(ADAFLAGS)

.PHONY: all
all: day3
	./day3 < test.txt
	./day3 < day3_input.txt

.PHONY: clean
clean:
	rm -f *.o
	rm -f day3 day3b
