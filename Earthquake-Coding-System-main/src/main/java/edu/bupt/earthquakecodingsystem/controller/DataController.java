package edu.bupt.earthquakecodingsystem.controller;

import edu.bupt.earthquakecodingsystem.domain.Data;
import edu.bupt.earthquakecodingsystem.service.DataService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@RestController
@RequestMapping(value = "/api/data")
public class DataController {
  private final DataService service;
  @Autowired
  public DataController(DataService service) {
    this.service = service;
  }

  @PostMapping("/decode")
  void decode(@RequestParam String code) {
    service.decode(code);
  }

  @GetMapping("/get-all")
  List<Data> getAllData() {
    return service.getAllData();
  }

  @GetMapping("/count-by-place")
  Map<String, Integer> countEarthquake() {
    Map<String, Integer> map = new HashMap<>();
    map.put("新疆", 0);
    map.put("西藏", 0);
    map.put("台湾", 0);
    map.put("青海", 0);
    map.put("云南", 0);
    map.put("甘肃", 0);
    map.put("内蒙古", 0);
    map.put("吉林", 0);
    map.put("河北", 0);
    map.put("宁夏", 0);
    map.put("陕西", 0);
    map.put("山西", 0);
    map.put("四川", 0);
    map.put("重庆", 0);
    map.put("河南", 0);
    map.put("山东", 0);
    map.put("黑龙江", 0);
    map.put("辽宁", 0);
    map.put("湖北", 0);
    map.put("安徽", 0);
    map.put("湖南", 0);
    map.put("贵州", 0);
    map.put("广西", 0);
    map.put("广东", 0);
    map.put("江西", 0);
    map.put("江苏", 0);
    map.put("浙江", 0);
    map.put("福建", 0);
    map.put("澳门", 0);
    map.put("香港", 0);
    map.put("海南", 0);
    map.put("北京", 0);
    map.put("上海", 0);
    map.put("南海诸岛", 0);
    List<Data> list = getAllData();
    for (var data : list) {
      int count = map.get(data.getLocation());
      map.put(data.getLocation(), count + 1);
    }
    return map;
  }

  @GetMapping("/count-last-year")
  List<Integer> countLastYear() {
    return service.countLastYearByMonth();
  }
}
