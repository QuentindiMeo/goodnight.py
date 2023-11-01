# goodnight.py

## Description

// TODO

## Usage

- **Launch**

```bash
python goodnight.py [OPTIONS]
```

- **Options**

```bash
-n, --nb-fragments <int>  Number of fragments to draw (def: 2..4)
-e, --emoji        <bool> Add emoji between fragments (def: false)
-s, --source       <str>  Source file to read fragments and emoji from (def: source.log)
-w, --for-whom     <str>  For whom the goodnight is (def: \"\")
-h, --help         Display this help and exit
```

## Compatability

This script is written in Python 3.10+ and is not backwards compatible with Python 2.x.
It was tested on and designed for Windows 10 and Ubuntu 22.04.

## Project log

- *[D 0.0.0] Oct 30 2023* - Project creation
- *[D 0.0.1] Oct 30 2023* - Adding Parameters class (-new) and first elementary components
- *[D 0.0.2] Oct 31 2023* - Adding parameter handling (- and --), Exit enum setup
- *[D 0.0.3] Nov 01 2023* - Adding -s (wip), Ctrl+C handler
