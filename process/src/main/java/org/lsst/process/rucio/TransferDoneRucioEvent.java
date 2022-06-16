package org.lsst.process.rucio;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * Representation of the "transfer-done" Rucio event
 */
public class TransferDoneRucioEvent {
    @JsonProperty("event_type")
    String eventType;

    @JsonProperty("payload")
    TransferDonePayload payload;

    @JsonProperty("created_at")
    String createdAt;

    public String toString() {
        return "event_type: "+eventType+" "+payload.toString();
    }
}

