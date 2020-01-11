package com.unbable.unbable_cli.helpers;

import com.unbable.unbable_cli.models.Output;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@Slf4j
public abstract class OutputWriterHelper {

    /**
     * This method is in charge of writing the list of Output objects provided
     * into a new output. If the file exists, it deletes all the lines and creates a new one.
     * @param outputList List of Output objects
     * @param outputName Name of the file to write
     */
    public abstract void write(List<Output> outputList, String outputName);
}
