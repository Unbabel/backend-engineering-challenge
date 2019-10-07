# Backend Engineering Challenge

## Notes

Script was devided in four parts:
1. `get_command_args()`: where command line args are read
2. `read_input_file(args.input_file)`: where input data is load
3. `cacl_avg_delivery_time(data, args.window_size)`: where the core calculation is performed
4. `write_output_file(result)`: where results are written to a file named 'outputfile.json' 


## How to run

Execute the following command for Windows OS

```unbabel_cli.exe --input_file events.json --window_size 10```

Execute the following command for OSx

```./unbabel_cli --input_file events.json --window_size 10```

- `input_file`: contains the path for the input file
- `window_size`: should be an integer greater than 0, it denotes the window size in minutes

## Improvements found
- Handle big files
- Handle sparse timestamps (what if input_file contains timestamps from different years?)
- Handle missing/noisy data


