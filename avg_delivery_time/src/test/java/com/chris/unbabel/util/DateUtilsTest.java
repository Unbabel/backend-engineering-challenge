package com.chris.unbabel.util;

import org.junit.Test;

import java.text.ParseException;
import java.util.Date;

import static org.hamcrest.Matchers.is;
import static org.junit.Assert.assertThat;

public class DateUtilsTest {

    @Test
    public void testParse() throws ParseException {
        Date date = DateUtils.parse("2018-12-26 18:23:19.903159");
        assertThat(date.getTime(), is(1545848599000L));
    }

    @Test
    public void testParseNoPrecision() throws ParseException {
        Date date = DateUtils.parse("2018-12-26 18:23:19");
        assertThat(date.getTime(), is(1545848599000L));
    }

    @Test(expected = NullPointerException.class)
    public void testParseNull() throws ParseException {
        DateUtils.parse(null);
    }
}
