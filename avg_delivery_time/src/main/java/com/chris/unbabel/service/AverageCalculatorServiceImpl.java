package com.chris.unbabel.service;

import com.chris.unbabel.core.AverageDeliveryTime;
import com.chris.unbabel.core.TranslationDelivered;

import javax.annotation.Nonnull;
import java.util.Collection;
import java.util.Date;

public class AverageCalculatorServiceImpl implements AverageCalculatorService {

    /**
     * Calculates a moving average translation delivery time based on window size.
     *
     * @param deliveredList     events to calculate the average delivery time.
     * @param currentDatetime   datetime to base the window size calculation.
     * @param windowSizeMinutes window size in minutes to calculate the average delivery time.
     * @return A list of an average delivery time based on the {@code windowSizeMinutes}.
     */
    @Override
    public Collection<AverageDeliveryTime> averageTranslationTimeOf(@Nonnull Collection<TranslationDelivered> deliveredList, @Nonnull Date currentDatetime, int windowSizeMinutes) {
        return null;
    }
}
