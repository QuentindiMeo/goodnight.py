.PHONY: all clean goodnight tests install

all: goodnight

goodnight:
	cp src/goodnight.py goodnight
	chmod +x goodnight

clean:
	rm -f goodnight

tests:
	./tests/test.sh

install:
	pip install -r requirements.txt
