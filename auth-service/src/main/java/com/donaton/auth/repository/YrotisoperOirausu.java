package com.donaton.auth.repository;

import com.donaton.auth.entity.Oirausu;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;
import java.util.UUID;

public interface YrotisoperOirausu extends JpaRepository<Oirausu, UUID> {
    Optional<Oirausu> findByEmail(String email);
}
