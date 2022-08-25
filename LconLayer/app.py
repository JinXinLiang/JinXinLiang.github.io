import pandas as pd
import datetime
from geojson import LineString, FeatureCollection, Feature,Point
from tools.CoordTransFormat import Coord
from tools.DataBaseHandle import DataBaseHandle
from tools.csv_to_json import csv_to_json, csv_to_strjson, csv_to_networkjson
from datetime import date,timedelta
import json
import csv
# yesterday = (date.today() + timedelta(days=-1)).strftime('%Y-%m-%d')
# today =date.today()
#
# yesterday = '2022-08-19'
# today = '2022-08-20'


class HotPointsShow(object):

    def __init__(self,start_time=None,end_time=None,days=None):
        self.db_handle = DataBaseHandle()
        self.days = datetime.timedelta(days=days) if days else days
        self.end_time = end_time if end_time else datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
        self.start_time = start_time if start_time else datetime.datetime.strptime(self.end_time,
                                                                                   '%Y-%m-%d %H:%M:%S') - self.days
        self.car_position_csv_path = 'tmp/car_position.csv'
        self.order_points_csv_path = 'tmp/order_points.csv'
        self.realmoney_csv_path = 'tmp/realmoney_points.csv'
        self.timeorder_csv_path = 'tmp/timeorder_point.csv'
        self.network_csv_path = 'tmp/network_data.csv'
        self.order_rz_csv_path = 'tmp/order_rz.csv'
        self.all_rz_od_csv_path = 'tmp/all_rz_od.csv'
        self.network_csv = 'assert/network.csv'
        self.network_json = 'assert/network.json'


    def get_network(self):
        sql = """
         SELECT net.name,net.lg,net.lt,IFNULL(car.ID4,0) ID4 ,IFNULL(car.ID6,0) ID6, IFNULL(car.`车辆平均电量`,0.00) electric from 
        (SELECT 网点名称 name,网点经度 lg ,网点纬度 lt ,CONCAT(网点经度,',',网点纬度) lgt FROM `network_detail` 
        WHERE `网点状态` = 1
        AND `网点名称` not like '%代步车%') net left
        JOIN 
        (SELECT `zz_allcar`.`当前网点`,
        count(CASE WHEN zz_allcar.`车系` like 'ID.4%' THEN 'ID4' END) AS 'ID4',
        count(CASE WHEN zz_allcar.`车系` like 'ID.6%' THEN 'ID6' END) AS 'ID6',
        ROUND(AVG(zz_allcar.`剩余油量(升)/电量`),2) AS 车辆平均电量
        from zz_allcar WHERE
        zz_allcar.`当前网点` not like '%自由取还%'
        AND
        zz_allcar.`当前网点` != ''
        AND
        zz_allcar.`当前网点` not like '%代步车%'
        GROUP BY zz_allcar.`当前网点`) car  ON
        car.`当前网点` = net.`name`
        """
        network_data = self.db_handle.select_mysql_data(sql)
        # print(network_data)
        network_data.to_csv(self.network_csv,index=False)
        self.csv_tojson(network_csv=self.network_csv,network_json=self.network_json)
        return network_data

    def get_reservation_points(self):
        sql = """
        select 取车经度 'lng', 取车纬度 'lat'
        from order_data
        where 下单时间 between '%s' and '%s'
        and 支付状态 <> 'CANCELLED'
        """ % (self.start_time, self.end_time)
        points = self.db_handle.select_mysql_data(sql)
        print(points)
        points = points.values.tolist()
        a = Coord(data=points)
        points = a.wgs84_to_gcj02()
        self.list_to_js(points, self.order_points_csv_path, 'tmp/order_points.js', 'orderData')
        return points

    # 生成日租下单取车地点
    def get_order_rz_points(self):
        sql = """
            SELECT net.网点经度 lng,net.网点纬度 lat FROM `order_rz` rz LEFT JOIN network_detail net on rz.取车网点 = net.`网点名称` 
            where 下单时间 between '%s' and '%s'  
            AND `取车网点` != '自由取还区'
            AND `订单状态` != 0
        """ % (self.start_time, self.end_time)
        points = self.db_handle.select_mysql_data(sql)
        print(points)
        points = points.values.tolist()
        a = Coord(data=points)
        points = a.wgs84_to_gcj02()
        self.list_to_js(points, self.order_rz_csv_path, 'tmp/order_rz.js', 'orderData')
        return points

    # 生成分时+日租取车经纬度
    def get_all_rz_od(self):
        points = self.get_reservation_points() + self.get_order_rz_points()
        self.list_to_js(points, self.all_rz_od_csv_path, 'tmp/all_rz_od.js', 'orderData')
        return

    def list_to_js(self, points, csv_path, output_path, data_name):
        js_df = pd.DataFrame(points, columns=['lng', 'lat'])
        js_df['value'] = 1
        js_df.to_csv(csv_path, index=False)
        csv_to_json(csv_path, output_path, data_name)


    def csv_tojson(self,network_csv,network_json):
        features = []
        with open(network_csv,newline='',encoding='utf-8') as csvfile:
            next(csvfile)
            reader = csv.reader(csvfile,delimiter=',')
            for name,lg,lt,ID4,ID6,electric in reader:
                stlg,endlt = map(float,(lg,lt))
                features.append(
                    Feature(
                        geometry = Point([stlg,endlt]),
                        properties = {
                            "name":name,
                            "ID4":ID4,
                            "ID6":ID6,
                            "electric":electric
                        }
                    )
                )
        collection = FeatureCollection(features)
        with open(network_json,'w',encoding='utf-8') as f:
            f.write(json.dumps(collection,sort_keys=False,indent=4,ensure_ascii=False))




if __name__ == '__main__':
    a = HotPointsShow(start_time='{} 00:00:00'.format(yesterday), end_time='{} 00:00:00'.format(today))
    a.get_network()
    a.get_reservation_points()#分时
    a.get_order_rz_points()#日租
    a.get_all_rz_od()#分时+日租


