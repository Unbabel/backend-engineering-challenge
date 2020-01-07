package com.unbable.unbable_cli.services;

import com.unbable.unbable_cli.helpers.OutputWriterHelper;
import com.unbable.unbable_cli.models.Event;
import com.unbable.unbable_cli.models.Input;
import com.unbable.unbable_cli.models.Output;
import com.unbable.unbable_cli.helpers.EventReaderHelper;
import com.unbable.unbable_cli.helpers.FileParserHelper;
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
    private FileParserHelper fileParserHelper;

    @Autowired
    private EventReaderHelper eventReaderHelper;

    @Autowired
    private OutputWriterHelper outputWriterHelper;

    public void generateAggregatedOutput(ApplicationArguments arguments) throws IOException {
        List<Output> outputList = getOutputList(arguments);
        outputWriterHelper.writeListToFile(outputList);
    }

    private List<Output> getOutputList(ApplicationArguments arguments) throws IOException {
        Input input = optionReaderHelper.getOptions(arguments);
        List<Event> events = fileParserHelper.parseFileEvents(input.getInputFile());
        LocalDateTime startMinute = events.get(0).getTimestamp().truncatedTo(ChronoUnit.MINUTES);
        LocalDateTime endMinute = events.get(events.size() - 1).getTimestamp().truncatedTo(ChronoUnit.MINUTES).plusMinutes(1);
        log.info("start {} end {}", startMinute, endMinute);
        log.info("window_size: {}, events: {}", input.getWindowSize(), events);

        return calculateAverage(startMinute, endMinute, input.getWindowSize(), events);
    }

    private List<Output> calculateAverage(LocalDateTime startMinute, LocalDateTime endMinute, int windowSize, List<Event> events) {
        List<Output> outputList = new ArrayList<>();

        for (LocalDateTime start = startMinute; start.compareTo(endMinute) <= 0; start = start.plusMinutes(1)) {
            List<Event> eventsFiltered = eventReaderHelper.filterByWindow(events, start, windowSize);
            double average = eventsFiltered.stream().mapToInt(Event::getDuration).average().orElse(0);

            Output output = new Output(average, start);
            outputList.add(output);
            System.out.println("date: " + start + " average_delivery_time: " + average);
        }

        return outputList;
    }
}
