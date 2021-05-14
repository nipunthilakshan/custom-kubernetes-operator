package com.example.data.viewer.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;

import java.util.UUID;
import javax.servlet.ServletRequestEvent;
import javax.servlet.ServletRequestListener;

public class RequestListener implements ServletRequestListener {
    private static final Logger LOGGER = LoggerFactory.getLogger(RequestListener.class);
    private static final String REQUEST_ID = "RequestId";

    @Override
    public void requestInitialized(ServletRequestEvent arg0) {
        String uniqueId = UUID.randomUUID().toString();
        LOGGER.info("HttpReq[init]:RequestId|{}", uniqueId);
        MDC.put(REQUEST_ID, uniqueId);
    }

    @Override
    public void requestDestroyed(ServletRequestEvent arg0) {
        LOGGER.info("HttpReq[destroyed]:RequestId|{}", MDC.get(REQUEST_ID));
        MDC.clear();
    }
}
