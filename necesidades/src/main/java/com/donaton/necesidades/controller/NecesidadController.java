package com.donaton.necesidades.controller;

import com.donaton.necesidades.model.Necesidad;
import com.donaton.necesidades.service.NecesidadService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/necesidades")
public class NecesidadController {

    private final NecesidadService necesidadService;

    NecesidadController(NecesidadService necesidadService) {
        this.necesidadService = necesidadService;
    }

    @GetMapping
    public List<Necesidad> listarTodas() {
        return necesidadService.listarTodas();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Necesidad> buscarPorId(@PathVariable Long id) {
        return ResponseEntity.ok(necesidadService.buscarPorId(id));
    }

    @PostMapping
    public ResponseEntity<Necesidad> crear(@Valid @RequestBody Necesidad necesidad) {
        Necesidad guardada = necesidadService.guardar(necesidad);
        return ResponseEntity.ok(guardada);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Necesidad> actualizar(@PathVariable Long id, @Valid @RequestBody Necesidad necesidad) {
        return ResponseEntity.ok(necesidadService.actualizar(id, necesidad));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        necesidadService.eliminar(id);
        return ResponseEntity.noContent().build();
    }
}