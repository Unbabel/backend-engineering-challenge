package com.chris.unbabel;

import com.chris.unbabel.core.Event;
import com.chris.unbabel.core.TranslationDelivered;
import com.chris.unbabel.exception.TranslationEventException;
import com.chris.unbabel.handler.ArgumentChecker;
import com.chris.unbabel.handler.DataMapperHandler;
import com.chris.unbabel.handler.DataMapperHandlerImpl;
import com.chris.unbabel.service.AverageCalculatorService;
import com.chris.unbabel.service.AverageCalculatorServiceImpl;

import javax.annotation.Nonnull;
import java.io.File;
import java.util.List;

import static com.chris.unbabel.handler.ArgumentChecker.checkArgumentHelp;
import static com.chris.unbabel.handler.ArgumentChecker.checkInvalidArguments;
import static java.lang.System.exit;

public class App {
    private static final String SEPARATOR = "---";
    private static final AverageCalculatorService SERVICE = new AverageCalculatorServiceImpl();
    private static final DataMapperHandler MAPPER = new DataMapperHandlerImpl();

    public static void main(String... args) {

        try {
            checkInvalidArguments(args);
            checkArgumentHelp(args);

            printHeader();

            printResponse(callService(args));
        } catch (Exception e) {
            println(SEPARATOR);
            println("Failed to process: " + e.getMessage());
            exit(1);
        }
    }

    private static String callService(@Nonnull final String... args) throws TranslationEventException {
        String file = ArgumentChecker.getArgumentFile(args);
        int windowSize = ArgumentChecker.getArgumentWindow(args);

        List<TranslationDelivered> deliveredList = MAPPER.mapEvents(new File(file), Event.TRANSLATION_DELIVERED);

        return MAPPER.map(SERVICE.calculateAverageTime(deliveredList, windowSize));
    }

    private static void printHeader() {
        println(SEPARATOR);
        println("Backend Engineering Challenge");
        println(SEPARATOR);
        println("Calling service...");
    }

    private static void printResponse(String response) {
        println(SEPARATOR);

        println(response
                .replace("[", "")
                .replace("]", "")
                .replace("},", "}\n")
        );

        println(SEPARATOR);
    }

    public static void println(String input) {
        System.out.println(input);
    }
}
