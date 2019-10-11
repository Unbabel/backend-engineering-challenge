package com.chris.unbabel.command;

import com.chris.unbabel.data.AverageDeliveryTime;
import com.chris.unbabel.data.TranslationDelivered;
import com.chris.unbabel.data.TranslationDeliveredPayload;
import com.chris.unbabel.exception.TranslationEventException;
import com.chris.unbabel.handler.ArgumentChecker;
import com.chris.unbabel.handler.DataMapperHandler;
import com.chris.unbabel.handler.RestServiceInvoker;

import java.io.File;
import java.util.Collection;
import java.util.List;

public class AverageCalculatorCommand implements Command<String> {
    private final DataMapperHandler mapper;
    private final Collection<String> properties;
    private final RestServiceInvoker<TranslationDeliveredPayload, AverageDeliveryTime> restService;

    public AverageCalculatorCommand(DataMapperHandler mapper,
                                    Collection<String> properties,
                                    RestServiceInvoker<TranslationDeliveredPayload, AverageDeliveryTime> restService) {
        this.mapper = mapper;
        this.properties = properties;
        this.restService = restService;
    }

    @Override
    public String call() throws TranslationEventException {
        final String file = ArgumentChecker.getArgumentFile(properties);
        final int windowSize = ArgumentChecker.getArgumentWindow(properties);

        List<TranslationDelivered> deliveredList = mapper.mapEvents(new File(file));

        return mapper.map(calculateAverageTime(deliveredList, windowSize));
    }

    private Collection<AverageDeliveryTime> calculateAverageTime(List<TranslationDelivered> deliveredList, int windowSize) {
        return restService.call(new TranslationDeliveredPayload(deliveredList, windowSize));
    }
}
