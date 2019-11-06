import argparse
import os
from lib.event_processor.event_processor import EventProcessor
from lib.event_reader.event_reader import EventReader
from lib.input.reader import Reader
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input-file", type=str,
                    help="the stream of events, should be .json file", required = True)
    parser.add_argument("-w","--window-size", type=int,
                    help="the window size in minutes", required = True)
    args = parser.parse_args()
    
    reader = Reader(args.input_file, args.window_size)
    input_data = reader.read_input()

    if input_data == False:
        return "Failed to read input-file or window-size"

    processor = EventProcessor(input_data.get("file"), EventReader())
    output_list = processor.calculate_date_range(input_data.get("window_size"))
    invalid_events = processor.get_events_with_invalid_data()
    
    if len(invalid_events) > 0:
        print("Some events had invalid data, please review these events:")
        for event in invalid_events:
            print(event)

    print("Check the output:")
    for output in output_list:
        print(output)
    

if __name__ == "__main__":
    main()

