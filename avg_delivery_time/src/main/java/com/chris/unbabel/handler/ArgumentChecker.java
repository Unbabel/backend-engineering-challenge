package com.chris.unbabel.handler;

import com.chris.unbabel.exception.TranslationEventException;
import com.google.common.collect.Lists;

import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import static com.google.common.base.Preconditions.checkArgument;
import static org.apache.commons.lang3.ArrayUtils.isEmpty;

public final class ArgumentChecker {
    private static final String ARG_TOKEN = "--";
    private static final String ARG_INPUT_FILE = ARG_TOKEN + "input_file";
    private static final String ARG_WINDOW_SIZE = ARG_TOKEN + "window_size";
    static final String ARG_HELP = ARG_TOKEN + "help";
    private static final String SPLIT_TOKEN = "=";

    private static final Collection<String> SUPPORTED_OPTIONS = Lists.newArrayList(ARG_INPUT_FILE, ARG_WINDOW_SIZE, ARG_HELP);

    private ArgumentChecker() {
        //
    }

    public static void checkArgumentHelp(String... args) {
        if (Arrays.asList(args).contains(ARG_HELP)) {
            HelpArgument.printHelp();
        }
    }

    public static int getArgumentWindow(String... args) throws TranslationEventException {
        return Integer.parseInt(getArg(ARG_WINDOW_SIZE, args).trim());
    }

    public static String getArgumentFile(String... args) throws TranslationEventException {
        return getArg(ARG_INPUT_FILE, args);
    }

    public static void checkInvalidArguments(String... args) {
        checkArgument(!isEmpty(args),
                "Error to execute command:\n" +
                        "The arguments cannot be empty. Type --help for help.\n\n");

        List<String> invalidArguments = Stream.of(args)
                .filter(argument -> SUPPORTED_OPTIONS.stream().noneMatch(argument::startsWith))
                .collect(Collectors.toList());

        checkArgument(invalidArguments.isEmpty(),
                "Error to execute command:\n" +
                        "The argument(s) (" + String.join(", ", invalidArguments) + ") is not supported. Type --help for help.\n\n");
    }

    private static String getArg(String token, String... args) throws TranslationEventException {
        return Stream.of(args)
                .filter(arg -> arg.startsWith(token))
                .map(arg -> arg.split(SPLIT_TOKEN))
                .filter(arg -> args.length == 2)
                .map(arg -> arg[1])
                .findFirst()
                .orElseThrow(TranslationEventException::new);
    }
}