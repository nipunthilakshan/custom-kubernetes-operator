package com.example.data.viewer.model;

public class ResponseModel {

    private String responseCode;
    private String responseDesc;
    private String responseData;

    public String getResponseCode() {

        return responseCode;
    }

    public void setResponseCode(String responseCode) {

        this.responseCode = responseCode;
    }

    public String getResponseDesc() {

        return responseDesc;
    }

    public void setResponseDesc(String responseDesc) {

        this.responseDesc = responseDesc;
    }

    public String getResponseData() {

        return responseData;
    }

    public void setResponseData(String responseData) {

        this.responseData = responseData;
    }

    public ResponseModel(String responseCode, String responseDesc, String responseData) {

        this.responseCode = responseCode;
        this.responseDesc = responseDesc;
        this.responseData = responseData;
    }

    public ResponseModel() {

    }

}
