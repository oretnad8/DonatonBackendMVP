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

    @GetMapping
    @PreAuthorize("hasRole('ADMIN_SENAPRED')")
    public ResponseEntity<java.util.List<UsuarioResponseDTO>> obtenerTodos() {
        return ResponseEntity.ok(usuarioService.obtenerTodos());
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN_SENAPRED')")
    public ResponseEntity<UsuarioResponseDTO> crearUsuario(@RequestBody UsuarioRequestDTO request) {
        return new ResponseEntity<>(usuarioService.crearUsuario(request), HttpStatus.CREATED);
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN_SENAPRED') or #id.toString() == authentication.principal")
    public ResponseEntity<UsuarioResponseDTO> obtenerUsuario(@PathVariable java.util.UUID id) {
        return ResponseEntity.ok(usuarioService.obtenerUsuario(id));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN_SENAPRED')")
    public ResponseEntity<UsuarioResponseDTO> actualizarUsuarioCompleto(@PathVariable java.util.UUID id, @RequestBody UsuarioRequestDTO request) {
        return ResponseEntity.ok(usuarioService.actualizarUsuarioCompleto(id, request));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN_SENAPRED')")
    public ResponseEntity<Void> eliminarUsuario(@PathVariable java.util.UUID id) {
        usuarioService.eliminarUsuario(id);
        return ResponseEntity.noContent().build();
    }
}
