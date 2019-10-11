package com.chris.unbabel.data;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;

import javax.xml.bind.annotation.XmlRootElement;
import java.io.Serializable;
import java.util.List;

@Getter
@Setter
@EqualsAndHashCode
@XmlRootElement
public class TranslationDeliveredPayload implements Serializable {
    private static final long serialVersionUID = -8459761044714751934L;

    private List<TranslationDelivered> transactionServiceList;
    private int windowSize;

    public TranslationDeliveredPayload() {
    }

    public TranslationDeliveredPayload(List<TranslationDelivered> transactionServiceList, int windowSize) {
        this.transactionServiceList = transactionServiceList;
        this.windowSize = windowSize;
    }
}
