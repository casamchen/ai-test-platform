import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from django.conf import settings

class Cipherd():
    def __init__(self) -> None:
        # 从环境变量或 Django settings 获取密钥，需与前端 VUE_APP_AES_KEY 保持一致
        env_key = os.environ.get('AES_ENCRYPTION_KEY', None)
        if env_key:
            self.key = env_key.encode('utf-8')
        else:
            # 默认密钥，与前端 main.js 中的默认值保持一致（必须完全相同）
            self.key = '1111111111111111'.encode('utf-8')
        # 固定 IV，与前端 VUE_APP_AES_IV 保持一致
        env_iv = os.environ.get('AES_ENCRYPTION_IV', None)
        if env_iv:
            self.iv = env_iv.encode('utf-8')
        else:
            self.iv = '1111111111111111'.encode('utf-8')

    def initialize_aes(self):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return cipher

    def encrypt(self, data):
        """加密数据，返回 base64 编码的密文"""
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        padder = pad(data.encode(), AES.block_size)
        encrypted_data = cipher.encrypt(padder)
        encryData = base64.b64encode(encrypted_data).decode('utf-8')
        return encryData

    def decrypt(self, data):
        """解密数据"""
        try:
            raw = base64.b64decode(data)
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            decrypted_data = unpad(cipher.decrypt(raw), AES.block_size).decode()
            return decrypted_data
        except Exception as e:
            raise ValueError(f"解密失败：{str(e)}")
