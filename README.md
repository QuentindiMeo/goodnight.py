<div align="center" id="top">
    <h1>🌙 goodnight.py 🌙</h1>
</div>

<div align="center">
    <a href="#full_moon_with_face-description">Description</a> &#xa0; | &#xa0;
    <a href="#city_sunset-usage">Usage</a> &#xa0; | &#xa0;
    <a href="#paperclips-compatability">Compatability</a> &#xa0; | &#xa0;
    <a href="#card_file_box-change-log">Change log</a>
</div>
&#xa0;
<div align="center">
    <a href="#top"><img alt="Python version" src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" /></a>
    <a href="#card_file_box-change-log"><img alt="Last version released" src="https://img.shields.io/badge/release-v0.2.6-blue?logo=windows-terminal" /></a>
    <a href="https://github.com/QuentindiMeo/goodnight.py/commits/main"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/QuentindiMeo/goodnight.py?color=blueviolet&logo=clarifai" /></a>
    <a href="#top"><img alt="Lines of code" src="https://tokei.rs/b1/github/QuentindiMeo/goodnight.py?category=code" /></a>
    <!-- <img alt="Lines of code" src="https://img.shields.io/tokei/lines/github/QuentindiMeo/goodnight.py?color=green&logo=haveibeenpwned" /> -->
    <!-- <img alt="TODO" src="https://img.shields.io/endpoint?url=https://todos.tickgit.com/badge?repo=github.com/quentindimeo/goodnight.py" /> -->
</div>
<div align="center">
    <a href="https://github.com/QuentindiMeo/goodnight.py/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/QuentindiMeo/goodnight.py?color=yellow&logo=github" /></a>
    <a href="https://github.com/QuentindiMeo/goodnight.py/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/QuentindiMeo/goodnight.py?color=forestgreen&logo=target" /></a>
    <a href="https://github.com/QuentindiMeo/goodnight.py/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/QuentindiMeo/goodnight.py?color=red&logo=stackedit" /></a>
    <a href="#top"><img alt="GitHub repository size" src="https://img.shields.io/github/languages/code-size/quentindimeo/goodnight.py?color=blue&logo=frontify" /></a>
</div>
&#xa0;
<div align="center" width="75%">
    <a href="#top"><abbr title="Demonstration v0.2.0">
    <img alt="Demo v0.2.0" src="./assets/demo_head.gif" />
    </abbr></a>
</div>
<div align="center">
    <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=Z9V98YGZMK8CU">
    <img alt="PayPal donate button" src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" width="22%" />
    </a>
</div>
&#xa0;

## :full_moon_with_face: Description

No need to think about not being repetitive in the way you say "Good night" any more!  
Just run this script and it will generate a random goodnight message for your loved one.  
The author of this script declines all responsibility for any conflict caused by the (over)use of this script. :wink:

> [!NOTE]
> Don't hesitate and report any kind of malfunction or request a feature by [**opening an issue**](https://github.com/QuentindiMeo/goodnight.py/issues)!

&#xa0;

## :city_sunset: Usage

&nbsp;&nbsp; :checkered_flag:&nbsp; **Launch**

``` bash
python goodnight.py [OPTIONS]
```

&#xa0;

&nbsp;&nbsp; :hammer_and_wrench:&nbsp; **Options**

``` txt
--default               Launch once with default values (ignores other parameters)
--no-copy               Do not copy the result to clipboard

-b, --bounds     (x,y)  Bounds for the random range of how many phrases to draw (def: 2,5)
-n, --nb-phrases <int>  Number of phrases to draw
-e, --emoji             Add emoji after each phrase (from source file)
-s, --source     <str>  Source file to pull contents (phrases...) from (def: ./assets/source.log)
-w, --for-whom   <str>  For whom the goodnight is (def: "" [no name used])

-r, --allow-repetition  Allow repetition of phrases if you ask for more than there are in the source file
-o, --other-step        Use the even-numbered phrase gaps as "and"s instead of commas (def: odd-)
-a, --alternate         Alternate between "and"s, and emoji instead of commas (requires -e, def: False)
-i, --ignore            Ignore preferences (preferences.sav file)
-S, --save              Save preferences to file (preferences.sav)

--verbose               Toggle verbose mode
-h, --help              Display this help and exit
```

&#xa0;

&nbsp;&nbsp; :hotsprings:&nbsp; **Default behavior** / its equivalents

``` bash
python goodnight.py --bounds "2,5" --source "./assets/source.log" --for-whom ""
python goodnight.py -b "2,5" -s "assets/source" -w ""
python goodnight.py --default
```

&#xa0;

&nbsp;&nbsp; :bookmark_tabs:&nbsp; **General Information**

- Fear not having to copy the result of the program, it will be automatically **copied to your clipboard**! :wink: (unless [`--no-copy`](#city_sunset-usage) is present)
- Your preferences are **automatically saved** upon the first launch unless specified otherwise (see above: [`-i`](#city_sunset-usage)).
  - Settings will be set based on parameters; if none is provided, they will be based on the preference file; if there is none, the CLI will ask you for them.
- Though Ctrl+D cannot be caught in this script, you can **use Ctrl+C** to exit at any time.
- [`-b`](#city_sunset-usage) and [`-n`](#city_sunset-usage) are mutually exclusive. If both are provided, the program will exit with an error.
- [`-o`](#city_sunset-usage) naturally has no effect if there is only one phrase or [`-e`](#city_sunset-usage) is present.
- A file named [source.log](./assets/source.log) serves as the default source file for phrases, emoji and nicknames.
  - You may create your own `.log` source file (see above: [`-s`](#city_sunset-usage)). Open the default source file to see how to format it.
  - You don't need to specify the `.log` in the source file path, the program can add it for you.
- If nicknames are provided in said source file, they will override the [`--for-whom`](#city_sunset-usage) option.

&#xa0;

## :paperclips: Compatability

This program was tested on and designed for WSL2 and Ubuntu 22.04.

> [!CAUTION]
> **goodnight.py**'s code is written in Python **3.10** and is **not** compatible with anterior versions.

&#xa0;

## :card_file_box: Change log

- ***[DEV 0.0.0]** Oct 30 2023* - Project creation
- ***[DEV 0.0.1]** Oct 30 2023* - Added Parameters class (-new) and first elementary components
- ***[DEV 0.0.2]** Oct 31 2023* - Added parameter handling (- and --), Exit and Help setup
- ***[DEV 0.0.3]** Nov 01 2023* - Added -s (wip), preferences.sav with -D and -i, Ctrl+C handler
- ***[DEV 0.0.4]** Nov 01 2023* - Added sources extractor (phrases, emoji), multioptional parameters handling
- ***[DEV 0.0.5]** Nov 01 2023* - Added nicknames to source extractor; removed -D, added --debug; added Types for clarity
- ***[DEV 0.1.0]** Nov 02 2023* - Added weighting feature to source extractor (Contents class); renamed --debug as --verbose
- ***[DEV 0.1.1]** Nov 03 2023* - Added possibility to set a random range as nbPhrases, added --isave
- ***[DEV 0.1.2]** Nov 04 2023* - Fixed CLI oddities; added warning if high upper bound on range, --default, links on README badges
- ***[DEV 0.1.3]** Nov 05 2023* - Fixed -n/-b oddities; added and implemented --allow-repetition and nickname picking
- ***[DEV 0.1.4]** Nov 05 2023* - Added emoji picking, improved --verbose, fixed missing file extraction case
- ***[DEV 0.1.5]** Nov 05 2023* - Fixed multi-optional param oddity, removed CLI need for parameters set by file
- ***[DEV 0.1.6]** Nov 05 2023* - Fixed usedEmoji malfunction, removed "s surrounding every element
- ***[DEV 0.2.0]** Nov 06 2023* - Added phrase picking, added -r as alias for --allow-repetition, presentation gif
- ***[DEV 0.2.1]** Nov 06 2023* - Adjusted gif, adding nicer transition "and" between phrases
- ***[DEV 0.2.2]** Nov 06 2023* - Added possibility to have several PHRASES (and others) in source file
- ***[DEV 0.2.3]** Nov 08 2023* - Minor coding style improvements (ty SonarLint), README adjustments
- ***[DEV 0.2.4]** Nov 09 2023* - Adding some documentation, fixing default parameter r/n skip
- ***[DEV 0.2.5]** Nov 13 2023* - Adding --other-step; updating usage/help; setting 999 as max r/n bound
- ***[DEV 0.2.6]** Nov 26 2023* - Adding --save; improving largely code efficiency and structure for maintainability
- ***[DEV 0.2.7]** Dec ?? 2023* - Adding --alternate, --no-copy, --infinite; removing --isave
- ***[REL 1.0.0]** Dec ?? 2023* - First release; major README update

<br />

[Back to top](#top)
