import os
from datetime import datetime
from loguru import logger

import duckdb


# 获取数据库文件的绝对路径
def get_db_path():
    # 获取当前文件所在目录的上一级目录
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 构造数据库文件的路径
    db_path = os.path.join(base_dir, 'storage', 'base.duckdb')
    return db_path


# 数据库连接函数
def get_db_connection():
    # 连接到 DuckDB 数据库
    connection = duckdb.connect(get_db_path())
    return connection


# 查询函数，直接使用三段格式
def get_cidr_info_with_isp(ip_address):
    try:
        connection = get_db_connection()

        # 使用固定的三段格式
        ip_parts = ip_address.split('.')
        pattern = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}."

        # 合并查询国家和 ISP 信息
        query = f'''
        SELECT 
            blocks.network, 
            loc.country_name, 
            loc.country_iso_code, 
            isp.isp
        FROM geolite2_country_blocks_ipv4 AS blocks
        JOIN geolite2_country_locations_en AS loc ON blocks.geoname_id = loc.geoname_id
        JOIN geoip2_isp_blocks_ipv4 AS isp ON blocks.network = isp.network
        WHERE blocks.network LIKE '{pattern}%'
        '''

        result = connection.execute(query).fetchone()
        connection.close()

        if result:
            data = {
                "network": result[0],
                "country_name": result[1],
                "country_iso_code": result[2],
                "isp": result[3]
            }
        else:
            data = {
                "network": "unknown",
                "country_name": "unknown",
                "country_iso_code": "unknown",
                "isp": "unknown"
            }
        logger.info(f"ip_address_info: {data}")
        return data
    except Exception as e:
        logger.info(f"Error occurred: {e}")
        return {
            "network": "unknown",
            "country_name": "unknown",
            "country_iso_code": "unknown",
            "isp": "unknown"
        }


# 从 CSV 文件读取数据并插入到 DuckDB
def import_csv_to_duckdb(csv_file_path, table_name, db_path):
    # 连接到 DuckDB 数据库
    connection = duckdb.connect(db_path)

    # 使用 DuckDB 的 COPY 命令从 CSV 文件加载数据
    connection.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM read_csv_auto('{csv_file_path}')
    """)

    # 关闭连接
    connection.close()


if __name__ == '__main__':
    # 示例 IP 地址
    a = datetime.now()
    client_ip = "45.67.200.10"

    # 获取 CIDR 信息
    cidr_info = get_cidr_info_with_isp(client_ip)
    print(cidr_info)

    print(datetime.now()-a)

    # csv_file_path = '/Users/jesse/Downloads/GeoLite2-Country-CSV_20241025/GeoIP2-ISP-Blocks-IPv6.csv'
    #
    # # 导入 CSV 数据到 DuckDB
    # import_csv_to_duckdb(csv_file_path, 'geoip2_isp_blocks_ipv6', get_db_path())
    #
    # # 打印成功消息
    # print("CSV 数据已成功导入到 DuckDB 数据库中。")
