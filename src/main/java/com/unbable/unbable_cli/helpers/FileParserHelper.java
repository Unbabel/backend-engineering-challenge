package com.unbable.unbable_cli.helpers;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.unbable.unbable_cli.models.Event;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

@Component
@Slf4j
public class FileParserHelper {

    @Autowired
    private ObjectMapper objectMapper;

    public List<Event> parseFileEvents(File inputFile) throws IOException {
        return Files.readAllLines(Paths.get(inputFile.getAbsolutePath()))
                .stream()
                .map(this::mapEvent)
                .filter(Objects::nonNull)
                .sorted(Comparator.comparing(Event::getTimestamp))
                .collect(Collectors.toList());
    }

    private Event mapEvent(String line) {
        Event event = null;

        try {
            event = objectMapper.readValue(line, Event.class);
        } catch (JsonProcessingException e) {
            log.error("The file isn't properly created, please check it and try later", e);
        }

        return event;
    }
}
