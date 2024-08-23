import base64
import time
import rsa
from faker import Faker

fk = Faker(locale='zh_CN')


class DataGenerator:

    @staticmethod
    def generate_str_title():
        """生成字符串标题"""
        alpha = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
        return ''.join(random.choices(alpha, k=10)) + "_title"

    @staticmethod
    def generate_str_summary():
        """生成字符串摘要"""
        alpha = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
        return ''.join(random.choices(alpha, k=50)) + "_summary"

    @staticmethod
    def generate_str_body():
        """生成字符串内容"""
        alpha = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
        return ''.join(random.choices(alpha, k=100)) + "_body"

    @staticmethod
    def generate_time_int():
        """生成当前时间戳为int类型"""
        return int(time.time() * 1000)

    @staticmethod
    def generate_time_str():
        """生成当前时间戳为str类型"""
        return str(int(time.time() * 1000))

    @staticmethod
    def generate_mobile_int():
        """随机生成手机号为int类型"""
        return int(fk.phone_number())

    @staticmethod
    def generate_mobile_str():
        """随机生成手机号为str类型"""
        return fk.phone_number()

    @staticmethod
    def generate_chn_name():
        """随机生成中文名字"""
        return fk.name()

    @staticmethod
    def generate_idcard():
        """随机生成一个身份证号"""
        return fk.ssn()

    @staticmethod
    def generate_addr():
        """随机生成一个地址"""
        return fk.address()

    @staticmethod
    def generate_city():
        """随机生成一个城市名"""
        return fk.city()

    @staticmethod
    def generate_company():
        """随机生成一个公司名"""
        return fk.company()

    @staticmethod
    def generate_postcode():
        """随机生成一个邮编"""
        return fk.postcode()

    @staticmethod
    def generate_email():
        """随机生成一个邮箱号"""
        return fk.email()

    @staticmethod
    def generate_date():
        """随机生成一个日期"""
        return fk.date()

    @staticmethod
    def generate_date_time():
        """随机生成一个时间"""
        return fk.date_time()

    @staticmethod
    def generate_ipv4():
        """随机生成一个ipv4的地址"""
        return fk.ipv4()

    @staticmethod
    def base64_encode(data: str):
        """base64编码"""
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')

    @staticmethod
    def md5_encrypt(data: str):
        """md5加密"""
        from hashlib import md5
        new_md5 = md5()
        new_md5.update(data.encode('utf-8'))
        return new_md5.hexdigest()

    @staticmethod
    def rsa_encrypt(msg, server_pub):
        """
        rsa加密
        :param msg: 待加密文本
        :param server_pub: 密钥
        :return:
        """
        msg = msg.encode('utf-8')
        pub_key = server_pub.encode("utf-8")
        public_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)  #
        cryto_msg = rsa.encrypt(msg, public_key_obj)  # 生成加密文本
        cipher_base64 = base64.b64encode(cryto_msg)  # 将加密文本转化为 base64 编码
        return cipher_base64.decode()


import random


def generate_random_alpha(length):
    alpha = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
    return ''.join(random.choices(alpha, k=length)) + "_title"


# 生成一个长度为5的随机字符串
print(generate_random_alpha(10))
print(type(generate_random_alpha(10)))