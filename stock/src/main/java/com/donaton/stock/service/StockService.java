package com.donaton.stock.service;

import com.donaton.stock.model.Stock;
import com.donaton.stock.repository.StockRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StockService {

    @Autowired
    private StockRepository stockRepository;

    public List<Stock> listarTodos() {
        return stockRepository.findAll();
    }

    public Stock buscarPorId(Long id) {
        return stockRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Stock no encontrado con id: " + id));
    }

    public Stock guardar(Stock stock) {
        return stockRepository.save(stock);
    }

    public Stock actualizar(Long id, Stock datosNuevos) {
        Stock stock = buscarPorId(id);
        stock.setNombre(datosNuevos.getNombre());
        stock.setCategoria(datosNuevos.getCategoria());
        stock.setCantidadDisponible(datosNuevos.getCantidadDisponible());
        stock.setEstado(datosNuevos.getEstado());
        stock.setUbicacionBodega(datosNuevos.getUbicacionBodega());
        return stockRepository.save(stock);
    }

    public void eliminar(Long id) {
        stockRepository.deleteById(id);
    }
}