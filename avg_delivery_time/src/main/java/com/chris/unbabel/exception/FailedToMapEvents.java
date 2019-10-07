package com.chris.unbabel.exception;

public class FailedToMapEvents extends TranslationEventException {

    private static final long serialVersionUID = 4774039726846145963L;

    public FailedToMapEvents(Throwable cause) {
        super(cause);
    }
}
