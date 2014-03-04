TARGET=solve_it.pyd
LIBS=-lm
INCLUDE=/usr/include/python3.3m
CC=g++
CFLAGS:=-std=c++11 -g -ggdb -Wall -fpic

OBJECTS = $(patsubst %.cpp, %.o, $(wildcard *.cpp))
HEADERS = $(wildcard *.h)
INCLUDECC = $(addprefix -I,$(INCLUDE))

.PHONY: default all clean
.PRECIOUS: $(TARGET) $(OBJECTS)

default: $(TARGET)
all: default

%.o: %.cpp $(HEADERS)
	$(CC) $(INCLUDECC) $(CFLAGS) -c $< -o $@

$(TARGET): $(OBJECTS)
	$(CC) -shared  $(OBJECTS) -Wall $(LIBS) -o $@

clean:
	-rm -f *.o
	-rm -f $(TARGET)
