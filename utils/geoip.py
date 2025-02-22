from pathlib import Path

import geoip2.database
from loguru import logger


class GeoIPService:
    def __init__(self):
        """
        初始化 GeoIPService，加载所有可用的数据库。
        """
        # 兼容 Windows 和 Linux 文件系统
        self.db_paths = {
            "city": Path("resources/geoip/GeoLite2-City/GeoLite2-City.mmdb"),
            "country": Path("resources/geoip/GeoLite2-Country/GeoLite2-Country.mmdb"),
            "asn": Path("resources/geoip/GeoLite2-ASN/GeoLite2-ASN.mmdb"),
            "isp": Path("resources/geoip/GeoIP2-ISP/GeoIP2-ISP.mmdb")
        }

        self.readers = {}
        for key, path in self.db_paths.items():
            if path.exists():   # os.path.exists(path)
                self.readers[key] = geoip2.database.Reader(str(path))
            else:
                logger.warning(f"Warning: {key} database not found at {path}")

    def get_location(self, ip):
        """ 获取 IP 地址的地理位置信息（国家、城市、区域）"""
        if "city" not in self.readers:
            return None
        try:
            response = self.readers["city"].city(ip)
            return {
                "country": response.country.name,
                "state": response.subdivisions.most_specific.name,
                "city": response.city.name,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
            }
        except geoip2.errors.AddressNotFoundError:
            return {}

    def get_country(self, ip):
        """ 获取 IP 地址的国家信息 """
        if "country" not in self.readers:
            return None
        try:
            response = self.readers["country"].country(ip)
            return {"country": response.country.name}
        except geoip2.errors.AddressNotFoundError:
            return {}

    def get_isp(self, ip):
        """ 获取 IP 地址的 ISP 信息 """
        if "isp" not in self.readers:
            return None
        try:
            response = self.readers["isp"].isp(ip)
            return {"isp": response.isp}
        except geoip2.errors.AddressNotFoundError:
            return {}

    def get_asn(self, ip):
        """ 获取 IP 地址的 ASN 信息 """
        if "asn" not in self.readers:
            return None
        try:
            response = self.readers["asn"].asn(ip)
            return {
                "asn": response.autonomous_system_number,
                "asn_org": response.autonomous_system_organization,
            }
        except geoip2.errors.AddressNotFoundError:
            return {}

    def close(self):
        """ 关闭所有数据库连接 """
        for reader in self.readers.values():
            reader.close()


geoip_service = GeoIPService()
