from lib.event_reader.event_reader import EventReader
import unittest
import json

class EventReaderTest(unittest.TestCase):
    """Event Reader unit test."""
    
    def setUp(self):
        self.event_reader = EventReader()

    def test_validate_timestamp_when_has_a_invalid_timestamp(self):
        event_sample = json.loads('{"timestamp": "2018-12-26T18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}')
        
        self.assertFalse(self.event_reader.validate_timestamp(event_sample))

    def test_validate_timestamp_when_doenst_have_timestamp(self):
        event_sample = json.loads('{"translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}')

        self.assertFalse(self.event_reader.validate_timestamp(event_sample))

    def test_validate_duration_when_duration_is_not_numeric(self):
        event_sample = json.loads('{"translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": "abs"}')

        self.assertFalse(self.event_reader.validate_duration(event_sample))
    
    def test_validate_duration_when_doesnt_have_duration(self):
        event_sample = json.loads('{"translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30}')
        
        self.assertFalse(self.event_reader.validate_duration(event_sample))
    
    def test_validate_duration_with_valid_duration(self):
        event_sample = json.loads('{"translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}')
        
        self.assertTrue(self.event_reader.validate_duration(event_sample))

    def test_validate_event_json(self):
        event_sample = json.loads('{"timestamp": "2018-12-26 18:11:08.509654", "translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}')
        
        self.assertTrue(self.event_reader.validate(event_sample))

if __name__ == '__main__':
    unittest.main()
    