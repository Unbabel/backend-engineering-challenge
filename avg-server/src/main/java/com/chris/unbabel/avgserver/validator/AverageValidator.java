package com.chris.unbabel.avgserver.validator;

import com.chris.unbabel.avgserver.core.TranslationDeliveredPayload;

/**
 * Validates the #TranslationDeliveredPayload object
 */
@FunctionalInterface
public interface AverageValidator {

    /**
     * Check if the event payload is valid
     *
     * @param translationDeliveredPayload event to be validated
     */
    void validate(TranslationDeliveredPayload translationDeliveredPayload);
}
