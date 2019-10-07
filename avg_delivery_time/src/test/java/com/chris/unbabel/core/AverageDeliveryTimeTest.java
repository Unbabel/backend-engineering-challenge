package com.chris.unbabel.core;

import com.chris.unbabel.util.DateUtils;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.text.ParseException;

import static org.hamcrest.Matchers.is;
import static org.junit.Assert.assertThat;

public class AverageDeliveryTimeTest {
    private static final ObjectMapper MAPPER = new ObjectMapper();
    private static final String JSON = "{\"date\":\"2019-10-07 16:26:00\",\"average_delivery_time\":10.5}";

    private AverageDeliveryTime sample;

    @Before
    public void setUp() throws ParseException {
        sample = new AverageDeliveryTime();

        sample.setDate(DateUtils.parse("2019-10-07 17:26:00"));
        sample.setAvgTime(10.5);
    }

    @Test
    public void testMarshall() throws JsonProcessingException {
        final AverageDeliveryTime averageDeliveryTime = new AverageDeliveryTime(sample);

        final String json = MAPPER.writeValueAsString(averageDeliveryTime);

        assertThat(json, is(JSON));
    }

    @Test
    public void testUnMarshall() throws IOException {
        final AverageDeliveryTime averageDeliveryTime = MAPPER.readValue(JSON, AverageDeliveryTime.class);

        assertThat(averageDeliveryTime.getDate(), is(sample.getDate()));
        assertThat(averageDeliveryTime.getAvgTime(), is(sample.getAvgTime()));
    }
}
