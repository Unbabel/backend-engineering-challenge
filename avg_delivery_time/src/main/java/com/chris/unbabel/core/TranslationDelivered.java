package com.chris.unbabel.core;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.common.base.MoreObjects;
import lombok.Getter;
import lombok.Setter;

import javax.annotation.Nonnull;
import java.io.Serializable;
import java.util.Date;
import java.util.Objects;

import static com.chris.unbabel.util.DateUtils.DATE_FORMAT;

/**
 * Translation Delivered data from an event stream.
 */
@Getter
@Setter
public class TranslationDelivered implements Serializable {
    private static final long serialVersionUID = -7312693523679168709L;

    @JsonProperty("timestamp")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = DATE_FORMAT)
    public Date timestamp;

    @JsonProperty("translation_id")
    public String translationId;

    @JsonProperty("source_language")
    public String sourceLanguage;

    @JsonProperty("target_language")
    public String targetLanguage;

    @JsonProperty("client_name")
    public String clientName;

    @JsonProperty("event_name")
    public String eventName;

    @JsonProperty("nr_words")
    public long nrWords;

    @JsonProperty("duration")
    public double duration;

    public TranslationDelivered() {
    }

    public TranslationDelivered(@Nonnull TranslationDelivered delivered) {
        timestamp = delivered.timestamp;
        translationId = delivered.translationId;
        sourceLanguage = delivered.sourceLanguage;
        targetLanguage = delivered.targetLanguage;
        clientName = delivered.clientName;
        eventName = delivered.eventName;
        nrWords = delivered.nrWords;
        duration = delivered.duration;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        TranslationDelivered that = (TranslationDelivered) o;
        return translationId.equals(that.translationId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(translationId);
    }

    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
                .add("timestamp", timestamp)
                .add("translationId", translationId)
                .add("sourceLanguage", sourceLanguage)
                .add("targetLanguage", targetLanguage)
                .add("clientName", clientName)
                .add("eventName", eventName)
                .add("duration", duration)
                .add("nrWords", nrWords)
                .toString();
    }
}
