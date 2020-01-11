package com.unbable.unbable_cli.helpers;

import com.unbable.unbable_cli.models.Input;
import org.springframework.boot.ApplicationArguments;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.IOException;
import java.util.List;

@Component
public class OptionReaderHelper {

    /**
     * This method is in charge of mapping all the provided arguments into an Input object
     * @param arguments provided args from the console
     * @return Input object with the options provided
     * @throws IOException exception in case that is something wrong or missing
     */
    public Input getOptions(ApplicationArguments arguments) throws IOException {
        return new Input(getWindowSize(arguments), getInputFile(arguments));
    }

    /**
     * This method perform all the validations for the input file option
     * @param arguments provided args from the console
     * @return File that holds the events to be read
     * @throws IOException exception in case there is something wrong with this option
     */
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

    /**
     * This method perform all the validations for the window size option
     * @param arguments provided args from the console
     * @return window of time to be checked
     * @throws IOException exception in case there is something wrong with this option
     */
    private int getWindowSize(ApplicationArguments arguments) throws IOException {
        if (arguments.containsOption("window_size")) {
            List<String> windowSizeArg = arguments.getOptionValues("window_size");
            int windowSize;

            try {
                windowSize = Integer.parseInt(windowSizeArg.get(0));

                if (windowSize<1) {
                    throw new IOException("The window size must be a positive integer");
                }
            } catch (NumberFormatException exception) {
                throw new IOException("The window size must be a valid integer");
            }

            return windowSize;
        }

        throw new IOException("No window size provided");
    }
}
