package com.chris.unbabel.avgserver;

import com.chris.unbabel.avgserver.core.AverageDeliveryTime;
import com.chris.unbabel.avgserver.core.TranslationDeliveredPayload;
import org.springframework.cloud.function.adapter.aws.SpringBootRequestHandler;

import java.util.Collection;

/**
 * Handle the Translation payload function data
 */
public class SpringLambdaHandler extends SpringBootRequestHandler<TranslationDeliveredPayload, Collection<AverageDeliveryTime>> {

}
