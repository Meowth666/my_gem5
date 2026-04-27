GEM5_PATH = /gem5
ISA = arm64
GXX = aarch64-linux-gnu-g++


all: 04-cross-compile-this-static 04-cross-compile-this-dynamic

04-cross-compile-this-static: m5.cpp
	$(GXX) -o 04-cross-compile-this-static m5.cpp -static -I$(GEM5_PATH)/include -L$(GEM5_PATH)/util/m5/build/$(ISA)/out -lm5

04-cross-compile-this-dynamic: m5.cpp
	$(GXX) -o 04-cross-compile-this-dynamic m5.cpp -I$(GEM5_PATH)/include -L$(GEM5_PATH)/util/m5/build/$(ISA)/out -lm5

clean:
	rm -f 04-cross-compile-this-static 04-cross-compile-this-dynamic