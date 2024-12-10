package edu.bupt.earthquakecodingsystem.repo;

import edu.bupt.earthquakecodingsystem.domain.LocationCode;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface LocationCodeRepo extends JpaRepository<LocationCode, Long> {
  LocationCode findByCode(String code);
}
