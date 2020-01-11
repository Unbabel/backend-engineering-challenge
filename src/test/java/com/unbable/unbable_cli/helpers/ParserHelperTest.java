package com.unbable.unbable_cli.helpers;

import com.unbable.unbable_cli.helpers.files.FileParserHelper;
import com.unbable.unbable_cli.models.Event;
import com.unbable.unbable_cli.models.Input;
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
public class ParserHelperTest {

    @Autowired
    private FileParserHelper fileParserHelper;

    @Test
    public void parse_file_events_successfully() {
        File inputFile = new File("src/test/resources/events.json");
        Input input = new Input(10, inputFile);

        try {
            List<Event> events = fileParserHelper.parseEvents(input);
            assertFalse(events.isEmpty());
        } catch (IOException e) {
            fail();
        }
    }

    @Test
    public void parse_file_events_wrong_lines() {
        File inputFile = new File("src/test/resources/custom_events.json");
        Input input = new Input(10, inputFile);

        try {
            List<Event> events = fileParserHelper.parseEvents(input);
            assertTrue(events.isEmpty());
        } catch (IOException e) {
            fail();
        }
    }
}
