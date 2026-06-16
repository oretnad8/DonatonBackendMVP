package com.donaton.stock.controller;

import com.donaton.stock.model.Stock;
import com.donaton.stock.service.StockService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/stock")
public class StockController {

    @Autowired
    private StockService stockService;

    @GetMapping
    public List<Stock> listarTodos() {
        return stockService.listarTodos();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Stock> buscarPorId(@PathVariable Long id) {
        return ResponseEntity.ok(stockService.buscarPorId(id));
    }

    @PostMapping
    public ResponseEntity<Stock> crear(@Valid @RequestBody Stock stock) {
        Stock guardado = stockService.guardar(stock);
        return ResponseEntity.ok(guardado);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Stock> actualizar(@PathVariable Long id, @Valid @RequestBody Stock stock) {
        return ResponseEntity.ok(stockService.actualizar(id, stock));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        stockService.eliminar(id);
        return ResponseEntity.noContent().build();
    }
}