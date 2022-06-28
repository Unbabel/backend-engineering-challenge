package com.unbabel.translationDelivery.writer;

import com.unbabel.translationDelivery.config.BatchConfig;
import com.unbabel.translationDelivery.vo.EventRecordVo;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.batch.item.ItemWriter;

import java.util.List;

public class EventTranslationDeliveryWriter implements ItemWriter<EventRecordVo> {
    private static final Logger LOG = LoggerFactory.getLogger(BatchConfig.class);

    /**
     * @param eventRecordVos
     * @throws Exception
     */
    @Override
    public void write(List<? extends EventRecordVo> eventRecordVos) throws Exception {
        LOG.info("==WRITER TRANSLATION DELIVERED==");
        for (EventRecordVo event : eventRecordVos) {
            LOG.info("event: " + event.getEvent_name());
        }
    }
}
