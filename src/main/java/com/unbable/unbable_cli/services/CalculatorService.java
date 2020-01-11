package com.unbable.unbable_cli.services;

import com.unbable.unbable_cli.helpers.files.FileWriterHelper;
import com.unbable.unbable_cli.models.Event;
import com.unbable.unbable_cli.models.Input;
import com.unbable.unbable_cli.models.Output;
import com.unbable.unbable_cli.helpers.EventReaderHelper;
import com.unbable.unbable_cli.helpers.ParserHelper;
import com.unbable.unbable_cli.helpers.OptionReaderHelper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;

@Service
@Slf4j
public class CalculatorService {

    @Autowired
    private OptionReaderHelper optionReaderHelper;

    @Autowired
    private ParserHelper parserHelper;

    @Autowired
    private EventReaderHelper eventReaderHelper;

    @Autowired
    private FileWriterHelper fileWriterHelper;

    /**
     * This method is the one in charge to get the outputList and call the OutputWriterHelper with it
     * @param arguments console args
     * @throws IOException exception in case something went wrong
     */
    public void generateAggregatedOutput(ApplicationArguments arguments) throws IOException {
        List<Output> outputList = getOutputList(arguments);
        fileWriterHelper.write(outputList, "output.json");
    }

    /**
     * This method is the one that generates the List of Outputs with the required calculations
     * @param arguments console args
     * @return List of Outputs
     * @throws IOException exception in case something went wrong
     */
    private List<Output> getOutputList(ApplicationArguments arguments) throws IOException {
        Input input = optionReaderHelper.getOptions(arguments);
        List<Event> events = parserHelper.parseEvents(input);

        if (!events.isEmpty()) {
            LocalDateTime startMinute = events.get(0).getTimestamp().truncatedTo(ChronoUnit.MINUTES);
            LocalDateTime endMinute = events.get(events.size() - 1).getTimestamp().truncatedTo(ChronoUnit.MINUTES).plusMinutes(1);
            log.info("start {} end {}", startMinute, endMinute);
            log.info("window_size: {}, events: {}", input.getWindowSize(), events.size());

            return calculateAverage(startMinute, endMinute, input.getWindowSize(), events);
        }

        throw new IOException("The file doesn't have valid events to process");
    }

    /**
     * This method is the one that finally perform the average calculation for each event
     * and creates the List of Output objects
     * @param startMinute timestamp for the first event truncated to minutes
     * @param endMinute timestamp for the last event truncated to the next minute
     * @param windowSize window size provided
     * @param events List of events
     * @return List of Output with the aggregated information
     */
    private List<Output> calculateAverage(LocalDateTime startMinute, LocalDateTime endMinute, int windowSize, List<Event> events) {
        List<Output> outputList = new ArrayList<>();

        for (LocalDateTime start = startMinute; start.compareTo(endMinute) <= 0; start = start.plusMinutes(1)) {
            List<Event> eventsFiltered = eventReaderHelper.filterByWindow(events, start, windowSize);
            double average = eventsFiltered.stream().mapToInt(Event::getDuration).average().orElse(0);

            Output output = new Output(average, start);
            outputList.add(output);
        }

        return outputList;
    }
}
