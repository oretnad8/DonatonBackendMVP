package com.donaton.necesidades.service;

import com.donaton.necesidades.model.Necesidad;
import com.donaton.necesidades.repository.NecesidadRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NecesidadService {

    private final NecesidadRepository necesidadRepository = null;

    public List<Necesidad> listarTodas() {
        return necesidadRepository.findAll();
    }

    public Necesidad buscarPorId(Long id) {
        return necesidadRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Necesidad no encontrada con id: " + id));
    }

    public Necesidad guardar(Necesidad necesidad) {
        return necesidadRepository.save(necesidad);
    }

    public Necesidad actualizar(Long id, Necesidad datosNuevos) {
        Necesidad necesidad = buscarPorId(id);
        necesidad.setNombre(datosNuevos.getNombre());
        necesidad.setCategoria(datosNuevos.getCategoria());
        necesidad.setCantidadRequerida(datosNuevos.getCantidadRequerida());
        necesidad.setNivelPrioridad(datosNuevos.getNivelPrioridad());
        necesidad.setUbicacion(datosNuevos.getUbicacion());
        return necesidadRepository.save(necesidad);
    }

    public void eliminar(Long id) {
        necesidadRepository.deleteById(id);
    }
}