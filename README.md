# :crescent_moon: <center>goodnight.py</center> :crescent_moon:

<div align="center" markdown="1">
    [Description](#full_moon_with_face-description) &#xa0; | &#xa0;
    [Usage](#city_sunset-usage) &#xa0; | &#xa0;
    [Compatability](#linked_paperclips-compatability) &#xa0; | &#xa0;
    [Project log](#card_file_box-project-log) &#xa0; | &#xa0;
</div>
<div align="center" markdown="1">
    ![GitHub top language](https://img.shields.io/github/languages/top/QuentindiMeo/goodnight.py?color=blue)
    ![Development status](https://img.shields.io/badge/development-WIP-blue)
    ![GitHub stars](https://img.shields.io/github/stars/QuentindiMeo/goodnight.py?color=yellow)
    ![GitHub last commit](https://img.shields.io/github/last-commit/QuentindiMeo/goodnight.py?color=blueviolet)
    ![GitHub contributors](https://img.shields.io/github/contributors/QuentindiMeo/goodnight.py?color=green)
    ![GitHub issues](https://img.shields.io/github/issues/QuentindiMeo/goodnight.py?color=red)
    ![Repository size](https://img.shields.io/github/repo-size/QuentindiMeo/goodnight.py?color=blue)
    ![Lines of code](https://img.shields.io/tokei/lines/github/QuentindiMeo/goodnight.py?color=green)
</div>

## :full_moon_with_face: Description

No need to think about not being repetitive in the way you say "Good night" any more!  
Just run this script and it will generate a random goodnight message for your loved one.  
The author of this script declines all responsibility for any conflict caused by the (over)use of this script.

## :city_sunset: Usage

- :checkered_flag: **Launch**

``` bash
python goodnight.py [OPTIONS]
```

- :hammer_and_wrench: **Options**

``` bash
-n, --nb-fragments <int>  Number of fragments to draw (def: 2..5)
-e, --emoji               Add emoji between fragments (def: False)
-s, --source       <str>  Source file to read fragments and emoji from (def: source.log)
-w, --for-whom     <str>  For whom the goodnight is (def: "" (no name used))

-i, --ignore              Ignore preferences (preferences.sav file) (def: False)
--debug                   Debug mode (def: False)
-h, --help         Display this help and exit
```

- :test_tube: **General**

Your preferences are automatically saved upon the first launch unless specified otherwise *(see above: -i)*.  
A file named [source.log](./source.log) serves as the default source file for fragments and emoji, you may create your own *(see above: -s)*.  
If nicknames are provided in said source file, they will override the `--for-whom` option.  
As Ctrl+D cannot be caught in this script, you can use Ctrl+C to exit at any time.

## :linked_paperclips: Compatability

This script is written in Python 3.10+ and is not backwards compatible with Python 2.x.  
It was tested on and designed for Windows 10 and Ubuntu 22.04.

## :card_file_box: Project log

- ***[D 0.0.0]** Oct 30 2023* - Project creation
- ***[D 0.0.1]** Oct 30 2023* - Added Parameters class (-new) and first elementary components
- ***[D 0.0.2]** Oct 31 2023* - Added parameter handling (- and --), Exit and Help setup
- ***[D 0.0.3]** Nov 01 2023* - Added -s (wip), preferences.sav with -D and -i, Ctrl+C handler
- ***[D 0.0.4]** Nov 01 2023* - Added sources extractor (phrases, emoji), handles multioptional parameters
- ***[D 0.0.5]** Nov 01 2023* - Added nicknames to source extractor, removed -D, added --debug, added Types for clarity

&#xa0;

[Back to top](#top)
