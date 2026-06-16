package com.donaton.user.dto;

import com.donaton.user.entity.Rol;
import com.donaton.user.entity.Usuario;
import java.util.UUID;

public class UsuarioResponseDTO {
    private UUID id;
    private String rut;
    private String nombre;
    private String apellido;
    private String email;
    private Rol rol;
    private Boolean estado;

    public UsuarioResponseDTO(Usuario usuario) {
        this.id = usuario.getId();
        this.rut = usuario.getRut();
        this.nombre = usuario.getNombre();
        this.apellido = usuario.getApellido();
        this.email = usuario.getEmail();
        this.rol = usuario.getRol();
        this.estado = usuario.getEstado();
    }
    
    public UUID getId() { return id; }
    public String getRut() { return rut; }
    public String getNombre() { return nombre; }
    public String getApellido() { return apellido; }
    public String getEmail() { return email; }
    public Rol getRol() { return rol; }
    public Boolean getEstado() { return estado; }
}
