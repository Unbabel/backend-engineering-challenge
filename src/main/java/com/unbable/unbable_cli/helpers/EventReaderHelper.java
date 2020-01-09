package com.unbable.unbable_cli.helpers;

import com.unbable.unbable_cli.models.Event;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Component
public class EventReaderHelper {

    private boolean eventBelongsToWindow(Event event, LocalDateTime start, LocalDateTime end) {
        LocalDateTime eventTime = event.getTimestamp();

        return (eventTime.isEqual(start) || eventTime.isAfter(start)) && (eventTime.isEqual(end) || eventTime.isBefore(end));
    }

    public List<Event> filterByWindow(List<Event> events, LocalDateTime start, Integer end) {
        return events.stream().filter(it -> eventBelongsToWindow(it, start.minusMinutes(end), start)).collect(Collectors.toList());
    }
}
