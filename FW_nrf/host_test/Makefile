# Simple host-side test build. No Zephyr, no NCS toolchain - uses the
# system C compiler (Apple clang on macOS, gcc on the Pi, same source).
#
#   make       # build + run
#   make clean

CC       ?= cc
CSTD     ?= -std=c99
WARNINGS ?= -Wall -Wextra -Wpedantic -Werror -Wshadow -Wconversion
OPT      ?= -O2 -g

CFLAGS   := $(CSTD) $(WARNINGS) $(OPT) -I../payload

SRC      := ../payload/r129_payload.c test_payload.c
BIN      := test_payload

.PHONY: all run clean

all: run

$(BIN): $(SRC) ../payload/r129_payload.h
	$(CC) $(CFLAGS) $(SRC) -o $@

run: $(BIN)
	./$(BIN)

clean:
	rm -f $(BIN)
