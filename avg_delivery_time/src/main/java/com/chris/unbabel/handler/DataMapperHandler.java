package com.chris.unbabel.handler;

import com.chris.unbabel.data.AverageDeliveryTime;
import com.chris.unbabel.data.TranslationDelivered;
import com.chris.unbabel.exception.TranslationEventException;

import javax.annotation.Nonnull;
import java.io.File;
import java.util.Collection;
import java.util.List;

public interface DataMapperHandler {

    List<TranslationDelivered> mapEvents(@Nonnull final File file) throws TranslationEventException;

    String map(Collection<AverageDeliveryTime> deliveryTimeList) throws TranslationEventException;
}
