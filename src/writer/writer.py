import json

WRITING_PERMISSIONS = "w"


def write(moving_average_list, output_file):
    with open(output_file, WRITING_PERMISSIONS, encoding='utf-8') as output:
        json.dump(moving_average_list, output, ensure_ascii=False, indent=4)
