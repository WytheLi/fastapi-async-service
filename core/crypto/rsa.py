from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


class RSAEncryption:
    def __init__(self, public_key_path: str = None, private_key_path: str = None):
        """初始化公钥和私钥"""
        if public_key_path:
            with open(public_key_path, "rb") as f:
                self.public_key = RSA.import_key(f.read())
        if private_key_path:
            with open(private_key_path, "rb") as f:
                self.private_key = RSA.import_key(f.read())

    def encrypt_with_public_key(self, data: str) -> str:
        """使用公钥加密数据"""
        cipher = PKCS1_OAEP.new(self.public_key)
        encrypted_data = cipher.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()

    def decrypt_with_private_key(self, encrypted_data: str) -> bytes:
        """使用私钥解密数据"""
        cipher = PKCS1_OAEP.new(self.private_key)
        decrypted_data = cipher.decrypt(base64.b64decode(encrypted_data))
        return decrypted_data

    def encrypt_with_private_key(self, data: str) -> str:
        """使用私钥加密数据"""
        cipher = PKCS1_OAEP.new(self.private_key)
        encrypted_data = cipher.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()

    def decrypt_with_public_key(self, encrypted_data: str) -> str:
        """使用公钥解密数据"""
        cipher = PKCS1_OAEP.new(self.public_key)
        decrypted_data = cipher.decrypt(base64.b64decode(encrypted_data))
        return decrypted_data.decode()


def generate_rsa_key():
    """
        生成 RSA 密钥对（公钥和私钥）
    :return:
    """
    key = RSA.generate(2048)
    private_key = key.export_key()
    with open("private.pem", "wb") as f:
        f.write(private_key)

    public_key = key.publickey().export_key()
    with open("public.pem", "wb") as f:
        f.write(public_key)
    print("公钥和私钥已生成")


rsa_encryption = RSAEncryption(private_key_path="private.pem")


if __name__ == '__main__':
    # generate_rsa_key()

    # 1. 客户端使用公钥加密数据
    rsa_encryption = RSAEncryption(public_key_path="public.pem")
    data = "This is a secret message"
    encrypted_data = rsa_encryption.encrypt_with_public_key(data)
    print(f"加密数据：{encrypted_data}")

    # 2. 服务器使用私钥解密数据
    rsa_encryption_private = RSAEncryption(private_key_path="private.pem")
    decrypted_data = rsa_encryption_private.decrypt_with_private_key(encrypted_data)
    print(f"解密数据：{decrypted_data}")
