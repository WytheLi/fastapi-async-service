from Crypto.Cipher import AES
import base64

from settings import settings


class AESEncryption(object):
    """AES对称加密 加密/解密工具类（使用 CBC 模式）"""
    def __init__(self, key: str, iv: str):
        """
        :param key: AES 密钥（16/24/32字节）
        :param iv: AES IV（16字节）
        """
        self.key = key.encode("utf-8")
        self.iv = iv.encode("utf-8")

    @staticmethod
    def pad(data: str) -> bytes:
        """填充数据到 16 的倍数"""
        padding_length = 16 - (len(data.encode()) % 16)
        return data.encode() + (chr(padding_length) * padding_length).encode()

    @staticmethod
    def unpad(data: bytes) -> bytes:
        """去除填充"""
        return data[:-ord(data[-1:])]

    def encrypt(self, data: str) -> str:
        """AES 加密"""
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted_bytes = cipher.encrypt(self.pad(data))
        return base64.b64encode(encrypted_bytes).decode("utf-8")

    def decrypt(self, encrypted_data: str) -> bytes:
        """AES 解密"""
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted_bytes = cipher.decrypt(base64.b64decode(encrypted_data))
        return self.unpad(decrypted_bytes)


aes_encryption = AESEncryption(key=settings.AES_IV, iv=settings.AES_IV)


if __name__ == '__main__':
    # 测试加密
    # 在 Postman 里发送请求时，不能直接使用 JSON 发送明文数据。你需要手动 AES 加密 请求体，然后发送加密后的数据。
    data = '{"username": "admin", "password": "123456"}'
    encrypted_data = aes_encryption.encrypt(data)
    print("加密后:", encrypted_data)

    # 测试解密
    decrypted_data = aes_encryption.decrypt(encrypted_data)
    print("解密后:", decrypted_data)
