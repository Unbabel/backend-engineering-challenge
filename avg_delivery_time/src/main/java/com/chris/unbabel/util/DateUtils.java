package com.chris.unbabel.util;

import javax.annotation.Nonnull;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Date;

import static com.google.common.base.Preconditions.checkNotNull;

/**
 * Date/time formats handler.
 */
public final class DateUtils {
    public static final String DATE_FORMAT = "yyyy-MM-dd HH:mm:ss";
    private static final SimpleDateFormat FORMATTER = new SimpleDateFormat(DATE_FORMAT);

    private DateUtils() {
        // Utility class
    }

    /**
     * Transforms a string date to a  {@link Date}.
     *
     * @param date A non null string date for the {@link #DATE_FORMAT}.
     * @return a datetime based on {@link #DATE_FORMAT}.
     * @throws ParseException if a string no respect the {@link #DATE_FORMAT}.
     */
    public static Date parse(@Nonnull final String date) throws ParseException {
        checkNotNull(date);
        return FORMATTER.parse(date);
    }

    /**
     *
     * @param date
     * @return
     */
    public static LocalDateTime toDateTime(Date date) {
        return LocalDateTime.ofInstant(date.toInstant(),
                ZoneId.systemDefault());
    }
}
