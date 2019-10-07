package com.chris.unbabel.service;

import com.chris.unbabel.core.AverageDeliveryTime;
import com.chris.unbabel.core.TranslationDelivered;
import com.google.common.collect.ImmutableCollection;

import javax.annotation.Nonnull;
import java.util.Date;

/**
 * Service to handle the average calculation.
 */
public interface AverageCalculatorService {

    /**
     * Calculates a moving average translation delivery time based on window size.
     *
     * @param deliveredList     events to calculate the average delivery time.
     * @param currentDatetime   datetime to base the window size calculation.
     * @param windowSizeMinutes window size in minutes to calculate the average delivery time.
     * @return A list of an average delivery time based on the {@code windowSizeMinutes}.
     */
    ImmutableCollection<AverageDeliveryTime> averageTranslationTimeOf(@Nonnull final ImmutableCollection<TranslationDelivered> deliveredList,
                                                           @Nonnull final Date currentDatetime,
                                                           final int windowSizeMinutes);
}

