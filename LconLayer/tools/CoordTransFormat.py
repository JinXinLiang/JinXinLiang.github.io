# coding: utf-8


"""
    WGS-84(GPS)与GCJ-02(高德)坐标系互转
"""

import math
from abc import abstractmethod


class CoordClass(object):

    def __init__(self, **kwargs):
        self.x_pi = 3.14159265358979324 * 3000.0 / 180.0
        self.pi = 3.1415926535897932384626
        self.a = 6378245.0  # 长半轴
        self.ee = 0.00669342162296594323  # 扁率
        self.data = list()
        self.get_data(**kwargs)
        self.check_data()

    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass

    def check_data(self):
        if not self.data:
            raise Exception('请重写get_data方法并返回数据列表')
        if not isinstance(self.data, list):
            raise Exception('get_data方法请返回list格式数据')

    def wgs84_to_gcj02(self):
        result = []
        for i in self.data:
            result.append(self._wgs84_to_gcj02(i[0], i[1]))
        return result

    def _wgs84_to_gcj02(self, lng, lat):
        lng, lat = float(lng), float(lat)
        if self.out_of_china(lng, lat):  # 判断是否在国内
            return lng, lat
        dlat = self.transform_lat(lng - 105.0, lat - 35.0)
        dlng = self.transform_lng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [mglng, mglat]

    def gcj02_to_wgs84(self):
        result = []
        for i in self.data:
            result.append(self._gcj02_to_wgs84(i[0], i[1]))
        return result

    def _gcj02_to_wgs84(self, lng, lat):
        if self.out_of_china(lng, lat):
            return lng, lat
        dlat = self.transform_lat(lng - 105.0, lat - 35.0)
        dlng = self.transform_lng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [lng * 2 - mglng, lat * 2 - mglat]

    def transform_lat(self, lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
              0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * self.pi) + 40.0 *
                math.sin(lat / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * self.pi) + 320 *
                math.sin(lat * self.pi / 30.0)) * 2.0 / 3.0
        return ret

    def transform_lng(self, lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
              0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * self.pi) + 40.0 *
                math.sin(lng / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * self.pi) + 300.0 *
                math.sin(lng / 30.0 * self.pi)) * 2.0 / 3.0
        return ret

    @staticmethod
    def out_of_china(lng, lat):
        if lng < 72.004 or lng > 137.8347:
            return True
        if lat < 0.8293 or lat > 55.8271:
            return True
        return False


class Coord(CoordClass):

    def get_data(self, data):
        if isinstance(data, dict):
            self.data = list(data.values())
        elif isinstance(data, list):
            self.data = data


if __name__ == '__main__':

    a = Coord()
    print(a.wgs84_to_gcj02())
