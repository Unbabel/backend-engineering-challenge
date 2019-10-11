package com.chris.unbabel.handler;

import com.chris.unbabel.data.AverageDeliveryTime;
import com.chris.unbabel.data.TranslationDelivered;
import com.chris.unbabel.exception.TranslationEventException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.annotation.Nonnull;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class DataMapperHandlerImpl implements DataMapperHandler {
    private static final Logger LOGGER = LoggerFactory.getLogger(DataMapperHandlerImpl.class);
    private static final ObjectMapper MAPPER = new ObjectMapper();

    @Override
    public List<TranslationDelivered> mapEvents(@Nonnull File file) throws TranslationEventException {
        try (final Stream<String> stream = Files.lines(Paths.get(file.toURI()))) {
            return stream.map(DataMapperHandlerImpl::readValue)
                    .filter(Optional::isPresent)
                    .map(Optional::get)
                    .collect(Collectors.toList());
        } catch (IOException e) {
            throw new TranslationEventException(e);
        }
    }

    private static Optional<TranslationDelivered> readValue(@Nonnull String json) {
        try {
            return Optional.ofNullable(MAPPER.readValue(json, TranslationDelivered.class));
        } catch (IOException e) {
            LOGGER.warn("Failed to parse json, cause={}", e.getMessage());
            LOGGER.debug(json, e);
            return Optional.empty();
        }
    }

    @Override
    public String map(Collection<AverageDeliveryTime> deliveryTimeList) throws TranslationEventException {
        try {
            return MAPPER.writeValueAsString(deliveryTimeList);
        } catch (JsonProcessingException e) {
            throw new TranslationEventException(e);
        }
    }
}
