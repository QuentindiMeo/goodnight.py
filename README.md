# goodnight.py

## Description

No need to think about not being repetitive with your "gn"s any more!  
Just run this script and it will generate a random goodnight message for your loved one.  
The author of this script declines all responsibility for any conflict caused by the (over)use of this script.

## Usage

- **Launch**

``` bash
python goodnight.py [OPTIONS]
```

- **Options**

``` bash
-n, --nb-fragments <int>  Number of fragments to draw (def: 2..4)
-e, --emoji               Add emoji between fragments (def: False)
-s, --source       <str>  Source file to read fragments and emoji from (def: [source.log](./source.log))
-w, --for-whom     <str>  For whom the goodnight is (def: "")
-D                 Set used parameters as preferences ([preferences.sav](./preferences.sav))
-i, --ignore       Ignore preferences ([preferences.sav](./preferences.sav))
-h, --help         Display this help and exit
```

*-D and -i are mutually exclusive; they cannot be used conjointly.*

- **General**

Your preferences are automatically saved upon the first launch unless specified otherwise *(see above: -i)*.  
A file named [source.log](./source.log) serves as the default source file for fragments and emoji, you may create your own *(see above: -s)*.  
If nicknames are provided in the source file, they will override the --for-whom option.  
As Ctrl+D cannot be caught in this script, you can use Ctrl+C to exit the script at any time.

## Compatability

This script is written in Python 3.10+ and is not backwards compatible with Python 2.x.  
It was tested on and designed for Windows 10 and Ubuntu 22.04.

## Project log

- ***[D 0.0.0]** Oct 30 2023* - Project creation
- ***[D 0.0.1]** Oct 30 2023* - Adding Parameters class (-new) and first elementary components
- ***[D 0.0.2]** Oct 31 2023* - Adding parameter handling (- and --), Exit and Help setup
- ***[D 0.0.3]** Nov 01 2023* - Adding -s (wip), preferences.sav with -D and -i, Ctrl+C handler
- ***[D 0.0.5]** Nov 01 2023* - Adding sources extractor (phrases and emoji); no nicknames yet [bug]
