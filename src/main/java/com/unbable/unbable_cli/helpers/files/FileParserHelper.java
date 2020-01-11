package com.unbable.unbable_cli.helpers.files;

import com.unbable.unbable_cli.helpers.ParserHelper;
import com.unbable.unbable_cli.models.Event;
import com.unbable.unbable_cli.models.Input;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

@Component
public class FileParserHelper extends ParserHelper {

    /**
     * This method reads all the lines from the input file and it maps each one into an object Event
     * @param input events provided
     * @return List of events
     * @throws IOException exception in case of error reading the lines
     */
    @Override
    public List<Event> parseEvents(Input input) throws IOException {
        return Files.readAllLines(Paths.get(input.getInputFile().getAbsolutePath()))
            .stream()
            .map(this::mapEvent)
            .filter(Objects::nonNull)
            .sorted(Comparator.comparing(Event::getTimestamp))
            .collect(Collectors.toList());
    }
}
