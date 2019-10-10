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
    public void setUp() {
        calculatorService = new AverageCalculatorServiceImpl();
    }

    @Test
    public void testAverageTranslationSimple() throws ParseException, JsonProcessingException {
        TranslationDelivered delivered0 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:09:08.509654"),
                "5aa5b2f39f7254a75aa5",
                100
        );

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
        TranslationDelivered delivered4 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:25:19.903159"),
                "5aa5b2f39f7254a75bb33",
                54
        );

        Collection<AverageDeliveryTime> averageDeliveryTimes = calculatorService.calculateAverageTime(
                Lists.newArrayList(delivered0, delivered1, delivered2, delivered3, delivered4),
                DateUtils.parse("2018-12-26 18:24:00"),
                14);

        assertThat(MAPPER.writeValueAsString(averageDeliveryTimes),
                Matchers.is("[{\"date\":\"2018-12-26 18:11:00\",\"average_delivery_time\":0.0}," +
                        "{\"date\":\"2018-12-26 18:12:00\",\"average_delivery_time\":20.0}," +
                        "{\"date\":\"2018-12-26 18:13:00\",\"average_delivery_time\":20.0}," +
                        "{\"date\":\"2018-12-26 18:14:00\",\"average_delivery_time\":20.0}," +
                        "{\"date\":\"2018-12-26 18:15:00\",\"average_delivery_time\":20.0}," +
                        "{\"date\":\"2018-12-26 18:16:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:17:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:18:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:19:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:20:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:21:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:22:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:23:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:24:00\",\"average_delivery_time\":39.75}]"));
    }

    @Test
    public void testAverageTranslationSimpleDefaultDate() throws ParseException, JsonProcessingException {
        TranslationDelivered delivered0 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:09:08.509654"),
                "5aa5b2f39f7254a75aa5",
                100
        );

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

        Collection<AverageDeliveryTime> averageDeliveryTimes = calculatorService.calculateAverageTime(
                Lists.newArrayList(delivered0, delivered1, delivered2, delivered3),
                14);

        assertThat(MAPPER.writeValueAsString(averageDeliveryTimes),
                Matchers.is("[{\"date\":\"2018-12-26 18:11:00\",\"average_delivery_time\":0.0}," +
                        "{\"date\":\"2018-12-26 18:12:00\",\"average_delivery_time\":20.0}," +
                        "{\"date\":\"2018-12-26 18:13:00\",\"average_delivery_time\":20.0}," +
                        "{\"date\":\"2018-12-26 18:14:00\",\"average_delivery_time\":20.0}," +
                        "{\"date\":\"2018-12-26 18:15:00\",\"average_delivery_time\":20.0}," +
                        "{\"date\":\"2018-12-26 18:16:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:17:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:18:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:19:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:20:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:21:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:22:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:23:00\",\"average_delivery_time\":25.5}," +
                        "{\"date\":\"2018-12-26 18:24:00\",\"average_delivery_time\":39.75}]"));
    }

    @Test
    public void testAverageTranslationWindowSizeEqualsOne() throws ParseException, JsonProcessingException {
        TranslationDelivered delivered1 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:11:08.509654"),
                "5aa5b2f39f7254a75aa5",
                20
        );

        Collection<AverageDeliveryTime> averageDeliveryTimes = calculatorService.calculateAverageTime(
                Lists.newArrayList(delivered1),
                DateUtils.parse("2018-12-26 18:24:00"),
                1);

        assertThat(MAPPER.writeValueAsString(averageDeliveryTimes),
                Matchers.is("[{\"date\":\"2018-12-26 18:24:00\",\"average_delivery_time\":0.0}]"));
    }

    @Test
    public void testAverageTranslationMoreThanOneAVGByTimeSlot() throws ParseException, JsonProcessingException {
        TranslationDelivered delivered0 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:09:08.509654"),
                "5aa5b2f39f7254a75aa5",
                50
        );

        TranslationDelivered delivered1 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:11:08.509654"),
                "5aa5b2f39f7254a75aa5",
                20
        );
        TranslationDelivered delivered2 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:11:10.509654"),
                "5aa5b2f39f7254a75aa5",
                25
        );
        TranslationDelivered delivered3 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:15:19.903159"),
                "5aa5b2f39f7254a75aa4",
                31
        );
        TranslationDelivered delivered4 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:23:05.509654"),
                "5aa5b2f39f7254a75aa5",
                40
        );
        TranslationDelivered delivered5 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:23:19.903159"),
                "5aa5b2f39f7254a75bb33",
                54
        );
        TranslationDelivered delivered6 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 18:29:19.903159"),
                "5aa5b2f39f7254a75bb33",
                54
        );

        Collection<AverageDeliveryTime> averageDeliveryTimes = calculatorService.calculateAverageTime(
                Lists.newArrayList(delivered0, delivered1, delivered2, delivered3, delivered4, delivered5),
                DateUtils.parse("2018-12-26 18:24:00"),
                14);

        assertThat(MAPPER.writeValueAsString(averageDeliveryTimes),
                Matchers.is("[{\"date\":\"2018-12-26 18:11:00\",\"average_delivery_time\":0.0}," +
                        "{\"date\":\"2018-12-26 18:12:00\",\"average_delivery_time\":22.5}," +
                        "{\"date\":\"2018-12-26 18:13:00\",\"average_delivery_time\":22.5}," +
                        "{\"date\":\"2018-12-26 18:14:00\",\"average_delivery_time\":22.5}," +
                        "{\"date\":\"2018-12-26 18:15:00\",\"average_delivery_time\":22.5}," +
                        "{\"date\":\"2018-12-26 18:16:00\",\"average_delivery_time\":26.75}," +
                        "{\"date\":\"2018-12-26 18:17:00\",\"average_delivery_time\":26.75}," +
                        "{\"date\":\"2018-12-26 18:18:00\",\"average_delivery_time\":26.75}," +
                        "{\"date\":\"2018-12-26 18:19:00\",\"average_delivery_time\":26.75}," +
                        "{\"date\":\"2018-12-26 18:20:00\",\"average_delivery_time\":26.75}," +
                        "{\"date\":\"2018-12-26 18:21:00\",\"average_delivery_time\":26.75}," +
                        "{\"date\":\"2018-12-26 18:22:00\",\"average_delivery_time\":26.75}," +
                        "{\"date\":\"2018-12-26 18:23:00\",\"average_delivery_time\":26.75}," +
                        "{\"date\":\"2018-12-26 18:24:00\",\"average_delivery_time\":40.25}]"));
    }

    @Test
    public void testAverageTranslationDateTimeEdgeLimits() throws ParseException, JsonProcessingException {
        TranslationDelivered delivered0 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 21:10:08.509654"),
                "5aa5b2f39f7254a75aa5",
                50
        );

        TranslationDelivered delivered1 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 22:58:08.509654"),
                "5aa5b2f39f7254a75aa5",
                20
        );
        TranslationDelivered delivered2 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 22:59:10.509654"),
                "5aa5b2f39f7254a75aa5",
                25
        );
        TranslationDelivered delivered3 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 22:59:19.903159"),
                "5aa5b2f39f7254a75aa4",
                31
        );
        TranslationDelivered delivered4 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 22:59:05.509654"),
                "5aa5b2f39f7254a75aa5",
                40
        );
        TranslationDelivered delivered5 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 23:01:19.903159"),
                "5aa5b2f39f7254a75bb33",
                54
        );
        TranslationDelivered delivered6 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 23:05:19.903159"),
                "5aa5b2f39f7254a75bb33",
                54
        );

        Collection<AverageDeliveryTime> averageDeliveryTimes = calculatorService.calculateAverageTime(
                Lists.newArrayList(delivered0, delivered1, delivered2, delivered3, delivered4, delivered5, delivered6),
                DateUtils.parse("2018-12-26 23:02:00"),
                10);

        assertThat(MAPPER.writeValueAsString(averageDeliveryTimes),
                Matchers.is("[{\"date\":\"2018-12-26 22:53:00\",\"average_delivery_time\":0.0}," +
                        "{\"date\":\"2018-12-26 22:54:00\",\"average_delivery_time\":0.0}," +
                        "{\"date\":\"2018-12-26 22:55:00\",\"average_delivery_time\":0.0}," +
                        "{\"date\":\"2018-12-26 22:56:00\",\"average_delivery_time\":0.0}," +
                        "{\"date\":\"2018-12-26 22:57:00\",\"average_delivery_time\":0.0}," +
                        "{\"date\":\"2018-12-26 22:58:00\",\"average_delivery_time\":0.0}," +
                        "{\"date\":\"2018-12-26 22:59:00\",\"average_delivery_time\":20.0}," +
                        "{\"date\":\"2018-12-26 23:00:00\",\"average_delivery_time\":29.0}," +
                        "{\"date\":\"2018-12-26 23:01:00\",\"average_delivery_time\":29.0}," +
                        "{\"date\":\"2018-12-26 23:02:00\",\"average_delivery_time\":41.5}]"));
    }

    @Test
    public void testAverageTranslationDayChanged() throws ParseException, JsonProcessingException {
        TranslationDelivered delivered0 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 23:57:08.509654"),
                "5aa5b2f39f7254a75aa5",
                50
        );

        TranslationDelivered delivered1 = new TranslationDelivered(
                DateUtils.parse("2018-12-26 23:59:08.509654"),
                "5aa5b2f39f7254a75aa5",
                20
        );
        TranslationDelivered delivered2 = new TranslationDelivered(
                DateUtils.parse("2018-12-27 00:01:10.509654"),
                "5aa5b2f39f7254a75aa5",
                25
        );

        Collection<AverageDeliveryTime> averageDeliveryTimes = calculatorService.calculateAverageTime(
                Lists.newArrayList(delivered0, delivered1, delivered2),
                DateUtils.parse("2018-12-27 00:01:00"),
                4);

        assertThat(MAPPER.writeValueAsString(averageDeliveryTimes),
                Matchers.is("[{\"date\":\"2018-12-26 23:58:00\",\"average_delivery_time\":50.0}," +
                        "{\"date\":\"2018-12-26 23:59:00\",\"average_delivery_time\":50.0}," +
                        "{\"date\":\"2018-12-27 00:00:00\",\"average_delivery_time\":35.0}," +
                        "{\"date\":\"2018-12-27 00:01:00\",\"average_delivery_time\":35.0}]"));
    }
}