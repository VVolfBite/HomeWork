package edu.bupt.earthquakecodingsystem.repo;

import edu.bupt.earthquakecodingsystem.domain.Data;
import edu.bupt.earthquakecodingsystem.domain.LocationCode;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Date;
import java.util.List;

public interface DataRepo extends JpaRepository<Data, Long> {
  List<Data> findAll();
  int countByLocation(String location);
  int countByTimeBetween(Date from, Date to);
}
