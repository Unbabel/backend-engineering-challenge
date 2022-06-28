from src.reader import read_json
import argparse
# Press the green button in the gutter to run the script.
# For each iteration I'll have the current timestamp - window size
# every minute will compare:
# 1. if no data available avg_delivered_time = 0
# 2. if data is available I have to track how many translation already happened and sum the time of those translations
# to get the avg
# 3. handle edge cases
# 4. create output
# 4. unit tests

def processEvents(df):
    pass


if __name__ == '__main__':
    df = read_json('files/events.json', )
    processEvents(df)

