package com.unbable.unbable_cli.helpers.files;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.unbable.unbable_cli.helpers.OutputWriterHelper;
import com.unbable.unbable_cli.models.Output;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.List;

@Component
@Slf4j
public class FileWriterHelper extends OutputWriterHelper {

    @Autowired
    private ObjectMapper objectMapper;

    /**
     * This method it's in charge of writing the list of Output objects provided
     * into a new output file. If the file exists, it deletes all the lines and creates a new one.
     *
     * @param outputList List of Output objects
     * @param outputName Name of the file to write
     */
    @Override
    public void write(List<Output> outputList, String outputName) {
        File outputFile = new File(outputName);
        Path path = Paths.get(outputFile.getAbsolutePath());
        if (outputFile.exists() && outputFile.length() > 0) {
            outputFile.delete();
        }

        outputList.forEach(
            it -> {
                try {
                    String content = objectMapper.writeValueAsString(it);
                    Files.write(
                        path,
                        (content + System.lineSeparator()).getBytes(),
                        StandardOpenOption.CREATE,
                        StandardOpenOption.APPEND
                    );
                } catch (IOException e) {
                    log.info("The output {}, could not be write into the file", it, e);
                }
            });
    }
}
