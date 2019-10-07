package com.chris.unbabel.handler;

import com.chris.unbabel.core.AverageDeliveryTime;
import com.chris.unbabel.core.TranslationDelivered;
import com.chris.unbabel.util.DateUtils;
import com.google.common.collect.ImmutableCollection;
import com.google.common.collect.ImmutableList;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.net.URISyntaxException;
import java.net.URL;
import java.text.ParseException;
import java.util.stream.Collectors;

import static com.chris.unbabel.core.Event.TRANSLATION_DELIVERED;
import static com.google.common.base.Preconditions.checkNotNull;
import static org.hamcrest.Matchers.contains;
import static org.hamcrest.Matchers.is;
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
    public void testMapEvents() {
        final ImmutableCollection<TranslationDelivered> mappedEvents = handler.mapEvents(file, TRANSLATION_DELIVERED);

        assertThat(
                mappedEvents.stream()
                        .map(TranslationDelivered::getTranslationId)
                        .collect(Collectors.toList()),
                contains("5aa5b2f39f7254a75aa5", "5aa5b2f39f7254a75aa4", "5aa5b2f39f7254a75bb33"));
    }

    @Test
    public void testMap() throws ParseException {
        AverageDeliveryTime deliveryTime1 = new AverageDeliveryTime();
        deliveryTime1.setDate(DateUtils.parse("2018-12-26 18:23:00"));
        deliveryTime1.setAvgTime(20.6D);

        AverageDeliveryTime deliveryTime2 = new AverageDeliveryTime();
        deliveryTime1.setDate(DateUtils.parse("2018-12-26 18:24:00"));
        deliveryTime1.setAvgTime(22.0D);

        String map = handler.map(ImmutableList.of(deliveryTime1, deliveryTime2));

        assertThat(map,
                is("{\"date\":\"2018-12-26 18:23:00\",\"average_delivery_time\":20.6}" +
                        "{\"date\":\"2018-12-26 18:24:00\",\"average_delivery_time\":22.0}"));
    }
}