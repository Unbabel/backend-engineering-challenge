package com.unbable.unbable_cli.helpers;

import com.unbable.unbable_cli.models.Input;
import org.springframework.boot.ApplicationArguments;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.IOException;
import java.util.List;

@Component
public class OptionReaderHelper {

    public Input getOptions(ApplicationArguments arguments) throws IOException {
        return new Input(getWindowSize(arguments), getInputFile(arguments));
    }

    private File getInputFile(ApplicationArguments arguments) throws IOException {
        if (arguments.containsOption("input_file")) {
            List<String> inputFileArg = arguments.getOptionValues("input_file");
            File inputFile = new File(inputFileArg.get(0));

            if (!inputFile.exists() || !inputFile.canRead()) {
                throw new IOException("The input file doesn't exists or can't be read");
            }

            return inputFile;
        }

        throw new IOException("No input file provided");
    }

    private Integer getWindowSize(ApplicationArguments arguments) throws IOException {
        if (arguments.containsOption("window_size")) {
            List<String> windowSizeArg = arguments.getOptionValues("window_size");

            try {
                int windowSize = Integer.parseInt(windowSizeArg.get(0));

                if (windowSize<1) {
                    throw new IOException("The window size must be a positive integer");
                }
            } catch (NumberFormatException exception) {
                throw new IOException("The window size must be a valid integer");
            }

            return Integer.valueOf(windowSizeArg.get(0));
        }

        throw new IOException("No window size provided");
    }
}
