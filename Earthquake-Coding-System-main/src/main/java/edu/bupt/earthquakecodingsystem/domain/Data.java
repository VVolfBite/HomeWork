package edu.bupt.earthquakecodingsystem.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import java.time.LocalDateTime;
import java.util.Date;

@Entity
@Getter
@Setter
@ToString
@RequiredArgsConstructor
public class Data {
  @Id
  @GeneratedValue(strategy = GenerationType.AUTO)
  private int id;
  private String code;
  private String location;
  private int longitude;
  private int latitude;
  private String origin;
  private Date time;
  private String carrier;
  private String type;
  private String label;
  private String description;
}
