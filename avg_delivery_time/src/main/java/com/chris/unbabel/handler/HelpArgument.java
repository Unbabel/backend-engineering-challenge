package com.chris.unbabel.handler;

import com.chris.unbabel.App;


final class HelpArgument {
    private static final String SEPARATOR = "\n---------------------------------------------------------------------------------\n";
    private static final String TAB = "\t\t";
    private static final String HELP =
            SEPARATOR +
                    "Welcome to [Backend Engineering Challenge]" +
                    SEPARATOR +
                    TAB +
                    ArgumentChecker.ARG_HELP + " : Open this help\n" +
                    TAB +
                    "Usage: \n" +
                    TAB +
                    "$ ./unbabel_cli --input_file=<FILE_NAME>  --window_size=<int value> [--help]" +
                    "\n\n" +
                    "Example:\n" +
                    TAB +
                    "$ ./unbabel_cli --input_file=input.json --window_size=10\n" +
                    TAB +
                    "$ ./unbabel_cli --help\n\n";

    private HelpArgument() {
        //
    }

    static void printHelp() {
        App.println(HELP);

        System.exit(0);
    }
}