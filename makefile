CC = clang
CFLAGS = -Wall -std=c99 -pedantic
LIBS = -lm

all: libphylib.so _phylib.so

clean:
	rm -f *.o *.so *.svg phylib_wrap.c phylib.py

phylib_wrap.c phylib.py: phylib.i phylib.h
	swig -python phylib.i 

phylib_wrap.o: phylib_wrap.c phylib.h
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11/ -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o phylib.o libphylib.so
	$(CC) -shared phylib_wrap.o -L. -L/usr/lib/python3.11/ -lpython3.11 -lphylib -o _phylib.so

libphylib.so: phylib.o
	$(CC) -shared phylib.o $(LIBS) -o libphylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -fPIC -o phylib.o 

