package com.unbabel.translationDelivery.config;

import com.alibaba.fastjson2.TypeReference;
import com.unbabel.translationDelivery.listener.JobListener;
import com.unbabel.translationDelivery.processor.TransactionItemProcessor;
import com.unbabel.translationDelivery.reader.JsonEventItemRead;
import com.unbabel.translationDelivery.vo.EventRecordVo;
import com.unbabel.translationDelivery.writer.EventTranslationDeliveryWriter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.batch.core.Job;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.configuration.annotation.JobBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepBuilderFactory;
import org.springframework.batch.item.json.JsonItemReader;
import org.springframework.batch.item.json.builder.JsonItemReaderBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;

import java.util.Set;

@Configuration
public class BatchConfig {

    private static final Logger LOG = LoggerFactory.getLogger(BatchConfig.class);

    @Autowired
    public JobBuilderFactory jobBuilderFactory;

    @Autowired
    public StepBuilderFactory stepBuilderFactory;

    @Bean
    public Job processTransactionJob() {
        LOG.info("==INIT JOB EVENT TRANSLATION DELIVERED JOB==");
        return jobBuilderFactory.get("TranslationEventDeliveryJob")
                .listener(listener())
                .flow(processEventsFromJSON())
                .end()
                .build();
    }

    @Bean
    public Step processEventsFromJSON() {
        LOG.info("==SETTING EVENT TRANSLATION DELIVERED JOB==");
        return stepBuilderFactory.get("TranslationEventDeliveryJob")
                .<Set<EventRecordVo>, EventRecordVo>chunk(2)
                .reader(eventTranslationDeliveredReader())
                .processor(eventsProcessor())
                .writer(eventsWriter())
                .build();

    }

    @Bean
    public EventTranslationDeliveryWriter eventsWriter() {
        return new EventTranslationDeliveryWriter();
    }

    @Bean
    public TransactionItemProcessor eventsProcessor() {
        return new TransactionItemProcessor();
    }

    @Bean
    public JobListener listener() {
        return new JobListener();
    }

    @Bean
    public JsonItemReader<Set<EventRecordVo>> eventTranslationDeliveredReader() {
        JsonEventItemRead<Set<EventRecordVo>> jsonReader = new JsonEventItemRead<>(new TypeReference<Object[]>() {
        }.getType());
        LOG.info("==INIT READER EVENT TRANSLATION DELIVERED JOB==");
        ClassPathResource resource = new ClassPathResource("event.json");
        return new JsonItemReaderBuilder<Set<EventRecordVo>>()
                .resource(resource)
                .jsonObjectReader(jsonReader)
                .name("EventTranslationDelivered")
                .build();
    }
}
