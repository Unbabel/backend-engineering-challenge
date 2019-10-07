package com.chris.unbabel.handler;

import com.chris.unbabel.core.AverageDeliveryTime;
import com.chris.unbabel.core.Event;
import com.chris.unbabel.core.TranslationDelivered;
import com.google.common.collect.ImmutableCollection;

import javax.annotation.Nonnull;
import java.io.File;

public class DataMapperHandlerImpl implements DataMapperHandler {


    @Override
    public ImmutableCollection<TranslationDelivered> mapEvents(@Nonnull File file, @Nonnull Event event) {
        return null;
    }

    @Override
    public String map(ImmutableCollection<AverageDeliveryTime> deliveryTimeList) {
        return null;
    }
}
