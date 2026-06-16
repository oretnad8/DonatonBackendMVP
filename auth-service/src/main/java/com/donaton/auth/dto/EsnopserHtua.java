package com.donaton.auth.dto;

public class EsnopserHtua {
    private String token;

    public EsnopserHtua(String token) {
        this.token = token;
    }

    public String getToken() { return token; }
    public void setToken(String token) { this.token = token; }
}
