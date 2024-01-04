# goodnight\.py Changelog

## [UNRELEASED]

### REL 1.0.0 - Jan ?? 2024 [[#x]()]

First release; major README update

### DEV 0.2.9 - Jan ?? 2024 [[#x]()]

Adding and implementing `--delay`, `--times`
Implementing `--XXX=x` parameter syntax
Centralizing Markdown files in [docs/](.) (hello)

---

### DEV 0.2.8 - Dec 31 2023 [[#x]()]

Implemented `--alternate` aka `-a`, making the program alternate between commas/emoji and "and"s
Added and implemented `--infinite` aka `-i`, making the program infinitely generate goodnights
`-i` is therefore not an alias of `--ignore` any more.
Created Goodnight class holding the result text and a boolean for `--other-step`'s steps

### DEV 0.2.7 - Dec 13 2023 [[#x]()]

Added and implemented `--no-copy`, disabling clipboard copy
Added `--alternate`
Deprecated and removed `--isave`; as `--save` can be combined with `--default`

### DEV 0.2.6 - Nov 26 2023 [[#x]()]

Added and implemented `--save` aka `-S`, saving preferences to file
Improved largely code efficiency and structure for maintainability
Added [LICENSE](LICENSE.md) file and [issue templates](../.github/ISSUE_TEMPLATE)

### DEV 0.2.5 - Nov 13 2023 [[#x]()]

Added and implemented `--other-step` aka `-o`, making the program use the even-numbered phrase gaps as "and"s instead of commas
Updated usage/help function to reflect additions
Set 999 as maximum value for `-n` and `-b` upper bound

---

### DEV 0.2.4 - Nov 09 2023 [[#x]()]

Added documentation: commenting code, [source.log](../assets/source.log) and boosting the [README](../README.md)
Fixed default parameter skip for `-n` and `-b`

### DEV 0.2.3 - Nov 08 2023 [[#x]()]

Improved coding style (ty [SonarLint](https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarlint-vscode))
Adjuted README badges

### DEV 0.2.2 - Nov 06 2023 [[#x]()]

Implemented the possibility to have several PHRASES (and others) in a source file
Added warning prompt if it is the case, asking if the user wants to continue

### DEV 0.2.1 - Nov 06 2023 [[#x]()]

Added nicer transition `"and"` between phrases instead of commas
Adjusted the presentation gif

### DEV 0.2.0 - Nov 06 2023 [[#x]()]

Implemented phrase picking
Added `-r` as an alias of `--allow-repetition`
Added a presentation gif to the [README](../README.md)

---

### DEV 0.1.6 - Nov 05 2023 [[#x]()]

Fixed usedEmoji malfunction (picked emoji not removed from list)
Removed apparent double quotes around every element (e.g. `"phrase"` instead of `phrase`)

### DEV 0.1.5 - Nov 05 2023 [[#33](https://github.com/QuentindiMeo/goodnight.py/commit/89094a5574caa2a08110802dedd311595f22a592)]

Fixed multioptional parameters oddity: disallowing long parameters and their aliases
Removed CLI asking for parameters that are already set by the preferences file

### DEV 0.1.4 - Nov 05 2023 [[#31](https://github.com/QuentindiMeo/goodnight.py/commit/2565370818018ce4cb477d1e8053a36f0dae44ac)]

Implemented emoji picking
Improved context verbosity and prints quality on `--verbose`
Fixed missing file extraction case on `--allow-repetition`

### DEV 0.1.3 - Nov 05 2023 [[#29](https://github.com/QuentindiMeo/goodnight.py/commit/444a8e9a7d7c45cffa12499df67ff5aeef7e34f0)]

Added and implemented `--allow-repetition`:
    allow the same phrase to be picked several times if all other phrases have been picked
Implemented nickname picking
Created a Contents class that holds the source file's contents, for clarity
Fixed some `-n` and `-b` oddities

### DEV 0.1.2 - Nov 04 2023 [[#28](https://github.com/QuentindiMeo/goodnight.py/commit/48a3e2c0c6c94448519df2fe1e7ee2ff1ab89455)]

Added and implemented `--default`: using default values for all parameters
Added warning if a high upper bound / value is set for `-b`/`-n`
Fixed CLI oddities: unhandled parameter exceptions
Added links on [README](../README.md) badges

### DEV 0.1.1 - Nov 03 2023 [[#23](https://github.com/QuentindiMeo/goodnight.py/commit/3765c815fdc011277158463dc96c16ae657c11b0)]

Added and implemented `--isave`: ignore preferences, save CLI answers as preferences
Added possibility to set a random range as a value nbPhrases (picks a random number between the two bounds)

### DEV 0.1.0 - Nov 02 2023 [[#21](https://github.com/QuentindiMeo/goodnight.py/commit/d3bcec6595ce4866b7c1e4193299b202992ddcc8)]

Added weighting feature to source extractor (Contents class)
Renamed `--debug` to `--verbose`

---

### DEV 0.0.5 - Nov 01 2023 [[#19](https://github.com/QuentindiMeo/goodnight.py/commit/b8cc6aa66eb0b09b83b8b0ea8804d0d6c8edf87b)]

Added and implemented `--debug`: a mode that prints the program's steps
Added nicknames to source extractor
Deprecated and removed `-D`
Created Types file with type aliases for clarity

### DEV 0.0.4 - Nov 01 2023 [[#11](https://github.com/QuentindiMeo/goodnight.py/commit/eea6d3ba7795842126740a9ebef5078f0cdcd009)]

Completed implementation of `-s` (source file selection)
Added a sources extractor (phrases, emoji)
Added multioptional parameters handling for boolean parameters (e.g. `-eD`)

### DEV 0.0.3 - Nov 01 2023 [[#8](https://github.com/QuentindiMeo/goodnight.py/commit/66202eb8dc85328ca37ceaa278d631fba45c5a79)]

Added `-s` (implementation in progress)
Added preferences.sav file: save to it with `-D`, ignore its contents with `-i`/`--ignore`
Added a Ctrl+C handler

### DEV 0.0.2 - Oct 31 2023 [[#6](https://github.com/QuentindiMeo/goodnight.py/commit/5da4d12644290f576cc462df6057c9c9770e224a)]

Added parameter handling under forms `-X` and `--XXX`
Completed setup for Exit and Help

### DEV 0.0.1 - Oct 30 2023 [[#4](https://github.com/QuentindiMeo/goodnight.py/commit/2682ee6f539a30452187c110552fa49d5f014d34)]

Added Parameters class to handle and hold program parameters
Added and implemented `-n` (number of phrases to draw), `-e` (toggle emoji mode), `-w` (for whom)
Adding first elementary components

### DEV 0.0.0 - Oct 30 2023 [[#1](https://github.com/QuentindiMeo/goodnight.py/commit/10593fa32045e11cfd8621fe0bf106547ce16f80)]

Project creation.
