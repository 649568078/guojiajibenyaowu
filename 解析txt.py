import pymysql
import re
import uuid

def insert_sql(conn,cursor,tablename, toinserts_values):
    keys = ", ".join(toinserts_values.keys())
    qmark = ", ".join(["%s"] * len(toinserts_values))
    sql_insert = "insert into %s (%s) values (%s)" % (tablename, keys, qmark)
    try:
        cursor.execute(sql_insert, list(toinserts_values.values()))
        conn.commit()
    except Exception as e:
        print(e)
        print(sql_insert)
        conn.rollback()
        print("插入失败")


def read_txt():
    conn = pymysql.connect(host="10.3.216.86", user="yangyusheng", password="yangysImi20,14:35", database="cde",
                           port=3396)
    if conn:
        print('数据库连接正常')

    # 使用cursor()方法创建一个游标对象
    cursor = conn.cursor()

    file_name = "40-46.txt"
    file = open(file_name, encoding='utf-8').read()
    # print(file)

    res_list = re.findall('\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*第\d*条(.*?品种名称[	]*[\u4e00-\u9fa5]*)',
                          file, re.DOTALL)
    print(len(res_list))
    for i in res_list:
        dict = {}
        contents1 = re.search('一级目录(.*)二级目录', i, re.DOTALL).group(1).replace('\n','').replace('\t','')
        contents2 = re.search('二级目录(.*)三级目录', i, re.DOTALL).group(1).replace('\n','').replace('\t','')
        contents3 = re.search('三级目录(.*)备注', i, re.DOTALL).group(1).replace('\n','').replace('\t','')
        remark = re.search('备注(.*)英文名', i, re.DOTALL).group(1).replace('\n','').replace('\t','')
        engname = re.search('英文名(.*)剂型、规格', i, re.DOTALL).group(1).replace('\n','').replace('\t','')
        form = re.search('剂型、规格(.*)品种名称', i, re.DOTALL).group(1).replace('\n\n',';').replace('\t','')
        Variety = re.search('品种名称(.*)', i, re.DOTALL).group(1).replace('\n','').replace('\t','')

        # print("一级目录:" + contents1)
        # print("二级目录:" + contents2)
        # print("三级目录:" + contents3)
        # print("备注:" + remark)
        # print("英文名:" + engname)
        # print("剂型、规格:" + form)
        # print("品种名称:" + Variety)
        dict["idCode"] = uuid.uuid4()
        dict["yijimulu"] = contents1
        dict["erjimulu"] = contents2
        dict["sanjimulu"] = contents3
        dict["memo"] = remark
        dict["nameen"] = engname
        dict["namecn"] = Variety
        dict["jixing"] = form
        print(form)
        print(dict)
        insert_sql(conn,cursor,'jibenyaowu2018_yang',dict)



if __name__ == '__main__':
    read_txt()
