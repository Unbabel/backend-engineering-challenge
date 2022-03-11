# Backend Engineering Challenge

[Challenge description](docs/challenge.md)

### Project requirements:
- Python 3.7
- Pip (at least 20)

### (Quick) Setup 
Install the package using `pip` 
```
$ pip install -e . 
```

Note: it's recommended to create a new virtual environment
```
python3 -m venv env
```

### Run
```
usage: unbabel_cli [-h] -f INPUT_DATA [-w WINDOW_SIZE] [-o OUTPUT_FILE_NAME]

optional arguments:
  -h, --help            Command Line interface to compute (moving) average
                        time of a given metrics file based on a window size
  -f INPUT_DATA, --file INPUT_DATA
                        File path with translation metrics data
  -w WINDOW_SIZE, --window_size WINDOW_SIZE
                        Moving window size in minutes (should be >0)
  -o OUTPUT_FILE_NAME, --output_file OUTPUT_FILE_NAME
                        Filename to output data. If none, data will be printed
                        to the console

```

Example
```
unbabel_cli -f data/data_9k.json -o output_9k.json
```

### Project Notes
For this challenge I tried to keep things as simple as possible, as well 
as performant.
I used a python dict to store the data from the file, using the 
uniqueness of the `key` to store the minutes values as a datetime object.
This way I could join all minutes under the same dict position. Then, for each
minute in data file, a dictionary of data is stored (duration, counts and no_words).

For istance: 
```
_dict = {datetime.datetime(2022, 03, 10, 11, 00) : {"duration": 20, "counts": 2}}
```

After the dict is complete (EOF reached), a for loop performs the average window
filter, subtracting and search 10 minutes with step of 1. This mechanism os not 
performant, but since there's no warranty that that is provided ordered by timestamp, 
this is the best compromise I found (the alternative would be a sort, that 
could bring serious problems on large datasets). 

The output can be written to a file or to the console log. 

Using the standard lib objects (avoiding
complex objects, or complex toolboxes like pandas or numpy) 
allowed to keep the performance and lower the memory 
consumption. Although memory may not be a problem with small data-sets, it can
become a nightmare if we try to process tons of data.

Unde the `data` directory, two files can be found: one containing 16 entrys and 
one containing 9000 entrys.
Although 9k is a small number, it is significan to confirm the performance of this
software. More tests should be carried on.

An issue that I consider important is with the input file. Although each line can be
in a json format, the whole file isn't. This way, it's not possible to use
some bootstrap methods such as [ijson](https://pypi.org/project/ijson/).
