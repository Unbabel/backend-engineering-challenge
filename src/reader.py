import json

def file_input_reader(filename):
    with open(filename, 'r') as f:
        result = f.readline()
        while result:
            yield json.loads(result)
            result = f.readline()