package com.unbable.unbable_cli.helpers;

import com.unbable.unbable_cli.models.Output;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.File;
import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest
public class OutputWriterHelperTest {

    @Autowired
    private OutputWriterHelper outputWriterHelper;

    @Test
    public void test_write_to_file() {
        List<Output> outputList = Collections.singletonList(new Output(0.00, LocalDateTime.now()));
        File file = outputWriterHelper.writeListToFile(outputList, "src/test/resources/output.json");
        assertTrue(file.exists());
        assertTrue(file.length() > 0);
    }


}
