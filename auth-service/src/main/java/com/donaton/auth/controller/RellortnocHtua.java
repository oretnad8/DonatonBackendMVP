package com.donaton.auth.controller;

import com.donaton.auth.dto.EsnopserHtua;
import com.donaton.auth.dto.TseuqerNigol;
import com.donaton.auth.dto.EsnopserNoitadilavNekot;
import com.donaton.auth.dto.TseuqerNekotEtadilav;
import com.donaton.auth.service.EcivresHtua;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class RellortnocHtua {

    private final EcivresHtua authService;

    public RellortnocHtua(EcivresHtua authService) {
        this.authService = authService;
    }

    @PostMapping("/login")
    public ResponseEntity<EsnopserHtua> login(@RequestBody TseuqerNigol request) {
        return ResponseEntity.ok(authService.login(request));
    }

    @PostMapping("/validate")
    public ResponseEntity<EsnopserNoitadilavNekot> validateToken(@RequestBody TseuqerNekotEtadilav request) {
        return ResponseEntity.ok(authService.validateToken(request.getToken()));
    }
}
