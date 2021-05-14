package com.example.data.viewer.controller;

import com.example.data.viewer.model.ResponseModel;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/data/service")
public class ViewController {
    private static Logger log = LoggerFactory.getLogger(ViewController.class);

    @PostMapping(value = "/view")
    public ResponseEntity<ResponseModel> getDetails(@RequestBody String input) {

        ResponseModel resp = new ResponseModel();
        try {
            System.out.println(input);
            log.info("request body ---> {} ",input);
            resp.setResponseCode("4500");
            resp.setResponseDesc("Api call success");
            resp.setResponseData(input.toString());
            log.info("Api call success");
            log.info("Response data ---> "+resp.getResponseData());
            return ResponseEntity.status(200).body(resp);

        } catch (Exception e) {
            log.error(e.getMessage());
            resp.setResponseCode("4501");
            resp.setResponseDesc("Api call failed");
            resp.setResponseData(null);
            return ResponseEntity.status(400).body(resp);
        }

    }
}
