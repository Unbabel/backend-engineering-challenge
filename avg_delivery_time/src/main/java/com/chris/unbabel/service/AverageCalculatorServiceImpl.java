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

public class AverageCalculatorServiceImpl implements AverageCalculatorService {

    /**
     * Calculates a moving average translation delivery time based on window size.
     *
     * @param deliveredList     events to calculate the average delivery time.
     * @param baseDatetime      datetime to base the window size calculation.
     * @param windowSizeMinutes window size in minutes to calculate the average delivery time.
     * @return A list of an average delivery time based on the {@code windowSizeMinutes}.
     */
    @Override
    public Collection<AverageDeliveryTime> averageTranslationTimeOf(@Nonnull final List<TranslationDelivered> deliveredList,
                                                                    @Nonnull final Date baseDatetime,
                                                                    final int windowSizeMinutes) {

        //   final Map<Date, List<TranslationDelivered>> map = deliveredList.stream()
        //         .collect(groupingBy(TranslationDelivered::getTimestamp, toList()));

        final List<AverageDeliveryTime> averageDeliveryTimes = new ArrayList<>();

        LocalDateTime current = DateUtils.toDateTime(baseDatetime)
                .minusMinutes(windowSizeMinutes - 1)
                .withSecond(0);

        int count = 1;
        int deliveryListPosition = 0;
        double lastAvg = 0.0D;

        do {
            Collection<Double> avgItems = new ArrayList<>();

            if (lastAvg != 0.0D) {
                avgItems.add(lastAvg);
            }

            while (deliveryListPosition < deliveredList.size()) {
                TranslationDelivered delivered = deliveredList.get(deliveryListPosition);

                LocalDateTime dateTime = DateUtils.toDateTime(delivered.getTimestamp());

                int startPoint = dateTime.compareTo(current.minusMinutes(1).withSecond(0));
                int endPoint = dateTime.compareTo(current.minusMinutes(1).withSecond(59));

                if (startPoint >= 0 && endPoint <= 0) {
                    avgItems.add(delivered.getDuration());
                } else {
                    break;
                }

                deliveryListPosition++;
            }

            ZonedDateTime zdt = current.atZone(ZoneId.systemDefault());

            double avg = 0.0D;
            if (!avgItems.isEmpty()) {
                avg = avgItems.stream().mapToDouble(d -> d).average().getAsDouble();
            }

            averageDeliveryTimes.add(new AverageDeliveryTime(Date.from(zdt.toInstant()), BigDecimal.valueOf(avg).setScale(2, RoundingMode.HALF_UP).doubleValue()));

            avgItems.clear();
            lastAvg = avg;

            ++count;

            current = current.plusMinutes(1);
        } while (count <= windowSizeMinutes);


        return averageDeliveryTimes;
    }
}
