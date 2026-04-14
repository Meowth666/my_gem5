GEM5_PATH = /gem5
ISA = x86
GXX = g++

all: annotate

annotate: annotate.cpp
	$(GXX) -o annotate annotate.cpp -no-pie \
	-I$(GEM5_PATH)/include \
	-L$(GEM5_PATH)/util/m5/build/$(ISA)/out \
	-I$(GEM5_PATH)/util/m5/src -lm5

clean:
	rm -f annotate