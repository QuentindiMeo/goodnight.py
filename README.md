<div align="center" id="top">
    <h1 markdown="1">:crescent_moon: goodnight.py :crescent_moon:</h1>
</div>

<div align="center">
    <a href="#full_moon_with_face-description">Description</a> &#xa0; | &#xa0;
    <a href="#city_sunset-usage">Usage</a> &#xa0; | &#xa0;
    <a href="#paperclips-compatability">Compatability</a> &#xa0; | &#xa0;
    <a href="#card_file_box-project-log">Project log</a>
</div>
&#xa0;
<div align="center">
    <img alt="Python version" src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
    <img alt="Development status" src="https://img.shields.io/badge/development-v0.1.0-blue?logo=windows-terminal" />
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/QuentindiMeo/goodnight.py?color=blueviolet&logo=clarifai" />
    <img alt="GitHub repository size" src="https://img.shields.io/github/repo-size/QuentindiMeo/goodnight.py?color=blue&logo=frontify" />
</div>
<div align="center">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/QuentindiMeo/goodnight.py?color=yellow&logo=github" />
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/QuentindiMeo/goodnight.py?color=green&logo=target" />
    <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/QuentindiMeo/goodnight.py?color=red&logo=stackedit" />
    <!-- <img alt="Lines of code" src="https://img.shields.io/tokei/lines/github/QuentindiMeo/goodnight.py?color=green&logo=haveibeenpwned" /> -->
</div>
&#xa0;

## :full_moon_with_face: Description

No need to think about not being repetitive in the way you say "Good night" any more!  
Just run this script and it will generate a random goodnight message for your loved one.  
The author of this script declines all responsibility for any conflict caused by the (over)use of this script. :wink:

## :city_sunset: Usage

&nbsp;&nbsp; :checkered_flag:&nbsp; **Launch**

``` bash
python goodnight.py [OPTIONS]
```

&#xa0;

&nbsp;&nbsp; :hammer_and_wrench:&nbsp; **Options**

``` bash
-n, --nb-phrases <int>  Number of phrases to draw (def: 2..5)
-e, --emoji             Add emoji between phrases (def: False)
-s, --source     <str>  Source file to read phrases and emoji from (def: source.log)
-w, --for-whom   <str>  For whom the goodnight is (def: "" (no name used))
--verbose               Toggle verbose mode (def: False)

-i, --ignore            Ignore preferences (preferences.sav file) (def: False)
-h, --help              Display this help and exit
```

&#xa0;

&nbsp;&nbsp; :test_tube:&nbsp; **General**

Your preferences are automatically saved upon the first launch unless specified otherwise *(see above: -i)*.  
A file named [source.log](./source.log) serves as the default source file for phrases, emoji and nicknames. You may create your own source file *(see above: -s)*. Open the default source file to see how to format it.  
If nicknames are provided in said source file, they will override the `--for-whom` option.  
As Ctrl+D cannot be caught in this script, you can use Ctrl+C to exit at any time.

## :paperclips: Compatability

This script is written in Python 3.10+ and is not backwards compatible with Python 2.x.  
It was tested on and designed for Windows 10 and Ubuntu 22.04.

## :card_file_box: Project log

- ***[DEV 0.0.0]** Oct 30 2023* - Project creation
- ***[DEV 0.0.1]** Oct 30 2023* - Added Parameters class (-new) and first elementary components
- ***[DEV 0.0.2]** Oct 31 2023* - Added parameter handling (- and --), Exit and Help setup
- ***[DEV 0.0.3]** Nov 01 2023* - Added -s (wip), preferences.sav with -D and -i, Ctrl+C handler
- ***[DEV 0.0.4]** Nov 01 2023* - Added sources extractor (phrases, emoji), handles multioptional parameters
- ***[DEV 0.0.5]** Nov 01 2023* - Added nicknames to source extractor, removed -D, added --debug, added Types for clarity
- ***[DEV 0.1.0]** Nov 02 2023* - Added weighting feature to source extractor (Contents class), renamed --debug as --verbose

<br/>

[Back to top](#top)
