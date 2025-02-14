import hashlib


class ShortCodeUtils:
    # 默认字符集，允许包含字母和数字
    DEFAULT_CHARS = ['F', 'L', 'G', 'W', '5', 'X', 'C', '3', '9', 'Z', 'M', '6', '7', 'Y',
                     'R', 'T', '2', 'H', 'S', '8', 'D', 'V', 'E', 'J', '4', 'K', 'Q', 'P',
                     'U', 'A', 'N', 'B']
    # 仅数字字符集
    NUMERIC_CHARS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # 默认字符集长度
    CHARS_LENGTH = len(DEFAULT_CHARS)
    # 默认邀请码长度
    CODE_LENGTH = 6
    # 盐值，用于混淆
    SLAT = 1234561
    # 素数
    PRIME = 31
    # 素数1，用于混淆
    PRIME1 = 3
    # 素数2，用于混淆
    PRIME2 = 11

    def __init__(self, use_letters=True, decode_able=True):
        # 根据是否使用字母来选择字符集
        self.CHARS = self.DEFAULT_CHARS if use_letters else self.NUMERIC_CHARS
        # 更新字符集长度
        self.CHARS_LENGTH = len(self.CHARS)
        # 邀请码长度
        self.CODE_LENGTH = 6
        # 是否可解码
        self.DECODE_ABLE = decode_able

    def gen(self, identifier, code_length=None):
        # 如果 identifier 是字符串，则将其转换为整数
        if isinstance(identifier, str):
            identifier = self.uuid_to_int(identifier)

        # 如果未指定 code_length，则使用默认长度
        if code_length is None:
            code_length = self.CODE_LENGTH

        # 混淆 identifier
        identifier = identifier * self.PRIME1 + self.SLAT
        b = [0] * code_length
        b[0] = identifier
        # 生成中间值数组 b
        for i in range(code_length - 1):
            b[i + 1] = b[i] // self.CHARS_LENGTH
            b[i] = (b[i] + i * b[0]) % self.CHARS_LENGTH
        b[code_length - 1] = (sum(b[:code_length - 1]) * self.PRIME1) % self.CHARS_LENGTH

        # 生成最终的 code_index_array
        code_index_array = [0] * code_length
        for i in range(code_length):
            code_index_array[i] = b[i * self.PRIME2 % code_length]

        # 将 code_index_array 转换为最终的邀请码字符串
        buffer = ''.join([self.CHARS[t] for t in code_index_array])
        return buffer

    def gen_with_uuid_and_user_id(self, uuid_str, user_id, table_count=1):
        # 更新字符集长度
        self.CHARS_LENGTH = len(self.CHARS)
        # 组合 uuid 和 user_id 生成唯一标识符
        combined_identifier = f"{uuid_str}-{user_id}"
        # 将组合标识符转换为整数
        identifier_hash = self.uuid_to_int(combined_identifier)
        
        # 计算字符集的总容量
        total_capacity = self.CHARS_LENGTH ** self.CODE_LENGTH

        # 字母数字组合的容量很大，先//2处理了
        # 纯数字必须扩容，如果分表，就必须更进一步扩容位数
        code_length = self.CODE_LENGTH

        # 确保 user_id 的值不大于邀请码位数的总容量
        while user_id >= total_capacity:
            code_length += 1
            total_capacity = self.CHARS_LENGTH ** code_length

        # 生成邀请码
        code = self.gen(identifier_hash, code_length)
        return code

    @staticmethod
    def uuid_to_int(uuid_str):
        # 将 UUID 字符串转换为整数
        return int(hashlib.sha256(uuid_str.encode()).hexdigest(), 16)

    def encode_gen(self, id):
        """
        生成邀请码，可以逆向恢复

        :param id: 唯一的id主键
        :return: code
        """
        id = (id * self.PRIME) + self.SLAT
        code = []

        while id > 0:
            code.append(self.CHARS[id % self.CHARS_LENGTH])
            id //= self.CHARS_LENGTH

        # 保证生成的代码长度在6到10之间
        while len(code) < 6:
            code.append(self.CHARS[0])
        code = code[:10]

        return ''.join(reversed(code))

    def decode(self, code):
        """
        将邀请码解密成原来的id

        :param code: 邀请码
        :return: id
        """
        id = 0

        for char in code:
            id = id * self.CHARS_LENGTH + self.find_index(char)

        id = (id - self.SLAT) // self.PRIME

        return id

    def find_index(self, c):
        """
        查找对应字符的index

        :param c: 字符
        :return: index
        """
        try:
            return self.CHARS.index(c)
        except ValueError:
            return -1


if __name__ == '__main__':
    # 不可逆的邀请码转换
    user_id = 123456
    user_uuid = '123e4567-e89b-12d3-a456-426614174000'
    invite_code_utils_numbers = ShortCodeUtils(use_letters=True)

    # 生成邀请码 (使用 user_id)
    code_with_numbers = invite_code_utils_numbers.gen(user_id)
    print(f"Generated Code with numbers for ID {user_id}: {code_with_numbers}")

    # 生成邀请码 (使用 user_uuid)
    code_with_numbers_uuid = invite_code_utils_numbers.gen(user_uuid)
    print(f"Generated Code with numbers for UUID {user_uuid}: {code_with_numbers_uuid}")

    # 生成邀请码 (使用 user_uuid 和 user_id)，支持分表
    code_with_uuid_and_user_id = invite_code_utils_numbers.gen_with_uuid_and_user_id(user_uuid, user_id, table_count=1)
    print(f"Generated Code with UUID {user_uuid} and user ID {user_id}: {code_with_uuid_and_user_id}")


    #可逆的邀请码转换
    # 生成邀请码
    user_id = 1234567891020
    code = invite_code_utils_numbers.encode_gen(user_id)
    print(f"Generated Code for ID {user_id}: {code}")

    # 解码邀请码
    decoded_id = invite_code_utils_numbers.decode(code)
    print(f"Decoded ID from Code {code}: {decoded_id}")

