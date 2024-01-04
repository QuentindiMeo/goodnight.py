.PHONY: all clean goodnight tests install

all: goodnight

goodnight:
	@chmod +x goodnight

clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__/
	@rm -rf tests/__pycache__/
	@rm -rf tests/*.pyc
	@rm -rf *.pyc
	@echo "Cleaning complete."

tests:
	@echo "Running tests..."
	@./tests/test.sh
	@echo "Tests complete."

install:
	@echo "Installing pyperclip..."
	@pip install pyperclip==1.8.2
	@echo "Installation complete."
	@echo ""
	@echo "Depending on your system, you may now need to install:"
	@echo "xclip or xsel (Linux), pbcopy and pbpaste (Mac), pywin32 (Windows)."
