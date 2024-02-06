# VARIABLES #

ECHO	=	/bin/echo -e
RM	=	rm -rf
CHMOD	=	chmod +x

COMPIL	=	*.pyc
SRC	=	src/
TESTS	=	tests/
CACHE	=	__pycache__/
NAME	=	goodnight.py

# TARGETS #

.PHONY: all clean goodnight default_run tests install

all:
	@$(ECHO) $(GRN)"  Assembling "$(NAME)"..."$(DEF) && \
	$(CHMOD) $(NAME) && \
	$(ECHO) $(GRN)"  "$(NAME)" ready to roll!!"$(DEF)

default_run:
	@$(ECHO) $(GRN)"  Running default case of "$(NAME)"..."$(DEF) && \
	./$(NAME) --default && \
	$(ECHO) $(GRN)"  "$(NAME)" run complete."$(DEF) || ( \
		$(ECHO) $(RED)"  "$(NAME)" run failed."$(DEF) \
	)

clean:
	@$(ECHO) $(GRN)"  Cleaning..."$(DEF) && \
	$(ECHO) $(LGTGRN)"  Cleaning " $(BLU)$(CACHE)$(DEF) && $(RM) $(SRC)$(CACHE) && \
	$(ECHO) $(LGTGRN)"  Cleaning " $(BLU)$(COMPIL)$(DEF) && $(RM) $(TESTS)$(COMPIL) && \
	$(ECHO) $(LGTGRN)"  Cleaning " $(BLU)$(TESTS)$(CACHE)$(DEF) && $(RM) $(TESTS)$(CACHE) && \
	$(ECHO) $(LGTGRN)"  Cleaning " $(BLU)$(TESTS)$(COMPIL)$(DEF) && $(RM) $(TESTS)$(COMPIL) && \
	$(ECHO) $(GRN)"  Cleaning complete."$(DEF) || ( \
		$(ECHO) $(RED)"  Cleaning failed."$(DEF) \
	)

tests:
	@$(ECHO) $(GRN)"  Running tests..."$(DEF) && \
	./tests/test.sh && \
	$(ECHO) $(GRN)"  Tests run complete."$(DEF) || ( \
		$(ECHO) $(RED)"  Tests run failed."$(DEF) \
	)

install:
	@$(ECHO) $(GRN)"  Installing pyperclip..."$(DEF) && \
	pip install pyperclip==1.8.2 && \
	$(ECHO) $(GRN)"  Installation complete.\n"$(DEF) && \
	$(ECHO) $(BLU)"  Depending on your system, you may now need to install:" && \
	$(ECHO) "\txclip or xsel (Linux),\n\tpbcopy and pbpaste (Mac),\n\tpywin32 (Windows)"$(DEF) || ( \
		$(ECHO) $(RED)"  Installation failed. Please make sure you have pip installed."$(DEF) && \
		$(ECHO) $(BLU)"  On Ubuntu, for example... 'sudo apt-get install python3-pip' might help."$(DEF) \
	)

# COLORING PRINTS #

DEF	=	"\e[0m"
BLU	=	"\e[1;34m"
LGTGRN	=	"\e[0;32m"
GRN	=	"\e[1;32m"
RED	=	"\e[1;31m"