package com.chris.unbabel.avgserver.core;

import com.chris.unbabel.avgserver.util.DateUtils;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.text.ParseException;

import static org.hamcrest.Matchers.is;
import static org.junit.Assert.assertThat;

public class TranslationDeliveredTest {
    private static final ObjectMapper MAPPER = new ObjectMapper();
    private static final String JSON = "{\"timestamp\": \"2018-12-26 18:23:19.903159\",\"translation_id\": \"5aa5b2f39f7254a75bb33\",\"source_language\": \"en\",\"target_language\": \"fr\",\"client_name\": \"booking\",\"event_name\": \"translation_delivered\",\"nr_words\": 100, \"duration\": 54}\n";

    private TranslationDelivered sample;

    @Before
    public void setUp() throws ParseException {
        sample = new TranslationDelivered();

        sample.setTimestamp(DateUtils.parse("2018-12-26 18:23:19.903159"));
        sample.setClientName("booking");
        sample.setEventName("translation_delivered");
        sample.setNrWords(100);
        sample.setSourceLanguage("en");
        sample.setTargetLanguage("fr");
        sample.setDuration(54.0D);
        sample.setTranslationId("5aa5b2f39f7254a75bb33");
    }

    @Test
    public void testUnMarshall() throws IOException {
        final TranslationDelivered delivered = MAPPER.readValue(JSON, TranslationDelivered.class);

        assertThat(delivered.getTimestamp(), is(sample.getTimestamp()));
        assertThat(delivered.getClientName(), is(sample.getClientName()));
        assertThat(delivered.getEventName(), is(sample.getEventName()));
        assertThat(delivered.getNrWords(), is(sample.getNrWords()));
        assertThat(delivered.getSourceLanguage(), is(sample.getSourceLanguage()));
        assertThat(delivered.getTargetLanguage(), is(sample.getTargetLanguage()));
        assertThat(delivered.getDuration(), is(sample.getDuration()));
        assertThat(delivered.getTranslationId(), is(sample.getTranslationId()));
    }
}
