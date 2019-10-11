package com.chris.unbabel.avgserver.validator;

import com.chris.unbabel.avgserver.core.TranslationDeliveredPayload;
import org.springframework.stereotype.Component;

import static com.google.common.base.Preconditions.checkNotNull;

@Component
public class AverageValidatorImpl implements AverageValidator {

    @Override
    public void validate(TranslationDeliveredPayload translationDeliveredPayload) {
        checkNotNull(translationDeliveredPayload);
        checkWindowSize(translationDeliveredPayload);
    }

    private void checkWindowSize(TranslationDeliveredPayload translationDeliveredPayload) {
        if (translationDeliveredPayload.getWindowSize() <= 0) {
            throw new IllegalArgumentException("Windows size must be greater than 0");
        }
    }
}
