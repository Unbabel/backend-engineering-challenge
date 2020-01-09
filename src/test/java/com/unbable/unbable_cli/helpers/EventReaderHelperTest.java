package com.unbable.unbable_cli.helpers;

import com.unbable.unbable_cli.models.Event;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
public class EventReaderHelperTest {

    @Autowired
    private EventReaderHelper eventReaderHelper;

    @Test
    public void test_filter_by_window() {
        Event event = new Event();
        event.setTimestamp(LocalDateTime.now());

        List<Event> events = Collections.singletonList(event);

        List<Event> eventsFiltered = eventReaderHelper.filterByWindow(events, LocalDateTime.now().minusMinutes(11), 10);
        assertTrue(eventsFiltered.isEmpty());
    }
}
