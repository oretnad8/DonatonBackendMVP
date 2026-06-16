package com.donaton.user.service;

import com.donaton.user.dto.UsuarioRequestDTO;
import com.donaton.user.dto.UsuarioResponseDTO;
import com.donaton.user.entity.Usuario;
import com.donaton.user.repository.UsuarioRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
@SuppressWarnings("null")
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;
    private final PasswordEncoder passwordEncoder;

    public UsuarioService(UsuarioRepository usuarioRepository, PasswordEncoder passwordEncoder) {
        this.usuarioRepository = usuarioRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public UsuarioResponseDTO crearUsuario(UsuarioRequestDTO request) {
        if (usuarioRepository.findByEmail(request.getEmail()).isPresent()) {
            throw new IllegalArgumentException("El email ya está registrado");
        }
        if (usuarioRepository.findByRut(request.getRut()).isPresent()) {
            throw new IllegalArgumentException("El RUT ya está registrado");
        }

        Usuario usuario = new Usuario();
        usuario.setRut(request.getRut());
        usuario.setNombre(request.getNombre());
        usuario.setApellido(request.getApellido());
        usuario.setEmail(request.getEmail());
        usuario.setPassword(passwordEncoder.encode(request.getPassword()));
        usuario.setRol(request.getRol());
        usuario.setEstado(true);

        return new UsuarioResponseDTO(usuarioRepository.save(usuario));
    }

    public UsuarioResponseDTO obtenerUsuario(UUID id) {
        Usuario usuario = usuarioRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Usuario no encontrado"));
        return new UsuarioResponseDTO(usuario);
    }

    public UsuarioResponseDTO actualizarContacto(UUID id, String email, String nombre, String apellido) {
        Usuario usuario = usuarioRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Usuario no encontrado"));
        
        if (email != null && !email.equals(usuario.getEmail()) && usuarioRepository.findByEmail(email).isPresent()) {
            throw new IllegalArgumentException("El email ya está en uso por otro usuario");
        }

        if (email != null) usuario.setEmail(email);
        if (nombre != null) usuario.setNombre(nombre);
        if (apellido != null) usuario.setApellido(apellido);

        return new UsuarioResponseDTO(usuarioRepository.save(usuario));
    }
}
