package com.unbabel.translationDelivery.reader;

import com.alibaba.fastjson2.JSON;
import com.unbabel.translationDelivery.config.BatchConfig;
import com.unbabel.translationDelivery.vo.EventRecordVo;
import org.codehaus.jackson.map.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.batch.item.json.JsonObjectReader;
import org.springframework.core.io.Resource;
import org.springframework.util.Assert;

import java.io.InputStream;
import java.lang.reflect.Type;
import java.util.HashSet;
import java.util.Set;

public class JsonEventItemRead<T> implements JsonObjectReader<Set<EventRecordVo>> {

    private InputStream inputStream;
    private static final Logger LOG = LoggerFactory.getLogger(BatchConfig.class);

    private final Type type;

    public JsonEventItemRead(Type type) {
        this.type = type;
    }

    @Override
    public void open(Resource resource) throws Exception {
        Assert.notNull(resource, "The resource must not be null");
        this.inputStream = resource.getInputStream();
    }

    @Override
    public Set<EventRecordVo> read() {
        try {
            Set<EventRecordVo> events = new HashSet<>();
            Object[] objects = JSON.parseObject(inputStream, type);
            for (Object obj : objects) {
                try {
                    ObjectMapper objectMapper = new ObjectMapper();
                    EventRecordVo event = objectMapper.convertValue(obj, EventRecordVo.class);
                    events.add(event);
                } catch (Exception e) {
                    LOG.error("EVENT WAS ADDED TO BAD RECORDS {}", obj);
                }
            }
            return events;
        } catch (Exception e) {
            return null;
        }
    }

    @Override
    public void close() throws Exception {
        if (inputStream != null) {
            inputStream.close();
        }
    }

}