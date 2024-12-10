package edu.bupt.earthquakecodingsystem.service;

import edu.bupt.earthquakecodingsystem.domain.Data;
import edu.bupt.earthquakecodingsystem.repo.DataRepo;
import edu.bupt.earthquakecodingsystem.repo.LocationCodeRepo;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.ZoneId;
import java.util.*;

@Slf4j
@Service
@RequiredArgsConstructor
public class DataService {
  private final LocationCodeRepo locationCodeRepo;
  private final DataRepo dataRepo;
  public void decode(String code) {

    Data data = new Data();
    data.setCode(code);

    data.setLocation(parseLocation(code.substring(0, 12)));

    Calendar calendar = Calendar.getInstance();
    calendar.set(Calendar.YEAR, Integer.parseInt(code.substring(12, 16)));
    calendar.set(Calendar.MONTH, Integer.parseInt(code.substring(16, 18)));
    calendar.set(Calendar.DAY_OF_MONTH, Integer.parseInt(code.substring(18, 20)));
    calendar.set(Calendar.HOUR_OF_DAY, Integer.parseInt(code.substring(20, 22)));
    calendar.set(Calendar.MINUTE, Integer.parseInt(code.substring(22, 24)));
    calendar.set(Calendar.SECOND, Integer.parseInt(code.substring(24, 26)));
    Date date = calendar.getTime();
    data.setTime(date);
    //业务数据来源大类代码
    HashMap<String,String>hashMap1=new HashMap<>();
    hashMap1.put("1","业务报送数据");
    hashMap1.put("2","泛在感知数据");
    hashMap1.put("3","其他");
    //业务数据来源子类代码
    HashMap<String,String>hashMap2=new HashMap<>();
    hashMap2.put("100","前方地震应急指挥部");
    hashMap2.put("101","后方地震应急指挥部");
    hashMap2.put("120","应急指挥技术系统");
    hashMap2.put("121","社会服务工程应急救援系统");
    hashMap2.put("140","危险区预评估工作组");
    hashMap2.put("141","地震应急技术协调组");
    hashMap2.put("142","震后政府信息支持工作项目组");
    hashMap2.put("180","灾情快速上报接收处理系统");
    hashMap2.put("181","地方地震局应急信息服务相关技术系统");
    hashMap2.put("199","其他");
    hashMap2.put("200","互联网感知");
    hashMap2.put("201","通信网感知");
    hashMap2.put("202","舆情网感知 ");
    hashMap2.put("203","电力系统感知");
    hashMap2.put("204","交通系统感知");
    hashMap2.put("205","其他");
    hashMap2.put("300","其他");
    data.setOrigin(hashMap1.get(code.substring(26,27)) + hashMap2.get(code.substring(26, 29)));
    //载体代码
    HashMap<String,String>hashMap3=new HashMap<>();
    hashMap3.put("0","文字");
    hashMap3.put("1","图像");
    hashMap3.put("2","音频");
    hashMap3.put("3","视频");
    hashMap3.put("4","其他");
    data.setCarrier(hashMap3.get(code.substring(29, 30)));
    //灾情大类代码
    String tmp = "";
    HashMap<String,String>hashMap4 = new HashMap<>();
    hashMap4.put("1","地震事件信息");
    hashMap4.put("2","人员伤亡及失踪信息");
    hashMap4.put("3","房屋破坏信息");
    hashMap4.put("4","生命线工程灾情信息");
    hashMap4.put("5","次生灾害信息");
    tmp = hashMap4.get(code.substring(30, 31)) + " ";
    //灾情子类代码
    HashMap<String,String>hashMap5 = new HashMap<>();
    hashMap5.put("101","震情信息");
    hashMap5.put("201","死亡");
    hashMap5.put("202","受伤");
    hashMap5.put("203","失踪");
    hashMap5.put("301","土木");
    hashMap5.put("302","砖木");
    hashMap5.put("303","砖混");
    hashMap5.put("304","框架");
    hashMap5.put("305","其他");
    hashMap5.put("401","交通");
    hashMap5.put("402","供水");
    hashMap5.put("403","输油");
    hashMap5.put("404","燃气");
    hashMap5.put("405","电力");
    hashMap5.put("406","通信");
    hashMap5.put("407","水利");
    hashMap5.put("501","崩塌");
    hashMap5.put("502","滑坡");
    hashMap5.put("503","泥石流");
    hashMap5.put("504","岩溶塌陷");
    hashMap5.put("505","地裂缝");
    hashMap5.put("506","地面沉降");
    hashMap5.put("507","其他");
    tmp = tmp + hashMap5.get(code.substring(30, 33));
    data.setType(tmp);
    //灾情指标代码
    HashMap<String,String>hashMap6=new HashMap<>();
    if (code.charAt(30) == '1') {
      hashMap6.put("001","地理位置");
      hashMap6.put("002","时间");
      hashMap6.put("003","震级");
      hashMap6.put("004","震源深度");
      hashMap6.put("005","烈度");
    }
    else if (code.charAt(30) == '2') {
      hashMap6.put("001", "受灾人数");
      hashMap6.put("002", "受灾程度");
    }
    else if (code.charAt(30) == '3') {
      hashMap6.put("001", "一般损坏面积");
      hashMap6.put("002", "严重损坏面积");
      hashMap6.put("003", "受灾程度");
    }
    else if (code.charAt(30) == '4') {
      hashMap6.put("001", "受灾设施数");
      hashMap6.put("002", "受灾范围");
      hashMap6.put("003", "受灾程度");
    }
    else if (code.charAt(30) == '5') {
      hashMap6.put("001", "灾害损失");
      hashMap6.put("002", "灾害范围");
      hashMap6.put("003", "灾害程度");
    }
    data.setLabel(hashMap6.get(code.substring(33, 36)));
    dataRepo.save(data);
  }

  private String parseLocation(String code) {
    String tmp1 = locationCodeRepo.findByCode(code.substring(0, 4).concat("00000000")).getLocation();
    String tmp2 = locationCodeRepo.findByCode(code.substring(0, 6).concat("000000")).getLocation();
    String tmp3 = locationCodeRepo.findByCode(code.substring(0, 9).concat("000")).getLocation();
    String tmp4 = locationCodeRepo.findByCode(code).getLocation();
    return tmp1 + " " + tmp2 + " " + tmp3 + " " + tmp4 + " ";
  }

  public List<Data> getAllData() {
    return dataRepo.findAll();
  }

  public List<Integer> countLastYearByMonth() {
    List<Integer> ret = new ArrayList<>();
    for (int i = 12; i >= 1; i--) {
      // First day of month
      Date first;
      Calendar calendar1 = Calendar.getInstance();
      calendar1.add(Calendar.MONTH, -i);
      calendar1.set(Calendar.DAY_OF_MONTH, 1);
      first = calendar1.getTime();
      // Last day of month
      Date last;
      Calendar calendar2 = Calendar.getInstance();
      calendar2.add(Calendar.MONTH, 1 - i);
      calendar2.set(Calendar.DAY_OF_MONTH, 0);
      last = calendar2.getTime();
      ret.add(dataRepo.countByTimeBetween(first, last));
    }
    return ret;
  }

}
