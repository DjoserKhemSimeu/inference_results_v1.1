LOADGEN_PATH ?= ../common/loadgen
LDFLAGS = -L$(LOADGEN_PATH) -L../common -lmlperf_loadgen -lnux -lnpu
CPPFLAGS = -I $(LOADGEN_PATH)/include -pthread -g -O3 -march=native -fopenmp -std=c++17

all: ssd_resnet34
ssd_resnet34: ./ssd_resnet34.cpp
	g++ -o $@ $< $(CPPFLAGS) $(LDFLAGS)

clean:
	rm -rf ssd_resnet34

