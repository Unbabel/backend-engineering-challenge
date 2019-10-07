package com.chris.unbabel.service;

import com.chris.unbabel.core.AverageDeliveryTime;
import com.chris.unbabel.core.TranslationDelivered;
import com.chris.unbabel.util.DateUtils;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.collect.Lists;
import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Test;

import java.text.ParseException;
import java.util.Collection;

import static org.junit.Assert.assertThat;

public class AverageCalculatorServiceTest {
    private static final ObjectMapper MAPPER = new ObjectMapper();

    private AverageCalculatorService calculatorService;

    @Before
    public void setUp(){
        calculatorService = new AverageCalculatorServiceImpl();
    }

    @Test
    public void testAverageTranslationCase1() throws ParseException, JsonProcessingException {
        TranslationDelivered delivered1 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:11:08.509654"),
                "5aa5b2f39f7254a75aa5",
                20

        );
        TranslationDelivered delivered2 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:15:19.903159"),
                "5aa5b2f39f7254a75aa4",
                31

        );
        TranslationDelivered delivered3 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:23:19.903159"),
                "5aa5b2f39f7254a75bb33",
                54
        );

        Collection<AverageDeliveryTime> averageDeliveryTimes = calculatorService.averageTranslationTimeOf(
                Lists.newArrayList(delivered1, delivered2, delivered3),
                DateUtils.parse("2018-12-26 18:24:00"),
                10);

        assertThat(MAPPER.writeValueAsString(averageDeliveryTimes),
                Matchers.is("[{\"date\": \"2018-12-26 18:11:00\", \"average_delivery_time\": 0}," +
                        "{\"date\": \"2018-12-26 18:12:00\", \"average_delivery_time\": 20}," +
                        "{\"date\": \"2018-12-26 18:13:00\", \"average_delivery_time\": 20}," +
                        "{\"date\": \"2018-12-26 18:14:00\", \"average_delivery_time\": 20}," +
                        "{\"date\": \"2018-12-26 18:15:00\", \"average_delivery_time\": 20}," +
                        "{\"date\": \"2018-12-26 18:16:00\", \"average_delivery_time\": 25.5}," +
                        "{\"date\": \"2018-12-26 18:17:00\", \"average_delivery_time\": 25.5}," +
                        "{\"date\": \"2018-12-26 18:18:00\", \"average_delivery_time\": 25.5}," +
                        "{\"date\": \"2018-12-26 18:19:00\", \"average_delivery_time\": 25.5}," +
                        "{\"date\": \"2018-12-26 18:20:00\", \"average_delivery_time\": 25.5}," +
                        "{\"date\": \"2018-12-26 18:21:00\", \"average_delivery_time\": 25.5}," +
                        "{\"date\": \"2018-12-26 18:22:00\", \"average_delivery_time\": 25.5}," +
                        "{\"date\": \"2018-12-26 18:23:00\", \"average_delivery_time\": 25.5}," +
                        "{\"date\": \"2018-12-26 18:24:00\", \"average_delivery_time\": 42.5}]"));
    }
}