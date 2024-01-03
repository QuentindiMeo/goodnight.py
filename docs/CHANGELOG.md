# goonight.py Changelog

## [UNRELEASED]

### REL 1.0.0 - Jan ?? 2024

First release; major README update

### DEV 0.2.9 - Jan ?? 2024

Adding and implementing `--delay`, `--times`
Implementing `--XXX=x` parameter syntax

---

### DEV 0.2.8 - Dec 31 2023

Implemented `--alternate`, making the program alternate between commas/emoji and "and"s
Added and implemented `--infinite`, making the program infinitely generate goodnights
Created Goodnight class holding the result text and a boolean for `--other-step`'s steps

### DEV 0.2.7 - Dec 13 2023

Added and implemented `--no-copy`, disabling clipboard copy
Added `--alternate`
Deprecated `--isave` as `--save` can be combined with `--default`

### DEV 0.2.6 - Nov 26 2023

Added and implemented `--save`, saving preferences to file
Improved largely code efficiency and structure for maintainability

### DEV 0.2.5 - Nov 13 2023

Added and implemented `--other-step`, making the program use the even-numbered phrase gaps as "and"s instead of commas
Updated usage/help function to reflect additions
Set 999 as maximum value for `-n` and `-b` upper bound

---

### DEV 0.2.4 - Nov 09 2023

Added documentation: commenting and [README](../README.md)
Fixed default parameter skip for `-n` and `-b`

### DEV 0.2.3 - Nov 08 2023

Improved coding style (ty [SonarLint](https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarlint-vscode))
Adjuted README badges

### DEV 0.2.2 - Nov 06 2023

Implemented the possibility to have several PHRASES (and others) in a source file
Added warning prompt if it is the case, asking if the user wants to continue

### DEV 0.2.1 - Nov 06 2023

Added nicer transition `"and"` between phrases instead of commas
Adjusted the presentation gif

### DEV 0.2.0 - Nov 06 2023

Implemented phrase picking
Added `-r` as an alias of `--allow-repetition`
Added a presentation gif to the [README](../README.md)

---

### DEV 0.1.6 - Nov 05 2023

Fixed usedEmoji malfunction (picked emoji not removed from list)
Removed apparent double quotes around every element (e.g. `"phrase"` instead of `phrase`)

### DEV 0.1.5 - Nov 05 2023

Fixed multioptional parameters oddity
Removed CLI asking for parameters that are already set by the preferences file

### DEV 0.1.4 - Nov 05 2023

Implemented emoji picking
Improved context verbosity and prints quality on `--verbose`
Fixed missing file extraction case

### DEV 0.1.3 - Nov 05 2023

Added and implemented `--allow-repetition`,
    allowing the same phrase to be picked several times if all other phrases have been picked
Implemented nickname picking
Fixed some `-n` and `-b` oddities

### DEV 0.1.2 - Nov 04 2023

Fixed CLI oddities; added `--default`, warning if high upper bound on range, links on README badges

### DEV 0.1.1 - Nov 03 2023

Added and implemented `--isave`: ignore preferences, save CLI answers as preferences
Added possibility to set a random range as a value nbPhrases (picks a random number between the two bounds)

### DEV 0.1.0 - Nov 02 2023

Added weighting feature to source extractor (Contents class)
Renamed `--debug` to `--verbose`

---

### DEV 0.0.5 - Nov 01 2023

Added and implemented `--debug`: a mode that prints the program's steps
Added nicknames to source extractor
Removed `-D`
Created Types file with type aliases for clarity

### DEV 0.0.4 - Nov 01 2023

Completed implementation of `-s` (source file selection)
Added a sources extractor (phrases, emoji)
Added multioptional parameters handling for boolean parameters (e.g. `-eD`)

### DEV 0.0.3 - Nov 01 2023

Added `-s` (implementation in progress)
Added preferences.sav file: save to it with `-D`, ignore its contents with `-i`/`--ignore`
Added a Ctrl+C handler

### DEV 0.0.2 - Oct 31 2023

Added parameter handling under forms `-X` and `--XXX`
Completed setup for Exit and Help

### DEV 0.0.1 - Oct 30 2023

Added Parameters class to handle and hold program parameters
Added and implemented `-n` (number of phrases to draw), `-e` (toggle emoji mode), `-w` (for whom)
Adding first elementary components

### DEV 0.0.0 - Oct 30 2023

Project creation. [#1](https://github.com/QuentindiMeo/goodnight.py/commit/10593fa32045e11cfd8621fe0bf106547ce16f80)
