package com.unbable.unbable_cli.helpers;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.unbable.unbable_cli.models.Event;
import com.unbable.unbable_cli.models.Input;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.List;

@Component
@Slf4j
public abstract class ParserHelper {

    @Autowired
    private ObjectMapper objectMapper;

    /**
     * This method reads all the lines from the input and it maps each one into an object Event
     * @param input events provided
     * @return List of events
     * @throws IOException exception in case of error reading the lines
     */
    public abstract List<Event> parseEvents(Input input) throws IOException;

    /**
     * This method is in charge of map a json to an Event object
     * It uses the objectMapper singleton configuration for it.
     * @param line string that holds a json
     * @return Event that holds all the properties from the line read
     */
    protected Event mapEvent(String line) {
        Event event = null;

        try {
            event = objectMapper.readValue(line, Event.class);
        } catch (JsonProcessingException e) {
            log.error("The file isn't properly created, please check it and try later", e);
        }

        return event;
    }
}
