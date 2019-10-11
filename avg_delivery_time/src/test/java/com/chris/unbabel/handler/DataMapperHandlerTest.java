package com.chris.unbabel.handler;

import com.chris.unbabel.data.AverageDeliveryTime;
import com.chris.unbabel.data.TranslationDelivered;
import com.chris.unbabel.exception.TranslationEventException;
import com.google.common.collect.ImmutableList;
import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.net.URISyntaxException;
import java.net.URL;
import java.text.ParseException;
import java.util.Collection;
import java.util.Date;
import java.util.stream.Collectors;

import static com.google.common.base.Preconditions.checkNotNull;
import static org.hamcrest.Matchers.contains;
import static org.junit.Assert.assertThat;

public class DataMapperHandlerTest {
    private static final URL EVENTS_URL = DataMapperHandlerTest.class.getClassLoader().getResource("events.json");

    private File file;
    private DataMapperHandler handler;

    @Before
    public void setUp() throws URISyntaxException {
        checkNotNull(EVENTS_URL);
        file = new File(EVENTS_URL.toURI());
        handler = new DataMapperHandlerImpl();
    }

    @Test
    public void testMapEvents() throws TranslationEventException {
        final Collection<TranslationDelivered> mappedEvents = handler.mapEvents(file);

        assertThat(
                mappedEvents.stream()
                        .map(TranslationDelivered::getTranslationId)
                        .collect(Collectors.toList()),
                contains("5aa5b2f39f7254a75aa5", "5aa5b2f39f7254a75aa4", "5aa5b2f39f7254a75bb33"));
    }

    @Test(expected = TranslationEventException.class)
    public void testMapEventsWrongFile() throws TranslationEventException {
        handler.mapEvents(new File("bad_name"));
    }

    @Test
    public void testMap() throws ParseException, TranslationEventException {
        AverageDeliveryTime deliveryTime1 = new AverageDeliveryTime();
        deliveryTime1.setDate(new Date());
        deliveryTime1.setAvgTime(20.6D);

        AverageDeliveryTime deliveryTime2 = new AverageDeliveryTime();
        deliveryTime2.setDate(new Date());
        deliveryTime2.setAvgTime(22.0D);

        String map = handler.map(ImmutableList.of(deliveryTime1, deliveryTime2));

        assertThat(map.isEmpty(), Matchers.is(false));
    }
}