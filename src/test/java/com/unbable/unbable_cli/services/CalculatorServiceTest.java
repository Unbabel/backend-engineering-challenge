package com.unbable.unbable_cli.services;

import com.unbable.unbable_cli.helpers.OptionReaderHelper;
import com.unbable.unbable_cli.helpers.files.FileParserHelper;
import com.unbable.unbable_cli.helpers.files.FileWriterHelper;
import com.unbable.unbable_cli.models.Event;
import com.unbable.unbable_cli.models.Input;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentMatchers;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.DefaultApplicationArguments;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.fail;
import static org.mockito.Mockito.when;
import static org.mockito.Mockito.doNothing;

@SpringBootTest
public class CalculatorServiceTest {

    @Mock
    private OptionReaderHelper optionReaderHelper;

    @Mock
    private FileParserHelper fileParserHelper;

    @MockBean
    private FileWriterHelper fileWriterHelper;

    @Autowired
    @InjectMocks
    private CalculatorService calculatorService;

    private Input input;

    private List<Event> events;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.initMocks(this);
        input = new Input(10, new File("src/test/resources/events.json"));
        Event event = new Event();
        event.setTimestamp(LocalDateTime.now());
        event.setDuration(10);
        events = Collections.singletonList(event);
    }

    @Test
    public void test_generate_aggregated_output() {
        ApplicationArguments applicationArguments = new DefaultApplicationArguments("--window_size=10", "--input_file=src/test/resources/events.json");

        try {
            when(optionReaderHelper.getOptions(ArgumentMatchers.any(ApplicationArguments.class)))
                .thenReturn(
                    input
                );
            when(fileParserHelper.parseEvents(ArgumentMatchers.any(Input.class))).thenReturn(events);
            doNothing().when(fileWriterHelper).write(ArgumentMatchers.anyList(), ArgumentMatchers.anyString());
            calculatorService.generateAggregatedOutput(applicationArguments);
            assertTrue(true);
        } catch (IOException e) {
            fail();
        }
    }

    @Test
    public void test_generate_aggregated_output_empty() {
        ApplicationArguments applicationArguments = new DefaultApplicationArguments("--window_size=10", "--input_file=src/test/resources/events.json");

        try {
            when(optionReaderHelper.getOptions(ArgumentMatchers.any(ApplicationArguments.class)))
                .thenReturn(
                    input
                );
            when(fileParserHelper.parseEvents(ArgumentMatchers.any(Input.class))).thenReturn(Collections.emptyList());
            doNothing().when(fileWriterHelper).write(ArgumentMatchers.anyList(), ArgumentMatchers.anyString());
            calculatorService.generateAggregatedOutput(applicationArguments);
            fail();
        } catch (IOException e) {
            assertEquals("The file doesn't have valid events to process", e.getMessage());
        }
    }

}
