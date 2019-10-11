package com.chris.unbabel.configuration;

import java.util.ResourceBundle;

public class ConfigProperties {
    private static final ResourceBundle PROPERTIES =  ResourceBundle.getBundle("configuration");

    private ConfigProperties() {
    }

    public static String getAvgEndPoint() {
        return PROPERTIES.getString("avg.endpoint");
    }
}
