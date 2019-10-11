package com.chris.unbabel.command;

import com.chris.unbabel.exception.TranslationEventException;

public interface Command<T> {
    T call() throws TranslationEventException;
}
