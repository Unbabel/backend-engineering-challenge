package com.chris.unbabel.avgserver.core;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@EqualsAndHashCode
public class TranslationDeliveredPayload {
    private List<TranslationDelivered> transactionServiceList;
    private int windowSize;

    public TranslationDeliveredPayload() {
    }

    public TranslationDeliveredPayload(List<TranslationDelivered> transactionServiceList, int windowSize) {
        this.transactionServiceList = transactionServiceList;
        this.windowSize = windowSize;
    }
}
