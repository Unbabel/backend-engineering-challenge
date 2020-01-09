package com.unbable.unbable_cli.helpers;

import com.unbable.unbable_cli.models.Event;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.File;
import java.io.IOException;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

@SpringBootTest
public class FileParserHelperTest {

    @Autowired
    private FileParserHelper fileParserHelper;

    @Test
    public void parse_file_events_successfully() {
        File inputFile = new File("src/test/resources/events.json");

        try {
            List<Event> events = fileParserHelper.parseFileEvents(inputFile);
            assertFalse(events.isEmpty());
        } catch (IOException e) {
            fail();
        }
    }

    @Test
    public void parse_file_events_wrong_lines() {
        File inputFile = new File("src/test/resources/custom_events.json");

        try {
            List<Event> events = fileParserHelper.parseFileEvents(inputFile);
            assertTrue(events.isEmpty());
        } catch (IOException e) {
            fail();
        }
    }
}
