# VARIABLES #

ECHO	=	/bin/echo -e
RM		=	rm -rf
CHMOD	=	chmod +x

COMPIL	=	*.pyc
CACHE	=	__pycache__/
NAME	=	goodnight.py

# TARGETS #

.PHONY: all clean goodnight run tests install

all: $(NAME)

$(NAME):
	@$(ECHO) $(BOLDGRN) " Assembling "$(NAME)"..."$(DEF)
	@$(CHMOD) $(NAME)
	@$(ECHO) $(BOLDGRN) " "$(NAME)" ready to roll!!"$(DEF)

run:
	@$(ECHO) $(BOLDGRN) " Running default case of "$(NAME)"..."$(DEF)
	@./$(NAME) --default
	@$(ECHO) $(BOLDGRN) " "$(NAME)" run complete."$(DEF) || $(ECHO) $(RED) " "$(NAME)" run failed."$(DEF)

clean:
	@$(ECHO) $(BOLDGRN) " Cleaning..."$(DEF)
	@$(ECHO) $(GRN) " Cleaning " $(BLU)$(CACHE)$(DEF) && $(RM) $(CACHE)
	@$(ECHO) $(GRN) " Cleaning " $(BLU)$(COMPIL)$(DEF) && $(RM) $(COMPIL)
	@$(ECHO) $(GRN) " Cleaning " $(BLU)tests/$(CACHE)$(DEF) && $(RM) tests/$(CACHE)
	@$(ECHO) $(GRN) " Cleaning " $(BLU)tests/$(COMPIL)$(DEF) && $(RM) tests/$(COMPIL)
	@$(ECHO) $(BOLDGRN) " Cleaning complete."$(DEF) || $(ECHO) $(RED) " Cleaning failed."$(DEF)

tests:
	@$(ECHO) $(BOLDGRN) " Running tests..."$(DEF)
	@./tests/test.sh
	@$(ECHO) $(BOLDGRN) " Tests run complete."$(DEF) || $(ECHO) $(RED) " Tests run failed."$(DEF)

install:
	@$(ECHO) $(BOLDGRN) " Installing pyperclip tests..."$(DEF)
	@pip install pyperclip==1.8.2
	@$(ECHO) $(BOLDGRN) " Installation complete.\n"$(DEF)
	@$(ECHO) $(BLU) " Depending on your system, you may now need to install:"
	@$(ECHO) "\txclip or xsel (Linux),\n\tpbcopy and pbpaste (Mac),\n\tpywin32 (Windows)"$(DEF)

# COLORING PRINTS #

DEF	=	"\e[0m"
BLU	=	"\e[1;34m"
GRN	=	"\e[0;32m"
BOLDGRN	=	"\e[1;32m"
RED	=	"\e[1;31m"