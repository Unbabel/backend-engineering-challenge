package com.unbabel.translationDelivery.processor;

import com.unbabel.translationDelivery.config.BatchConfig;
import com.unbabel.translationDelivery.vo.EventRecordVo;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.batch.item.ItemProcessor;

import java.util.List;
import java.util.Map;
import java.util.Set;

public class TransactionItemProcessor implements ItemProcessor<Set<EventRecordVo>, EventRecordVo>{
	private static final Logger LOG = LoggerFactory.getLogger(BatchConfig.class);
	/**
	 * @param eventRecordVo
	 * @return
	 * @throws Exception
	 */
	@Override
	public EventRecordVo process(Set<EventRecordVo> eventRecordVo) throws Exception {
		LOG.info("==INIT PROCESSOR EVENT TRANSLATION DELIVERED JOB==");
		return eventRecordVo.stream().findFirst().get();
	}

}
