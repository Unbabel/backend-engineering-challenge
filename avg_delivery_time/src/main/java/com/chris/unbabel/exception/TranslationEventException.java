package com.chris.unbabel.exception;

public class TranslationEventException extends Exception {
    private static final long serialVersionUID = -7302810471345137465L;

    /**
     * Constructs a new exception with {@code null} as its detail message.
     * The cause is not initialized, and may subsequently be initialized by a
     * call to {@link #initCause}.
     */
    public TranslationEventException() {
    }

    public TranslationEventException(Throwable cause) {
        super(cause);
    }
}
