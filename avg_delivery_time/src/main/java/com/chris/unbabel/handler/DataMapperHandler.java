package com.chris.unbabel.handler;

import com.chris.unbabel.core.AverageDeliveryTime;
import com.chris.unbabel.core.Event;
import com.chris.unbabel.core.TranslationDelivered;
import com.google.common.collect.ImmutableCollection;

import javax.annotation.Nonnull;
import java.io.File;

public interface DataMapperHandler {

    ImmutableCollection<TranslationDelivered> mapEvents(@Nonnull final File file,
                                                        @Nonnull final Event event);

    String map(ImmutableCollection<AverageDeliveryTime> deliveryTimeList);
}
