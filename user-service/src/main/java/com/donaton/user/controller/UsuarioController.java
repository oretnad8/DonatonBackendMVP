package com.donaton.user.controller;

import com.donaton.user.dto.UsuarioRequestDTO;
import com.donaton.user.dto.UsuarioResponseDTO;
import com.donaton.user.service.UsuarioService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/usuarios")
public class UsuarioController {

    private final UsuarioService usuarioService;

    public UsuarioController(UsuarioService usuarioService) {
        this.usuarioService = usuarioService;
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN_SENAPRED')")
    public ResponseEntity<UsuarioResponseDTO> crearUsuario(@RequestBody UsuarioRequestDTO request) {
        return new ResponseEntity<>(usuarioService.crearUsuario(request), HttpStatus.CREATED);
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN_SENAPRED') or #id.toString() == authentication.principal")
    public ResponseEntity<UsuarioResponseDTO> obtenerUsuario(@PathVariable UUID id) {
        return ResponseEntity.ok(usuarioService.obtenerUsuario(id));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN_SENAPRED') or #id.toString() == authentication.principal")
    public ResponseEntity<UsuarioResponseDTO> actualizarUsuario(@PathVariable UUID id, @RequestBody UsuarioRequestDTO request) {
        return ResponseEntity.ok(usuarioService.actualizarContacto(id, request.getEmail(), request.getNombre(), request.getApellido()));
    }
}
