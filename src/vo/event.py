class Event:
    def __int__(self, timestamp, translation_id, source_language, target_language, client_name, event_name, nr_words,
                duration):
        self.timestamp = timestamp
        self.translation_id = translation_id
        self.source_language = source_language
        self.target_language = target_language
        self.client_name = client_name
        self.event_name = event_name
        self.nr_words = nr_words
        self.duration = duration

