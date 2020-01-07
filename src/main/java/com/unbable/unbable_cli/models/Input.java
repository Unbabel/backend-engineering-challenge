package com.unbable.unbable_cli.models;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.io.File;

@Getter
@Setter
@AllArgsConstructor
public class Input {

    private int windowSize;

    private File inputFile;
}
