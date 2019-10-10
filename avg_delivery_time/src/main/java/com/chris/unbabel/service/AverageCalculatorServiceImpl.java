package com.chris.unbabel.service;

import com.chris.unbabel.core.AverageDeliveryTime;
import com.chris.unbabel.core.TranslationDelivered;
import com.chris.unbabel.util.DateUtils;
import com.google.common.collect.Iterables;

import javax.annotation.Nonnull;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.*;

import static com.chris.unbabel.core.AverageDeliveryTime.build;

/**
 * @see AverageCalculatorService
 */
public class AverageCalculatorServiceImpl implements AverageCalculatorService {

    private static final int LAST_SECOND = 59;
    private static final int DOUBLE_SCALE = 2;
    private static final int RESET_SECONDS = 0;

    /**
     * @see AverageCalculatorService#calculateAverageTime(List, long)
     */
    @Override
    public Collection<AverageDeliveryTime> calculateAverageTime(@Nonnull final List<TranslationDelivered> deliveredList,
                                                                final long windowSizeMinutes) {
        Collection<AverageDeliveryTime> averageDeliveryTimeList = Collections.emptyList();

        if (!deliveredList.isEmpty()) {
            averageDeliveryTimeList = calculateAverageTime(deliveredList, getLastPosition(deliveredList), windowSizeMinutes);
        }

        return averageDeliveryTimeList;
    }

    private Date getLastPosition(@Nonnull final List<TranslationDelivered> list) {
        LocalDateTime dateTime = DateUtils.toDateTime(Iterables.getLast(list).getTimestamp()).plusMinutes(1);
        final ZonedDateTime dateTimeAsLocal = dateTime.atZone(ZoneId.systemDefault());

        return Date.from(dateTimeAsLocal.toInstant());
    }

    /**
     * @see AverageCalculatorService#calculateAverageTime(List, Date, long)
     */
    @Override
    public Collection<AverageDeliveryTime> calculateAverageTime(@Nonnull final List<TranslationDelivered> deliveredList,
                                                                @Nonnull final Date baseDatetime,
                                                                final long windowSizeMinutes) {
        final List<AverageDeliveryTime> averageDeliveryTimes = new ArrayList<>();
        final long firstPosition = windowSizeMinutes - 1L;

        LocalDateTime currentWindowTime = DateUtils.toDateTime(baseDatetime)
                .minusMinutes(firstPosition)
                .withSecond(RESET_SECONDS);

        int windowPosition = 1;
        int deliveryListPosition = calculateDeliveryListFirstPosition(deliveredList, currentWindowTime);
        double lastAvg = 0.0D;

        do {
            final Collection<Double> averageValues = new ArrayList<>();

            deliveryListPosition = addAverageValues(deliveredList, currentWindowTime, deliveryListPosition, lastAvg, averageValues);

            lastAvg = calculateAverageForCurrentWindowTime(averageDeliveryTimes, currentWindowTime, averageValues);

            averageValues.clear();
            ++windowPosition;

            currentWindowTime = currentWindowTime.plusMinutes(1);
        } while (windowPosition <= windowSizeMinutes);

        return averageDeliveryTimes;
    }

    private int calculateDeliveryListFirstPosition(@Nonnull List<TranslationDelivered> deliveredList, LocalDateTime current) {
        int deliveryListPosition = 0;

        while (deliveryListPosition < deliveredList.size()) {
            TranslationDelivered delivered = deliveredList.get(deliveryListPosition);
            LocalDateTime dateTime = DateUtils.toDateTime(delivered.getTimestamp());

            int point = dateTime.compareTo(current.minusMinutes(1).withSecond(RESET_SECONDS));

            if (point <= 0) {
                deliveryListPosition++;
            } else {
                break;
            }
        }

        return deliveryListPosition;
    }

    private int addAverageValues(@Nonnull List<TranslationDelivered> deliveredList, LocalDateTime current, int deliveryListPosition, double lastAvg, Collection<Double> avgItems) {
        if (lastAvg != 0.0D) {
            avgItems.add(lastAvg);
        }

        while (deliveryListPosition < deliveredList.size()) {
            final TranslationDelivered delivered = deliveredList.get(deliveryListPosition);
            final LocalDateTime dateTime = DateUtils.toDateTime(delivered.getTimestamp());

            int startPoint = dateTime.compareTo(current.minusMinutes(1).withSecond(RESET_SECONDS));
            int endPoint = dateTime.compareTo(current.minusMinutes(1).withSecond(LAST_SECOND));

            if (startPoint >= 0 && endPoint <= 0) {
                avgItems.add(delivered.getDuration());
            } else {
                break;
            }

            deliveryListPosition++;
        }
        return deliveryListPosition;
    }

    private double calculateAverageForCurrentWindowTime(List<AverageDeliveryTime> averageDeliveryTimes, LocalDateTime currentTime, Collection<Double> averageValues) {
        final ZonedDateTime currentTimeAsLocal = currentTime.atZone(ZoneId.systemDefault());

        final double avg = BigDecimal.valueOf(averageValues.stream().mapToDouble(d -> d).average().orElse(0.0D))
                .setScale(DOUBLE_SCALE, RoundingMode.HALF_UP)
                .doubleValue();

        averageDeliveryTimes.add(build(Date.from(currentTimeAsLocal.toInstant()), avg));

        return avg;
    }
}
