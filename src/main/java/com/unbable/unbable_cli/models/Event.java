package com.unbable.unbable_cli.models;

import com.fasterxml.jackson.annotation.JsonFormat;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.datatype.jsr310.deser.LocalDateTimeDeserializer;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
public class Event {

    @JsonDeserialize(using = LocalDateTimeDeserializer.class)
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss.SSSSSS")
    private LocalDateTime timestamp;

    @JsonProperty("translation_id")
    private String translationId;

    @JsonProperty("source_language")
    private String sourceLanguage;

    @JsonProperty("target_language")
    private String targetLanguage;

    @JsonProperty("client_name")
    private String clientName;

    @JsonProperty("event_name")
    private String eventName;

    @JsonProperty("nr_words")
    private Integer nrWords;

    private Integer duration;
}
