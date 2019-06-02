## Steps
1. Clone the repo
    ```git clone https://github.com/ichux/backend-engineering-challenge.git```

2. Create a virtual environment, activate it and *cd* into the cloned repository to run
    ```pip install -r requirements.txt```

3. to run the application
```console
python unbabel_cli.py --input_file INPUT_FILE --window_size WINDOW_SIZE
[--output_file OUTPUT_FILE] [--client_name CLIENT_NAME]
```

#### Parameters
```
--input_file == (compulsory) the data to be evaluated
--window_size == (compulsory) the time gap size in minutes
--output_file == (optional) output file to save the results to
--client_name == (optional) to filter your data by a client's name
```