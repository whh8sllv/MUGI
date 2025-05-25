import sys

class MUGI():

    def __init__(self, key, IV):
        self.key = key
        self.IV = IV
        self.D0 = 0x6a09e667f3bcc908
        self.D1 = 0xbb67ae8584caa73b
        self.D2 = 0x3c6ef372fe94f82b

    def initCipher(self):
        key_0 = int(('0x' + self.key[:16]), 16)
        key_1 = int(('0x' + self.key[16:]), 16)
        a_49_2 = (self.left_shift(key_0, 7)) ^ (self.right_shift(key_1, 7)) ^ self.D0
        a_49 = [key_0, key_1, a_49_2]
        b_16 = []
        temp = a_49
        for i in range(16):
            a_new = self.function_rho1(temp, 0, 0)
            temp = a_new
            b_16.append(a_new[0])
        a_33 = a_new
        b_16 =  b_16[::-1]
        IV_0 = int(('0x' + self.IV[:16]), 16)
        IV_1 = int(('0x' + self.IV[16:]), 16)
        a_32_0 = a_33[0] ^ IV_0
        a_32_1 = a_33[1] ^ IV_1
        a_32_2 = a_33[2] ^ (self.left_shift(IV_0, 7)) ^ (self.right_shift(IV_1, 7)) ^ self.D0
        a_32 = [a_32_0, a_32_1, a_32_2]
        temp = a_32
        for i in range(16):
            a_new = self.function_rho1(temp, 0, 0)
            temp = a_new
        a_16 = a_new
        temp_a, temp_b = a_16, b_16
        z_i = ''
        for i in range(16):
            a_new = self.next_and_stream(temp_a, temp_b)[0]
            b_new = self.next_and_stream(temp_a, temp_b)[1]
            z = self.next_and_stream(temp_a, temp_b)[2]
            temp_a, temp_b = a_new, b_new
        return temp_a, temp_b, z

    def next_and_stream(self, a, b):
        a_next = self.function_rho1(a, b[4], b[10])
        b_next = self.function_lambda1(b, a[0])
        z_i = hex(a_next[2])[2:]
        if len(z_i) < 16:
            dif = 16 - len(z_i)
            z_i = '0' * dif + z_i
        return a_next, b_next, z_i
    
    def make_keystream(self, a_0, b_0, z, text_length_byte):
        temp_a = a_0
        temp_b = b_0
        while len(bytes.fromhex(z)) < text_length_byte:
            a_new = self.next_and_stream(temp_a, temp_b)[0]
            b_new = self.next_and_stream(temp_a, temp_b)[1]
            z += self.next_and_stream(temp_a, temp_b)[2]
            temp_a, temp_b = a_new, b_new
        return z
    
    def function_lambda1(self, b, a_0):
        b_new = [0] * 16
        for j in range(16):
            if j == 0 or j == 4 or j == 10:
                continue
            b_new[j] = b[j-1]
        b_new[0] = b[15] ^ a_0
        b_new[4] = b[3] ^ b[7]
        b_new[10] = b[9] ^ self.left_shift(b[13], 32)
        return b_new
    
    def function_rho1(self, a_i, w1, w2):
        a_0_new = a_i[1]
        a_1_new = a_i[2] ^ self.function_F(a_i[1], w1) ^ self.D1
        a_2_new = a_i[0] ^ self.function_F(a_i[1], self.left_shift(w2, 17)) ^ self.D2
        return [a_0_new, a_1_new, a_2_new]
    
    def function_F(self, x, t):
        x_new = hex(x ^ t)[2:]
        if len(x_new) < 16:
            dif = 16 - len(x_new)
            x_new = '0' * dif + x_new
        x_i = []
        for i in range(1, len(x_new), 2):
            x_i.append(x_new[i-1] + x_new[i])
        p_i = [self.function_S_R(i)[2:] for i in x_i]
        q_l = self.function_M(p_i[0], p_i[1], p_i[2], p_i[3])
        q_r = self.function_M(p_i[4], p_i[5], p_i[6], p_i[7])
        return int(('0x' + q_r[0] + q_r[1] + q_l[2] + q_l[3] + q_l[0] + q_l[1] + q_r[2] + q_r[3]), 16)
    
    def function_S_R(self, x):
        x = int('0x' + x, 16)
        SUB = ['0x63', '0x7c', '0x77', '0x7b', '0xf2', '0x6b', '0x6f', '0xc5', '0x30', '0x01', '0x67', '0x2b', '0xfe', '0xd7', '0xab', '0x76', 
               '0xca', '0x82', '0xc9', '0x7d', '0xfa', '0x59', '0x47', '0xf0', '0xad', '0xd4', '0xa2', '0xaf', '0x9c', '0xa4', '0x72', '0xc0',
               '0xb7', '0xfd', '0x93', '0x26', '0x36', '0x3f', '0xf7', '0xcc', '0x34', '0xa5', '0xe5', '0xf1', '0x71', '0xd8', '0x31', '0x15',
               '0x04', '0xc7', '0x23', '0xc3', '0x18', '0x96', '0x05', '0x9a', '0x07', '0x12', '0x80', '0xe2', '0xeb', '0x27', '0xb2', '0x75',
               '0x09', '0x83', '0x2c', '0x1a', '0x1b', '0x6e', '0x5a', '0xa0', '0x52', '0x3b', '0xd6', '0xb3', '0x29', '0xe3', '0x2f', '0x84',
               '0x53', '0xd1', '0x00', '0xed', '0x20', '0xfc', '0xb1', '0x5b', '0x6a', '0xcb', '0xbe', '0x39', '0x4a', '0x4c', '0x58', '0xcf',
               '0xd0', '0xef', '0xaa', '0xfb', '0x43', '0x4d', '0x33', '0x85', '0x45', '0xf9', '0x02', '0x7f', '0x50', '0x3c', '0x9f', '0xa8',
               '0x51', '0xa3', '0x40', '0x8f', '0x92', '0x9d', '0x38', '0xf5', '0xbc', '0xb6', '0xda', '0x21', '0x10', '0xff', '0xf3', '0xd2',
               '0xcd', '0x0c', '0x13', '0xec', '0x5f', '0x97', '0x44', '0x17', '0xc4', '0xa7', '0x7e', '0x3d', '0x64', '0x5d', '0x19', '0x73',
               '0x60', '0x81', '0x4f', '0xdc', '0x22', '0x2a', '0x90', '0x88', '0x46', '0xee', '0xb8', '0x14', '0xde', '0x5e', '0x0b', '0xdb',
               '0xe0', '0x32', '0x3a', '0x0a', '0x49', '0x06', '0x24', '0x5c', '0xc2', '0xd3', '0xac', '0x62', '0x91', '0x95', '0xe4', '0x79',
               '0xe7', '0xc8', '0x37', '0x6d', '0x8d', '0xd5', '0x4e', '0xa9', '0x6c', '0x56', '0xf4', '0xea', '0x65', '0x7a', '0xae', '0x08',
               '0xba', '0x78', '0x25', '0x2e', '0x1c', '0xa6', '0xb4', '0xc6', '0xe8', '0xdd', '0x74', '0x1f', '0x4b', '0xbd', '0x8b', '0x8a',
               '0x70', '0x3e', '0xb5', '0x66', '0x48', '0x03', '0xf6', '0x0e', '0x61', '0x35', '0x57', '0xb9', '0x86', '0xc1', '0x1d', '0x9e',
               '0xe1', '0xf8', '0x98', '0x11', '0x69', '0xd9', '0x8e', '0x94', '0x9b', '0x1e', '0x87', '0xe9', '0xce', '0x55', '0x28', '0xdf',
               '0x8c', '0xa1', '0x89', '0x0d', '0xbf', '0xe6', '0x42', '0x68', '0x41', '0x99', '0x2d', '0x0f', '0xb0', '0x54', '0xbb', '0x16']
        return SUB[x]
    
    def function_M(self, x0, x1, x2, x3):
        m = 8
        f_x = self.get_int('100011011')
        const1 = self.get_int(self.make_polynomials(bin(1)[2:]))
        const2 = self.get_int(self.make_polynomials(bin(2)[2:]))
        const3 = self.get_int(self.make_polynomials(bin(3)[2:]))
        x0 = self.get_int(self.make_polynomials(bin(int('0x' + x0, 16))[2:]))
        x1 = self.get_int(self.make_polynomials(bin(int('0x' + x1, 16))[2:]))
        x2 = self.get_int(self.make_polynomials(bin(int('0x' + x2, 16))[2:]))
        x3 = self.get_int(self.make_polynomials(bin(int('0x' + x3, 16))[2:]))
        y0 = hex(self.polynomials_multiply(const2, x0, f_x) ^ self.polynomials_multiply(const3, x1, f_x) ^ self.polynomials_multiply(const1, x2, f_x) ^ self.polynomials_multiply(const1, x3, f_x))[2:]
        y1 = hex(self.polynomials_multiply(const1, x0, f_x) ^ self.polynomials_multiply(const2, x1, f_x) ^ self.polynomials_multiply(const3, x2, f_x) ^ self.polynomials_multiply(const1, x3, f_x))[2:]
        y2 = hex(self.polynomials_multiply(const1, x0, f_x) ^ self.polynomials_multiply(const1, x1, f_x) ^ self.polynomials_multiply(const2, x2, f_x) ^ self.polynomials_multiply(const3, x3, f_x))[2:]
        y3 = hex(self.polynomials_multiply(const3, x0, f_x) ^ self.polynomials_multiply(const1, x1, f_x) ^ self.polynomials_multiply(const1, x2, f_x) ^ self.polynomials_multiply(const2, x3, f_x))[2:]
        sup = [y0, y1, y2, y3]
        res = []
        for y_i in sup:
            if len(y_i) < 2:
                res.append('0' + y_i)
            else:
                res.append(y_i)          
        return res
    
    def get_int(self, string):
        return [int(i) for i in string]
    
    def make_polynomials(self, num):
        while len(num) < 8:
            num = '0' + num
        return num
    
    def polynomials_module(self, a, f_x):
        if len(a) < len(f_x):
            return a
        for i in range(len(f_x)):
            a[i] = (a[i] + f_x[i]) % 2
        while a and a[0] == 0:
            a.pop(0)
        return self.polynomials_module(a, f_x)
    
    def polynomials_multiply(self, a, b, f_x):
        len_res = len(a) + len(b) - 1
        res = [0] * len_res
        for i in range(len(a)):
            if a[i] == 1:
                for j in range(len(b)):
                    res[i+j] = (res[i+j] + b[j]) % 2
        module = ''.join(str(i) for i in self.polynomials_module(res, f_x))
        if module == '':
            module += '0'
        return int(('0b' + module), 2)

    def left_shift(self, bits, n):
        return ((bits << n) | (bits >> (64 - n))) & (2**64 - 1) 
    
    def right_shift(self, bits, n):
        return ((bits >> n) | (bits << (64 - n))) & (2**64 - 1)
    
    def encryptData(self, plaintext):
        byte_length = len(plaintext)
        s_0 = self.initCipher()
        z_res = self.make_keystream(s_0[0], s_0[1], s_0[2], byte_length)
        z = bytes.fromhex(z_res)
        ciphertext = ''
        for i in range(byte_length):
            xor = hex(plaintext[i] ^ z[i])[2:]
            if len(xor) < 2:
                xor = '0' + xor
            ciphertext += xor
        return ciphertext, z_res
    
    def decryptData(self, ciphertext):
        ciphertext_i = bytes.fromhex(ciphertext)
        byte_length = len(ciphertext_i)
        s_0 = self.initCipher()
        z_i = self.make_keystream(s_0[0], s_0[1], s_0[2], byte_length)
        z = bytes.fromhex(z_i)
        res = []
        for i in range(byte_length):
            res.append(z[i] ^ ciphertext_i[i])
        return bytes(res), z_i
    
def encodeFile(plaintext_file, ciphertext_file, key_IV_file, output_z=None):

    with open(plaintext_file, 'rb') as text_bytes:
        input_bytes = text_bytes.read()
    
    with open(key_IV_file, 'r', encoding='utf-8') as initizialization_parametres:
        parametres = initizialization_parametres.readlines()
    key = parametres[0].strip()
    IV = parametres[1].strip()     

    ciphertext, z = MUGI(key, IV).encryptData(input_bytes)

    with open(ciphertext_file, 'w') as encoded_result:
        encoded_result.write('---Your ciphertext---\n')
        encoded_result.write('\n')
        encoded_result.write(ciphertext)
    
    if output_z:
        with open(output_z, 'w') as keystream:
            keystream.write('---Keystream Z generated by MUGI---\n')
            keystream.write('\n')
            keystream.write(z)


def decodeFile(ciphertext_file, plaintext_file, key_IV_file, output_z=None):

    with open(ciphertext_file, 'r', encoding='utf-8') as cipher_text:
        input_cipher = cipher_text.read()

    with open(key_IV_file, 'r', encoding='utf-8') as initizialization_parametres:
        parametres = initizialization_parametres.readlines()
    key = parametres[0].strip()
    IV = parametres[1].strip()   

    plaintext, z = MUGI(key, IV).decryptData(input_cipher)

    with open(plaintext_file, 'wb') as decoded_result:
        decoded_result.write('---Your decrypted text---'.encode('utf-8') + b'\n')
        decoded_result.write(b'\n')
        decoded_result.write(plaintext)

    if output_z:
        with open(output_z, 'w') as keystream:
            keystream.write('---Keystream Z generated by MUGI---\n')
            keystream.write('\n')
            keystream.write(z)

def display_help_info():
    print('''
Вас вітає служба підтримки Вашої покірної програми-шифратора MUGI Utility :D
За допомогою MUGI Utility Ви можете зашифровувати/розшифровувати файли та <за бажанням> отримати послідовність псевдовипадкових чисел Z, яку генерує MUGI, щоб зашифрувати/розшифрувати файли.
Інструкція використання:

    - Зашифрувати файл:
            python main.py -encode <input_file> <output_file> <key_iv_file> [keystream_z_file]
    - Опис параметрів, які приймаються на вхід для шифрування:
     <input_file>      - ім'я файла, який необхідно зашифрувати
     <output_file>     - ім'я файла, в який треба записати шифрований текст
     <key_iv_file>     - ім'я файла, в якому зберігаються ключ шифрування (перший рядок) та вектор ініціалізації (другий рядок)
     [keystream_z_file] - (необов'язковий параметр) ім'я файла, в який буде збережно послідовність чисел Z     
          
    - Розшифрувати файл:
            python main.py -decode <input_file> <output_file> <key_iv_file> [keystream_z_file]
    - Опис параметрів, які приймаються на вхід для розшифрування:
     <input_file>      - ім'я файла, який необхідно розшифрувати
     <output_file>     - ім'я файла, в який треба записати розшифрований текст
     <key_iv_file>     - ім'я файла, в якому зберігаються ключ шифрування (перший рядок) та вектор ініціалізації (другий рядок)
     [keystream_z_file] - (необов'язковий параметр) ім'я файла, в який буде збережно послідовність чисел Z    
          
    - Вивести цю ж довідку:
           python main.py -help''')
          
def main():
    if len(sys.argv) < 2 and '-help' not in sys.argv:
        print('Щоб скористатись програмою-шифратором MUGI Utility введіть команди, вказані в інструкції :)\n')
        print('Інструкція: python main.py -encode <input_file> <output_file> <key_iv_file> [keystream_z_file]')
        print('            python main.py -decode <input_file> <output_file> <key_iv_file> [keystream_z_file]\n')
        print('            Якщо Ви хочете більш детально ознайомитись із командами MUGI Utility, введіть: python main.py -help')
    else:
        command = sys.argv[1]
        if command == '-help' and len(sys.argv) == 2:
            display_help_info()

        elif command == '-encode' and len(sys.argv) >= 5:
            input_file = sys.argv[2]
            output_file = sys.argv[3]
            key_file = sys.argv[4]
            output_z = sys.argv[5] if len(sys.argv) > 5 else None
            try:
                encodeFile(input_file, output_file, key_file, output_z)
                print()
                print(f"Ваш файл '{input_file}' було успішно зашифровано. Результат шифрування в файлі '{output_file}'")
                if output_z:
                    print(f"Побачити згенеровану послідовність Z ви можете у файлі '{output_z}'\n")
                print('Приходьте ще! <3')
            except: 
                print('Некоректно введена команда або назва файлів. Використовуйте: python main.py -encode <input_file> <output_file> <key_iv_file> [keystream_z_file]')
                print('                                                             python main.py -decode <input_file> <output_file> <key_iv_file> [keystream_z_file]')
                print('Або ж в разі будь-якого непорозуміння між Вами та цією шайтан-машиною, скористайтесь нашою цілобовою підтримкою ^^: python main.py -help')

        elif command == '-decode' and len(sys.argv) >= 5:
            input_file = sys.argv[2]
            output_file = sys.argv[3]
            key_file = sys.argv[4]
            output_z = sys.argv[5] if len(sys.argv) > 5 else None
            try:
                decodeFile(input_file, output_file, key_file, output_z)
                print()
                print(f"Ваш файл '{input_file}' було успішно розшифровано. Результат розшифрування в файлі '{output_file}'")
                if output_z:
                    print(f"Побачити згенеровану послідовність Z ви можете в файлі '{output_z}'")
                print('Приходьте ще! <3')
            except:
                print('Некоректно введена команда або назва файлів. Використовуйте: python main.py -encode <input_file> <output_file> <key_iv_file> [keystream_z_file]')
                print('                                                             python main.py -decode <input_file> <output_file> <key_iv_file> [keystream_z_file]')
                print('Або ж в разі будь-якого непорозуміння між Вами та цією шайтан-машиною, скористайтесь нашою цілобовою підтримкою ^^: python main.py -help')
            

        else:
            print('Некоректно введена команда. Використовуйте: python main.py -encode <input_file> <output_file> <key_iv_file> [keystream_z_file]')
            print('                                            python main.py -decode <input_file> <output_file> <key_iv_file> [keystream_z_file]')
            print('Або ж в разі будь-якого непорозуміння між Вами та цією шайтан-машиною, скористайтесь нашою цілобовою підтримкою ^^: python main.py -help')
        
    
if __name__ == '__main__':
    main()