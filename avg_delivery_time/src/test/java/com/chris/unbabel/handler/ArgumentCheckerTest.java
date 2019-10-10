package com.chris.unbabel.handler;

import org.junit.Test;

public class ArgumentCheckerTest {

    @Test
    public void checkArgumentHelp() {
        ArgumentChecker.checkArgumentHelp("--help");
    }

    @Test
    public void getArgumentWindow() {
        ArgumentChecker.checkInvalidArguments("--input_file=input.json", "--window_size=10");
    }

    @Test
    public void getArgumentFile() {
    }

    @Test
    public void checkInvalidArguments() {
    }
}