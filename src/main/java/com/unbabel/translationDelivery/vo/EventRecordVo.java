package com.unbabel.translationDelivery.vo;


import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import lombok.ToString;
import lombok.Setter;
import lombok.Getter;

import java.util.Date;

/**
 * Event Class
 */
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@ToString
public class EventRecordVo {

    String timestamp;
    String translation_id;
    String source_language;
    String target_language;
    String client_name;
    String event_name;
    int duration;
    int nr_words;
}
