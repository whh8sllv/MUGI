def left_shift(bits, n):
    return ((bits << n) | (bits >> (64 - n))) & (2**64 - 1)

def right_shift(bits, n):
    return ((bits >> n) | (bits << (64 - n))) & (2**64 - 1)

def init(key, IV):
    D0 = 0x6a09e667f3bcc908
    key_0 = '0x' + key[:16]
    key_1 = '0x' + key[16:]    
    a_49 = []
    b_16 = []
    a_49.append(int(key_0, 16))
    a_49.append(int(key_1, 16))
    key_00 = int(key_0, 16)
    key_11 = int(key_1, 16)
    a_49_2 = (left_shift(key_00, 7)) ^ (right_shift(key_11, 7)) ^ D0
    a_49.append(a_49_2)
    a_48 = function_rho1(a_49, 0, 0)
    b_16.append(hex(a_48[0]))
    temp = a_48
    counter = 47
    for i in range(15):
        a_new = function_rho1(temp, 0, 0)
        counter -= 1
        temp = a_new
        b_16.append(hex(a_new[0]))
    a_33 = a_new
    print([hex(i) for i in a_33])
    b_16 =  b_16[::-1]
    print(b_16)








def function_rho1(a_i, w1, w2):
    D1 = 0xbb67ae8584caa73b
    D2 = 0x3c6ef372fe94f82b
    # a_i - array
    a_0_new = a_i[1]
    a_1_new = a_i[2] ^ function_F(a_i[1], w1) ^ D1
    a_2_new = a_i[0] ^ function_F(a_i[1], left_shift(w2, 17)) ^ D2
    return [a_0_new, a_1_new, a_2_new]


def function_F(x, t):
    # в каком формате x и t под вопросом
    x_new = hex(x ^ t)[2:]
    if len(x_new) < 16:
        dif = 16 - len(x_new)
        x_new = '0' * dif + x_new
    
    # допустим x_new - это строка
    x_i = []
    for i in range(1, len(x_new), 2):
        x_i.append(x_new[i-1] + x_new[i])
    p_i = [function_S_R(i)[2:] for i in x_i]
    
    q_l = function_M(p_i[0], p_i[1], p_i[2], p_i[3])
    q_r = function_M(p_i[4], p_i[5], p_i[6], p_i[7])
    return int(('0x' + q_r[0] + q_r[1] + q_l[2] + q_l[3] + q_l[0] + q_l[1] + q_r[2] + q_r[3]), 16)






def function_S_R(x):
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


def function_M(x0, x1, x2, x3):
    m = 8
    f_x = [int(i) for i in '100011011']
    const1 = [int(i) for i in make_polynomials(bin(1)[2:])]
    const2 = [int(i) for i in make_polynomials(bin(2)[2:])]
    const3 = [int(i) for i in make_polynomials(bin(3)[2:])]
    x0 = [int(i) for i in make_polynomials(bin(int('0x' + x0, 16))[2:])]
    x1 = [int(i) for i in make_polynomials(bin(int('0x' + x1, 16))[2:])]
    x2 = [int(i) for i in make_polynomials(bin(int('0x' + x2, 16))[2:])]
    x3 = [int(i) for i in make_polynomials(bin(int('0x' + x3, 16))[2:])]
    y0 = hex(polynomials_multiply(const2, x0, f_x) ^ polynomials_multiply(const3, x1, f_x) ^ polynomials_multiply(const1, x2, f_x) ^ polynomials_multiply(const1, x3, f_x))[2:]
    y1 = hex(polynomials_multiply(const1, x0, f_x) ^ polynomials_multiply(const2, x1, f_x) ^ polynomials_multiply(const3, x2, f_x) ^ polynomials_multiply(const1, x3, f_x))[2:]
    y2 = hex(polynomials_multiply(const1, x0, f_x) ^ polynomials_multiply(const1, x1, f_x) ^ polynomials_multiply(const2, x2, f_x) ^ polynomials_multiply(const3, x3, f_x))[2:]
    y3 = hex(polynomials_multiply(const3, x0, f_x) ^ polynomials_multiply(const1, x1, f_x) ^ polynomials_multiply(const1, x2, f_x) ^ polynomials_multiply(const2, x3, f_x))[2:]
    sup = [y0, y1, y2, y3]
    res = []
    for y_i in sup:
        if len(y_i) < 2:
            res.append('0' + y_i)
        else:
            res.append(y_i)
    print            
    return res

def make_polynomials(num):
    while len(num) < 8:
        num = '0' + num
    return num


def polynomials_module(a, p_x):
    if len(a) < len(p_x):
        return a
    for i in range(len(p_x)):
        a[i] = (a[i] + p_x[i]) % 2
    while a and a[0] == 0:
        a.pop(0)
    return polynomials_module(a, p_x)

def polynomials_multiply(a, b, p_x):
    len_res = len(a) + len(b) - 1
    res = [0] * len_res
    for i in range(len(a)):
        if a[i] == 1:
            for j in range(len(b)):
                res[i+j] = (res[i+j] + b[j]) % 2
    return int(('0b' + ''.join(str(i) for i in polynomials_module(res, p_x))), 2)
    

key = '000102030405060708090a0b0c0d0e0f'
vector = 'f0e0d0c0b0a090807060504030201000'

print(init(key, vector))
