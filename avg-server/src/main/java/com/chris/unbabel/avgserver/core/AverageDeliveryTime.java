package com.chris.unbabel.avgserver.core;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.common.base.MoreObjects;
import lombok.Getter;
import lombok.Setter;

import javax.annotation.Nonnull;
import java.io.Serializable;
import java.util.Date;
import java.util.Objects;

import static com.chris.unbabel.avgserver.util.DateUtils.DATE_FORMAT;

/**
 * Average Delivery Time data object.
 * Used as output value.
 */
@Getter
@Setter
public class AverageDeliveryTime implements Serializable {
    private static final long serialVersionUID = 8047746517213578294L;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = DATE_FORMAT)
    private Date date;

    @JsonProperty("average_delivery_time")
    private double avgTime;

    public AverageDeliveryTime() {
    }

    public AverageDeliveryTime(@Nonnull AverageDeliveryTime avg) {
        this.date = avg.getDate();
        this.avgTime = avg.getAvgTime();
    }

    public AverageDeliveryTime(Date date, double avgTime) {
        this.date = date;
        this.avgTime = avgTime;
    }

    public static AverageDeliveryTime build(Date date, double avgTime){
        return new AverageDeliveryTime(date, avgTime);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        AverageDeliveryTime that = (AverageDeliveryTime) o;
        return date.equals(that.date);
    }

    @Override
    public int hashCode() {
        return Objects.hash(date);
    }

    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
                .add("date", date)
                .add("averageDeliveryTime", avgTime)
                .toString();
    }
}
