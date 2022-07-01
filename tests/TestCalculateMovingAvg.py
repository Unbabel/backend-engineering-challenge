import unittest

import pandas as pd

from src.processor import processor


class TestCalculateMovingAvg(unittest.TestCase):

    def test_moving_avg_do_not_overlap(self):
        expected_output = [
            {
                "dates": "2018-12-26 18:11:00",
                "duration": 0
            },
            {
                "dates": "2018-12-26 18:12:00",
                "duration": 20.0
            },
            {
                "dates": "2018-12-26 18:13:00",
                "duration": 20.0
            },
            {
                "dates": "2018-12-26 18:14:00",
                "duration": 31.0
            },
        ]
        input_data = dict()
        input_data = [
            {
                "timestamp": "2018-12-26 18:11:08.509654",
                "translation_id": "5aa5b2f39f7254a75aa5",
                "source_language": "en",
                "target_language": "fr",
                "client_name": "easyjet",
                "event_name": "translation_requested",
                "nr_words": 30,
                "duration": 20
            },
            {
                "timestamp": "2018-12-26 18:13:19.903159",
                "translation_id": "5aa5b2f39f7254a75aa4",
                "source_language": "en",
                "target_language": "fr",
                "client_name": "easyjet",
                "event_name": "translation_delivered",
                "nr_words": 30,
                "duration": 31
            }
        ]
        df = pd.DataFrame(input_data)
        expected_df = pd.DataFrame(expected_output)
        expected_df['dates'] = expected_df['dates'].astype('datetime64[s]')
        output = processor.process(df, 2)
        pd.testing.assert_frame_equal(output.reset_index(drop=True), expected_df.reset_index(drop=True),
                                      check_names=False)

    def test_moving_avg_with_example_readme(self):
        expected_output = [
            {"dates": "2018-12-26 18:11:00", "duration": 0.0},
            {"dates": "2018-12-26 18:12:00", "duration": 20.0},
            {"dates": "2018-12-26 18:13:00", "duration": 20.0},
            {"dates": "2018-12-26 18:14:00", "duration": 20.0},
            {"dates": "2018-12-26 18:15:00", "duration": 20.0},
            {"dates": "2018-12-26 18:16:00", "duration": 25.5},
            {"dates": "2018-12-26 18:17:00", "duration": 25.5},
            {"dates": "2018-12-26 18:18:00", "duration": 25.5},
            {"dates": "2018-12-26 18:19:00", "duration": 25.5},
            {"dates": "2018-12-26 18:20:00", "duration": 25.5},
            {"dates": "2018-12-26 18:21:00", "duration": 25.5},
            {"dates": "2018-12-26 18:22:00", "duration": 31.0},
            {"dates": "2018-12-26 18:23:00", "duration": 31.0},
            {"dates": "2018-12-26 18:24:00", "duration": 42.5}
        ]
        input_data = dict()
        input_data = [
            {"timestamp": "2018-12-26 18:11:08.509654", "translation_id": "5aa5b2f39f7254a75aa5",
             "source_language": "en", "target_language": "fr", "client_name": "easyjet",
             "event_name": "translation_delivered", "nr_words": 30, "duration": 20},
            {"timestamp": "2018-12-26 18:15:19.903159", "translation_id": "5aa5b2f39f7254a75aa4",
             "source_language": "en", "target_language": "fr", "client_name": "easyjet",
             "event_name": "translation_delivered", "nr_words": 30, "duration": 31},
            {"timestamp": "2018-12-26 18:23:19.903159", "translation_id": "5aa5b2f39f7254a75bb33",
             "source_language": "en", "target_language": "fr", "client_name": "booking",
             "event_name": "translation_delivered", "nr_words": 100, "duration": 54}
        ]
        df = pd.DataFrame(input_data)
        expected_df = pd.DataFrame(expected_output)
        expected_df['dates'] = expected_df['dates'].astype('datetime64[s]')
        output = processor.process(df, 10)
        pd.testing.assert_frame_equal(output.reset_index(drop=True), expected_df.reset_index(drop=True),
                                      check_names=False)

    def test_with_duplicate(self):
        expected_output = [
            {"dates": "2018-12-26 18:11:00", "duration": 20.0},
            {"dates": "2018-12-26 18:12:00", "duration": 20.0},
            {"dates": "2018-12-26 18:13:00", "duration": 20.0},
            {"dates": "2018-12-26 18:14:00", "duration": 20.0},
            {"dates": "2018-12-26 18:15:00", "duration": 20.0},
            {"dates": "2018-12-26 18:16:00", "duration": 25.5},
            {"dates": "2018-12-26 18:17:00", "duration": 25.5},
            {"dates": "2018-12-26 18:18:00", "duration": 25.5},
            {"dates": "2018-12-26 18:19:00", "duration": 25.5},
            {"dates": "2018-12-26 18:20:00", "duration": 25.5},
            {"dates": "2018-12-26 18:21:00", "duration": 31.0},
            {"dates": "2018-12-26 18:22:00", "duration": 31.0},
            {"dates": "2018-12-26 18:23:00", "duration": 31.0},
            {"dates": "2018-12-26 18:24:00", "duration": 42.5}
        ]

        input_data = dict()
        input_data = [
            {"timestamp": "2018-12-26 18:11:00.00000", "translation_id": "5aa5b2f39f7254a75aa5",
             "source_language": "en", "target_language": "fr", "client_name": "easyjet",
             "event_name": "translation_delivered", "nr_words": 30, "duration": 20},
            {"timestamp": "2018-12-26 18:15:19.903159", "translation_id": "5aa5b2f39f7254a75aa4",
             "source_language": "en", "target_language": "fr", "client_name": "easyjet",
             "event_name": "translation_delivered", "nr_words": 30, "duration": 31},
            {"timestamp": "2018-12-26 18:23:19.903159", "translation_id": "5aa5b2f39f7254a75bb33",
             "source_language": "en", "target_language": "fr", "client_name": "booking",
             "event_name": "translation_delivered", "nr_words": 100, "duration": 54}
        ]
        df = pd.DataFrame(input_data)
        expected_df = pd.DataFrame(expected_output)
        expected_df['dates'] = expected_df['dates'].astype('datetime64[s]')
        print(expected_df)
        output = processor.process(df, 10)
        pd.testing.assert_frame_equal(output.reset_index(drop=True), expected_df.reset_index(drop=True),
                                      check_names=False)


if __name__ == '__main__':
    unittest.main()
