package com.chris.unbabel.core;

public enum Event {
    TRANSLATION_DELIVERED("translation_delivered");

    private String name;

    Event(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
