package com.unbable.unbable_cli.helpers;

import com.unbable.unbable_cli.models.Event;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Component
public class EventReaderHelper {

    /**
     * This method is to the determine if an Event belongs inside a time window.
     *
     * @param event Event to check
     * @param start Start date for the window
     * @param end End date for the window
     * @return true if belongs, false if it doesnt.
     */
    private boolean eventBelongsToWindow(Event event, LocalDateTime start, LocalDateTime end) {
        LocalDateTime eventTime = event.getTimestamp();

        return (eventTime.isEqual(start) || eventTime.isAfter(start)) && (eventTime.isEqual(end) || eventTime.isBefore(end));
    }

    /**
     * This method is to filter all the events from a list, keeping only those that belong inside the required
     * window of time.
     * @param events List of events
     * @param start Start date for the window
     * @param end End date for the window
     * @return Filtered list
     */
    public List<Event> filterByWindow(List<Event> events, LocalDateTime start, Integer end) {
        return events.stream().filter(it -> eventBelongsToWindow(it, start.minusMinutes(end), start)).collect(Collectors.toList());
    }
}
