package org.lsst.process.rucio;

import com.fasterxml.jackson.annotation.JsonProperty;

/*
 * Payload section of the "transfer-done" event
 *
 * EXAMPLE::

{"reason":"","dst-url":"root://xrd3:1096//rucio/test/79/64/file1_1cdc7d0c-7c14-439c-bc31-0f226d00c10f","activity":"User Subscriptions","submitted_at":"2022-05-05 16:20:34.644759","dst-type":"DISK","transfer-endpoint":"https://fts:8446","created_at":"2022-05-05 16:20:04.135878","src-type":"DISK","duration":4,"protocol":"root","scope":"test","dst-rse":"XRD3","transferred_at":"2022-05-05 16:20:41","src-rse":"XRD1","checksum-md5":"96495fba673e6fd1263e7d3a67e69215","request-id":"09765bdf53164c7b8207740ee60b2450","previous-request-id":null,"transfer-link":null,"bytes":5959,"file-size":5959,"name":"file1_1cdc7d0c-7c14-439c-bc31-0f226d00c10f","src-url":"root://xrd1:1094//rucio/test/79/64/file1_1cdc7d0c-7c14-439c-bc31-0f226d00c10f","guid":null,"started_at":"2022-05-05 16:20:37","tool-id":"rucio-conveyor","checksum-adler":"4616689d","transfer-id":"4aa13ec2-cc8f-11ec-a22a-0242ac130002","account":"root","transfer_link":"https://fts:8449/fts3/ftsmon/#/job/4aa13ec2-cc8f-11ec-a22a-0242ac130002"}

*/

public class TransferDonePayload {
        @JsonProperty("reason")
        String reason;

        @JsonProperty("dst-url")
        String dstUrl;

        @JsonProperty("activity")
        String activity;

        @JsonProperty("submitted_at")
        String submittedAt;

        @JsonProperty("dst-type")
        String dstType;

        @JsonProperty("transfer-endpoint")
        String transferEndpoint;

        @JsonProperty("created_at")
        String createdAt;

        @JsonProperty("src-type")
        String srcType;

        @JsonProperty("duration")
        Integer duration;

        @JsonProperty("protocol")
        String protocol;

        @JsonProperty("scope")
        String scope;

        @JsonProperty("dst-rse")
        String dstRse;

        @JsonProperty("transferred_at")
        String transferredAt;

        @JsonProperty("src-rse")
        String srcRse;

        @JsonProperty("checksum-md5")
        String checksumMD5;

        @JsonProperty("request-id")
        String requestId;

        @JsonProperty("previous-request-id")
        String previousRequestid;

        @JsonProperty("transfer-link")
        String transferLink;

        @JsonProperty("bytes")
        Integer bytes;

        @JsonProperty("file-size")
        Integer fileSize;

        @JsonProperty("name")
        String name;

        @JsonProperty("src-url")
        String srcURL;

        @JsonProperty("guid")
        String guid;

        @JsonProperty("started_at")
        String startedAt;

        @JsonProperty("tool-id")
        String toolId;

        @JsonProperty("checksum-adler")
        String checksumAdler;

        @JsonProperty("transfer-id")
        String transferId;

        @JsonProperty("account")
        String account;

        @JsonProperty("transfer_link")
        String transferLink2;

    public String toString() {
            String s = "dst-rse: "+dstRse+" dst-url: "+dstUrl;
            return s;
    }
}
