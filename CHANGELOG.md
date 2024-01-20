# goodnight\.py Changelog

<div id="top" />

## [UNRELEASED]

### REL 1.0.0 - XXX ?? 2024 [[#x]()]

First release
Announcing the release on Reddit & Discord

### DEV 0.3.3 - Jan ?? 2024 [[#x]()]

Adding and implementing `--version` aka `-v`: print the program's version.  
Adding a dynamic loading bar while the program is generating a goodnight.  
Redacting and making unit tests.  
Announcing the release date of the first release on Reddit & Discord.

### DEV 0.3.2 - Jan ?? 2024 [[#x]()]

Adding a values unpacking function for parameters, for clarity.  
Adding a Ctrl+D handler, exiting the program gracefully with a context message [EOFError, SIGTERM].  
Fixing the long overdue bug of the static FILE_AV suppressing the CLI asking for parameters.  
Redacting a demonstration script and a demonstration source file.  
Updating the [README demonstration gif](README.md).

### DEV 0.3.1 - Jan ?? 2024 [[#x]()]

Enhancing the Makefile and its prints.  
Changed the Parameters class' constructor to taking a dictionary argument, to avoid having 20 arguments.  
Adding and implementing `--nick-nth`: forcing the nickname to be after the nth phrase.  
Adding and implementing `--preferences` aka `-p`: punctually, using a specifice file as set preferences file.  
Updating the [README](README.md)'s general information to reflect changes.

---

## [RELEASED]

### DEV 0.3.0 - Jan 06 2024 [[#x]()]

Creating a Makefile and executable file at the root of the repository, for clarity.  
Adding confirmation prompt if the delay is set to a high value (> 10000) through CLI.  
Implementing the possibility to set the delay to `p`: press Enter to proceed after each interation.  
Implementing `--XXX=x` parameter syntax.  
Implementing duplicate parameter error handling.  
Enhancing verbosity and context messages.

---

### DEV 0.2.9 - Jan 04 2024 [[#73](https://github.com/QuentindiMeo/goodnight.py/commit/9e869cdd585183bd89673fda99fbc057efb5b8fa)]

Added and implemented `--times`: compute and print x goodnights.  
Added and implemented `--delay`: add a delay between each goodnight iteration (in milliseconds).  
Created this file (hello), [CODE OF CONDUCT](CODE_OF_CONDUCT.md) and [CONTRIBUTING](CONTRIBUTING.md).

### DEV 0.2.8 - Dec 31 2023 [[#64](https://github.com/QuentindiMeo/goodnight.py/commit/7fa2780f0411992f1704d1b91860585eb5394a82)]

Implemented `--alternate` aka `-a`: make the program alternate between commas/emoji and "and"s.  
Added and implemented `--infinite` aka `-i`: make the program infinitely generate goodnights.  
`-i` is therefore not an alias of `--ignore` any more.  
Created Goodnight class holding the result text and a boolean for `--other-step`'s steps.

### DEV 0.2.7 - Dec 13 2023 [[#60](https://github.com/QuentindiMeo/goodnight.py/commit/52fb39d61c1f5143bc0c9e00628f7f76acdb67ee)]

Added and implemented `--no-copy`, disabling clipboard copy.  
Added `--alternate`.  
Deprecated and removed `--isave`; as `--save` can be combined with `--default`.

### DEV 0.2.6 - Nov 26 2023 [[#56](https://github.com/QuentindiMeo/goodnight.py/commit/40b273f84baaac2488be58acf6c3ce6ec2430545)]

Added and implemented `--save` aka `-S`: save runtime preferences to file.  
Improved largely the code efficiency and its structure, for maintainability.  
Implemented regex handles for arguments interpretation, for clarity.  
Added types on handled exceptions.  
Added [LICENSE](LICENSE.md) file and [issue templates](.github/ISSUE_TEMPLATE).

### DEV 0.2.5 - Nov 13 2023 [[#46](https://github.com/QuentindiMeo/goodnight.py/commit/11c4ee16af7233d136cd283ac1411e9ee1ab37c7)]

Added and implemented `--other-step` aka `-o`: make the program use the even-numbered phrase gaps as "and"s instead of commas.  
Updated usage/help function to reflect additions.  
Set 999 as maximum value for `-n` and `-b` upper bound.  
Adding confirmation prompt if `-n` or `-b` is set to a high value (> 6) through CLI.

---

### DEV 0.2.4 - Nov 09 2023 [[#44](https://github.com/QuentindiMeo/goodnight.py/commit/a9dc5d7f87523405adb64bdb5071a715e0cd5608)]

Added documentation: commenting code, [source.log](assets/source.log) and boosting the [README](README.md).  
Fixed default parameter skip for `-n` and `-b`.

### DEV 0.2.3 - Nov 08 2023 [[#42](https://github.com/QuentindiMeo/goodnight.py/commit/53c4f656d62f88e5c8d29d50c604e59f740b3cb0)]

Improved coding style (ty [SonarLint](https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarlint-vscode)).  
Adjusted [README](README.md) badges.

### DEV 0.2.2 - Nov 06 2023 [[#39](https://github.com/QuentindiMeo/goodnight.py/commit/18fbf246d579934cd737bae7db1bbe6e6d715619)]

Implemented the possibility to have several PHRASES (and others) in a source file.  
Added warning prompt if it is the case, asking if the user wants to continue.

### DEV 0.2.1 - Nov 06 2023 [[#38](https://github.com/QuentindiMeo/goodnight.py/commit/44eae7fdfb83faa957940478f57066c84cb6389d)]

Added nicer transition `"and"` between phrases instead of commas.  
Adjusted the presentation gif.

### DEV 0.2.0 - Nov 06 2023 [[#37](https://github.com/QuentindiMeo/goodnight.py/commit/54af7148d9bebdcc8a61c35a3aea227632081389)]

Implemented phrase picking.  
Added `-r` as an alias of `--allow-repetition`.  
Added a presentation gif to the [README](README.md).

---

### DEV 0.1.6 - Nov 05 2023 [[#34](https://github.com/QuentindiMeo/goodnight.py/commit/01be6a583fa6057cbf1058478a09e4530f21278d)]

Fixed usedEmoji malfunction (picked emoji not removed from list).  
Removed apparent double quotes around every element (e.g. `"phrase"` instead of `phrase`).

### DEV 0.1.5 - Nov 05 2023 [[#33](https://github.com/QuentindiMeo/goodnight.py/commit/89094a5574caa2a08110802dedd311595f22a592)]

Fixed multioptional parameters oddity: disallowing long parameters and their aliases.  
Removed CLI asking for parameters that are already set by the preferences file.

### DEV 0.1.4 - Nov 05 2023 [[#31](https://github.com/QuentindiMeo/goodnight.py/commit/2565370818018ce4cb477d1e8053a36f0dae44ac)]

Implemented emoji picking.  
Improved context verbosity and prints quality on `--verbose`.  
Fixed missing file extraction case on `--allow-repetition`.

### DEV 0.1.3 - Nov 05 2023 [[#29](https://github.com/QuentindiMeo/goodnight.py/commit/444a8e9a7d7c45cffa12499df67ff5aeef7e34f0)]

Added and implemented `--allow-repetition`:.  
.  .  allow the same phrase to be picked several times if all other phrases have been picked
Implemented nickname picking.  
Created a Contents class that holds the source file's contents, for clarity.  
Fixed some `-n` and `-b` oddities.

### DEV 0.1.2 - Nov 04 2023 [[#28](https://github.com/QuentindiMeo/goodnight.py/commit/48a3e2c0c6c94448519df2fe1e7ee2ff1ab89455)]

Added and implemented `--default`: using default values for all parameters.  
Added warning if a high upper bound / value is set for `-b`/`-n`.  
Fixed CLI oddities: unhandled parameter exceptions.  
Added links on [README](README.md) badges.

### DEV 0.1.1 - Nov 03 2023 [[#23](https://github.com/QuentindiMeo/goodnight.py/commit/3765c815fdc011277158463dc96c16ae657c11b0)]

Added and implemented `--isave`: ignore preferences, save CLI answers as preferences.  
Added possibility to set a random range as a value nbPhrases (picks a random number between the two bounds)

### DEV 0.1.0 - Nov 02 2023 [[#21](https://github.com/QuentindiMeo/goodnight.py/commit/d3bcec6595ce4866b7c1e4193299b202992ddcc8)]

Added weighting feature to source extractor (Contents class).  
Renamed `--debug` to `--verbose`.  
Major [README](README.md) overhaul.

---

### DEV 0.0.5 - Nov 01 2023 [[#19](https://github.com/QuentindiMeo/goodnight.py/commit/b8cc6aa66eb0b09b83b8b0ea8804d0d6c8edf87b)]

Added and implemented `--debug`: a mode that prints the program's steps.  
Added nicknames to source extractor.  
Deprecated and removed `-D`.  
Created Types file with type aliases for clarity.

### DEV 0.0.4 - Nov 01 2023 [[#11](https://github.com/QuentindiMeo/goodnight.py/commit/eea6d3ba7795842126740a9ebef5078f0cdcd009)]

Completed implementation of `-s` (source file selection).  
Added a sources extractor (phrases, emoji).  
Added multioptional parameters handling for boolean parameters (e.g. `-eD`).

### DEV 0.0.3 - Nov 01 2023 [[#8](https://github.com/QuentindiMeo/goodnight.py/commit/66202eb8dc85328ca37ceaa278d631fba45c5a79)]

Added `-s` (implementation in progress).  
Added preferences.sav file: save to it with `-D`, ignore its contents with `-i`/`--ignore`.  
Added a Ctrl+C handler, exiting the program gracefully with a context message.

### DEV 0.0.2 - Oct 31 2023 [[#6](https://github.com/QuentindiMeo/goodnight.py/commit/5da4d12644290f576cc462df6057c9c9770e224a)]

Added parameter handling under forms `-X` and `--XXX`.  
Completed setup for Exit and Help.

### DEV 0.0.1 - Oct 30 2023 [[#4](https://github.com/QuentindiMeo/goodnight.py/commit/2682ee6f539a30452187c110552fa49d5f014d34)]

Added Parameters class to handle and hold program parameters.  
Added and implemented `-n` (number of phrases to draw), `-e` (toggle emoji mode), `-w` (for whom).  
Adding first elementary components.

### DEV 0.0.0 - Oct 30 2023 [[#1](https://github.com/QuentindiMeo/goodnight.py/commit/10593fa32045e11cfd8621fe0bf106547ce16f80)]

Project creation.

<br />

[Back to top](#top)
