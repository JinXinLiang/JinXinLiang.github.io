import pandas as pd
import pymysql

from config import logger, host, port, user, password, db


class DataBaseHandle(object):
    # 初始化连接数据库
    def __init__(self):
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8')
        self.cur = self.conn.cursor()

    # 缺失值NaN,NaT替换为None 插入数据库之前的步骤
    @staticmethod
    def null_value_replace(data, data_type):
        df = data.reset_index(drop=True)
        row = df.shape[0]
        dit1 = {}
        try:
            for tup in data_type:
                dit1[tup[0]] = df[tup[2]].astype(tup[1]).mask(df[tup[2]].isnull(), None)
        except Exception as e:
            logger.error(e)
            raise Exception('')
        rows = []
        for i in range(row):
            oneRow = []
            for tup1 in data_type:
                oneRow.append(dit1[tup1[0]][i])
            rows.append(tuple(oneRow))
        return rows

    # rows数据插入数据库
    def insert_mysql_data(self, table_name, data, data_type, insert_type="replace"):
        col_names_list = []
        col_dataframe_list = []
        for type in data_type:
            col_names_list.append(type[0])
            col_dataframe_list.append(type[2])
        col_names_str = ",".join(col_names_list)
        col_str = ",".join(["%s" for i in col_names_list])
        insert_SQL = insert_type+" into "+table_name + " ( " + col_names_str + ") VALUES (" + col_str+");"
        data = data[col_dataframe_list]
        rows = self.null_value_replace(data, data_type)
        try:
            self.cur.executemany(insert_SQL, rows)
            self.conn.commit()  # 执行SQL语句后，使数据库更改生效
            logger.info(table_name + " 数据插入成功！")
        except Exception as e:
            logger.error('Reason: %s' % e)
            self.conn.rollback()  # 回滚，使执行出错的命令，不改变数据库
            logger.info(table_name + " 插入数据失败，执行了回滚")

    # 删除数据库数据
    def delete_mysql_data(self, delete_SQL):
        try:
            self.cur.execute(delete_SQL)  # 像sql语句传递参数
            self.conn.commit()
            logger.info(delete_SQL + " 数据删除成功！")
        except Exception as e:
            logger.error('Reason: %s' % e)
            self.conn.rollback()
            logger.info(delete_SQL+" 删除数据失败，执行了回滚")

    # 查询数据
    def select_mysql_data(self, select_sql):
        data = pd.read_sql(select_sql, self.conn)
        if data.empty:
            logger.error('%s 未获取到数据' % select_sql)
        return data


def main():
    pass


if __name__ == '__main__':
    main()
