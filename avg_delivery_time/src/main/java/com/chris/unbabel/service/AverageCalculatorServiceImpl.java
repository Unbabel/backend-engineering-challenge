package com.chris.unbabel.service;

import com.chris.unbabel.core.AverageDeliveryTime;
import com.chris.unbabel.core.TranslationDelivered;
import com.chris.unbabel.util.DateUtils;

import javax.annotation.Nonnull;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.List;

import static com.chris.unbabel.core.AverageDeliveryTime.build;

/**
 * @see AverageCalculatorService
 */
public class AverageCalculatorServiceImpl implements AverageCalculatorService {

    private static final int LAST_SECOND = 59;
    private static final int DOUBLE_SCALE = 2;

    /**
     * @see AverageCalculatorService#calculateAverageTime(List, Date, long)
     */
    @Override
    public Collection<AverageDeliveryTime> calculateAverageTime(@Nonnull final List<TranslationDelivered> deliveredList,
                                                                @Nonnull final Date baseDatetime,
                                                                final long windowSizeMinutes) {

        final List<AverageDeliveryTime> averageDeliveryTimes = new ArrayList<>();
        final long firstPosition = windowSizeMinutes - 1L;

        LocalDateTime currentTime = DateUtils.toDateTime(baseDatetime)
                .minusMinutes(firstPosition)
                .withSecond(0);

        int windowPosition = 1;
        int deliveryListPosition = calculateDeliveryListFirstPosition(deliveredList, currentTime);
        double lastAvg = 0.0D;

        do {
            final Collection<Double> averageValues = new ArrayList<>();

            deliveryListPosition = addAverageValues(deliveredList, currentTime, deliveryListPosition, lastAvg, averageValues);

            final double avg = calculateAverageForCurrentWindowTime(averageDeliveryTimes, currentTime, averageValues);

            averageValues.clear();
            lastAvg = avg;

            ++windowPosition;

            currentTime = currentTime.plusMinutes(1);
        } while (windowPosition <= windowSizeMinutes);
        
        return averageDeliveryTimes;
    }

    private int calculateDeliveryListFirstPosition(@Nonnull List<TranslationDelivered> deliveredList, LocalDateTime current) {
        int deliveryListPosition = 0;

        while (deliveryListPosition < deliveredList.size()) {
            TranslationDelivered delivered = deliveredList.get(deliveryListPosition);
            LocalDateTime dateTime = DateUtils.toDateTime(delivered.getTimestamp());

            int point = dateTime.compareTo(current.minusMinutes(1).withSecond(0));

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

            int startPoint = dateTime.compareTo(current.minusMinutes(1).withSecond(0));
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
