from src.reader.reader import read
from src.processor.processor import process
from src.writer.writer import write
import argparse

def read_arguments():
    parser = argparse.ArgumentParser(description='Events Aggregated per minute')
    parser.add_argument('--input_file', required=True, type=str, help='Input file')
    parser.add_argument('--window_size', required=True, type=int, help='Window Size')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = read_arguments()
    df = read(args.input_file)
    out_frame = process(df, args.window_size)
    write(out_frame)
