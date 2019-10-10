package com.chris.unbabel.handler;

import com.chris.unbabel.core.AverageDeliveryTime;
import com.chris.unbabel.core.Event;
import com.chris.unbabel.core.TranslationDelivered;
import com.chris.unbabel.exception.TranslationEventException;

import javax.annotation.Nonnull;
import java.io.File;
import java.util.Collection;
import java.util.List;

public interface DataMapperHandler {

    List<TranslationDelivered> mapEvents(@Nonnull final File file,
                                         @Nonnull final Event event) throws TranslationEventException;

    String map(Collection<AverageDeliveryTime> deliveryTimeList) throws TranslationEventException;
}
