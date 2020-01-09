package com.unbable.unbable_cli.helpers;

import com.unbable.unbable_cli.models.Input;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.DefaultApplicationArguments;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.IOException;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.fail;

@SpringBootTest
public class OptionReaderHelperTest {

    @Autowired
    private OptionReaderHelper optionReaderHelper;

    @Test
    public void test_get_options_successfully() {
        ApplicationArguments applicationArguments = new DefaultApplicationArguments("--window_size=10", "--input_file=events.json");

        try {
            Input input = optionReaderHelper.getOptions(applicationArguments);
            assertNotNull(input);
        } catch (IOException ex) {
            fail();
        }
    }

    @Test
    public void test_get_options_negative_window_format() {
        ApplicationArguments applicationArguments = new DefaultApplicationArguments("--window_size=-1", "--input_file=events.json");

        try {
            optionReaderHelper.getOptions(applicationArguments);
            fail();
        } catch (IOException ex) {
            assertEquals("The window size must be a positive integer", ex.getMessage());
        }
    }

    @Test
    public void test_get_options_wrong_window_format() {
        ApplicationArguments applicationArguments = new DefaultApplicationArguments("--window_size='hi'", "--input_file=events.json");

        try {
            optionReaderHelper.getOptions(applicationArguments);
            fail();
        } catch (IOException ex) {
            assertEquals("The window size must be a valid integer", ex.getMessage());
        }
    }

    @Test
    public void test_get_options_missing_window_format_arg() {
        ApplicationArguments applicationArguments = new DefaultApplicationArguments("--input_file=events.json");

        try {
            optionReaderHelper.getOptions(applicationArguments);
            fail();
        } catch (IOException ex) {
            assertEquals("No window size provided", ex.getMessage());
        }
    }

    @Test
    public void test_get_options_input_file_does_not_exists() {
        ApplicationArguments applicationArguments = new DefaultApplicationArguments("--window_size=10", "--input_file=wrong.json");

        try {
            optionReaderHelper.getOptions(applicationArguments);
            fail();
        } catch (IOException ex) {
            assertEquals("The input file doesn't exists or can't be read", ex.getMessage());
        }
    }

    @Test
    public void test_get_options_missing_input_file_arg() {
        ApplicationArguments applicationArguments = new DefaultApplicationArguments("--window_size=10");

        try {
            optionReaderHelper.getOptions(applicationArguments);
            fail();
        } catch (IOException ex) {
            assertEquals("No input file provided", ex.getMessage());
        }
    }
}
