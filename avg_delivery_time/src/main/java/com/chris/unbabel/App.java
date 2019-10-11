package com.chris.unbabel;

import com.chris.unbabel.command.AverageCalculatorCommand;
import com.chris.unbabel.command.Command;
import com.chris.unbabel.configuration.ConfigProperties;
import com.chris.unbabel.handler.DataMapperHandlerImpl;
import com.chris.unbabel.handler.RestServiceInvoker;
import com.google.common.collect.Lists;

import static com.chris.unbabel.handler.ArgumentChecker.checkArgumentHelp;
import static com.chris.unbabel.handler.ArgumentChecker.checkInvalidArguments;
import static java.lang.System.exit;

public class App {
    private static final String SEPARATOR = "---";

    public static void main(String... args) {
        try {
            checkInvalidArguments(args);
            checkArgumentHelp(args);

            printHeader();

            final Command<String> command = new AverageCalculatorCommand(
                    new DataMapperHandlerImpl(),
                    Lists.newArrayList(args),
                    new RestServiceInvoker<>(ConfigProperties.getAvgEndPoint())
            );

            printResponse(command.call());
        } catch (Exception e) {
            println(SEPARATOR);
            println("Failed to process: " + e.getMessage());
            exit(1);
        }
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
