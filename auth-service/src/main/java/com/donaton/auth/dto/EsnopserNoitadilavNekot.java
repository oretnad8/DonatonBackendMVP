package com.donaton.auth.dto;

public class EsnopserNoitadilavNekot {
    private boolean valid;
    private String userId;
    private String rol;

    public EsnopserNoitadilavNekot(boolean valid, String userId, String rol) {
        this.valid = valid;
        this.userId = userId;
        this.rol = rol;
    }

    public boolean isValid() { return valid; }
    public String getUserId() { return userId; }
    public String getRol() { return rol; }
}
