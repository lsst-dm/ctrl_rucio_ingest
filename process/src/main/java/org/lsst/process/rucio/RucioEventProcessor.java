package org.lsst.process.rucio;

import org.lsst.process.rucio.TransferDoneRucioEvent;
import org.apache.camel.Exchange;
import org.apache.camel.Processor;
import org.json.JSONException;
import org.json.JSONObject;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Rucio json event Camel processor
 */
public class RucioEventProcessor implements Processor {

    private static final Logger logger = LogManager.getLogger(RucioEventProcessor.class.getName());

    /**
     * Processes Rucio JSON-formatted transfer-done events, 
     * setting the dst-rse and dst-url attributes into the header of the
     * messages so they can be filtered externally
     *
     * Note that if support for additional events need to be added,
     * a custom class must be written for each one, because the payload portion of
     * the event is different in each case.
     */
    public void process(Exchange exchange) throws Exception {
        String body = exchange.getIn().getBody(String.class);

        JSONObject json = new JSONObject(body);
        String eventType = json.getString("event_type");

        // only filter "transfer-done" events
        if (eventType.equals("transfer-done")) {
            String jsonData = json.toString();

            // map the json data to a Java Object
            ObjectMapper objectMapper = new ObjectMapper();
            TransferDoneRucioEvent transferDoneRucioEvent = objectMapper.readValue(jsonData, TransferDoneRucioEvent.class);

            logger.info("TransferDoneRucioEvent: {}", transferDoneRucioEvent);
            logger.info("dst-rse: {}; dst-url: {}" , transferDoneRucioEvent.payload.dstRse, transferDoneRucioEvent.payload.dstUrl);

            // set the header values of the event attributes dst-rse, and dst-url in the payload
            exchange.getIn().setHeader("dstRse",transferDoneRucioEvent.payload.dstRse);
            exchange.getIn().setHeader("dstUrl",transferDoneRucioEvent.payload.dstUrl);
        } else {
            // set all other event headers to default values
            logger.info("got {} event", eventType);
            exchange.getIn().setHeader("dstRse", "do-not-route");
            exchange.getIn().setHeader("dstUrl", "http://www.lsst.org/");
        }
    }
}
