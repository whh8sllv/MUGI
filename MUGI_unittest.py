import unittest
import main

def make_256_bits_keystream(key, iv):
    MUGI_enc = main.MUGI(key, iv)
    s_0 = MUGI_enc.initCipher()
    z = s_0[2]
    temp_a, temp_b = s_0[0], s_0[1]
    for i in range(3):
        a_new = MUGI_enc.next_and_stream(temp_a, temp_b)[0]
        b_new = MUGI_enc.next_and_stream(temp_a, temp_b)[1]
        z_new = MUGI_enc.next_and_stream(temp_a, temp_b)[2]
        temp_a, temp_b = a_new, b_new
        z += z_new
    return z

class TestMUGI(unittest.TestCase):
    
    '''
    Testing case #1:
    key = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    IV = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    Z = c7 6e 14 e7 08 36 e6 b6 cb 0e 9c 5a 0b f0 3e 1e 0a cf 9a f4 9e be 6d 67 d5 72 6e 37 4b 13 97 ac
    '''

    def test_null_key_and_null_IV(self):
        self.assertEqual(make_256_bits_keystream('00000000000000000000000000000000', '00000000000000000000000000000000'), 'c76e14e70836e6b6cb0e9c5a0bf03e1e0acf9af49ebe6d67d5726e374b1397ac')

    '''
    Testing case #2:
    key = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    IV = 34 61 69 88 51 81 21 39 01 55 00 a5 3b 7e 59 87
    Z = 2a a1 c5 c7 20 73 b1 b3 a9 d1 0d c6 85 50 66 10 28 30 56 0d 9a 24 65 c9 9c 29 1c 13 81 4e 08 8d
    '''

    def test_null_key_and_default_IV(self):
        self.assertEqual(make_256_bits_keystream('00000000000000000000000000000000', '3461698851812139015500a53b7e5987'), '2aa1c5c72073b1b3a9d10dc6855066102830560d9a2465c99c291c13814e088d')

    '''
    Testing case #3:
    key = 51 34 00 b1 04 a0 59 91 30 ad 00 fc 48 d7 59 e0
    IV = 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    Z = bd df ad 5f 04 b8 86 25 c3 ad ac e1 56 d1 c1 99 36 ff a4 e9 a7 fd f7 5a aa b8 29 13 42 85 aa 4b
    '''

    def test_default_key_and_null_IV(self):
        self.assertEqual(make_256_bits_keystream('513400b104a0599130ad00fc48d759e0', '00000000000000000000000000000000'), 'bddfad5f04b88625c3adace156d1c19936ffa4e9a7fdf75aaab829134285aa4b')

    '''
    Testing case #4.1:
    key = 69 e7 06 ee 52 95 37 2c 75 13 01 47 30 23 79 93
    IV = 2a 00 45 c8 49 27 49 d5 3a 9b 16 4a 25 e4 49 15
    Z = e3 cc 67 a0 25 5b 0f 28 2d 9a 5b 1b bd f7 f2 df 84 eb 46 f6 07 d6 e6 dd 32 86 13 43 94 dd 95 fb
    '''

    def test_default_key_and_default_IV_case1(self):
        self.assertEqual(make_256_bits_keystream('69e706ee5295372c7513014730237993', '2a0045c8492749d53a9b164a25e44915'), 'e3cc67a0255b0f282d9a5b1bbdf7f2df84eb46f607d6e6dd3286134394dd95fb')

    '''
    Testing case #4.2:
    key = 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f
    IV = f0 e0 d0 c0 b0 a0 90 80 70 60 50 40 30 20 10 00
    Z = bc 62 43 06 14 b7 9b 71 71 a6 66 81 c3 55 42 de 7a ba 5b 4f b8 0e 82 d7 0b 96 98 28 90 b6 e1 43
    '''

    def test_default_key_and_default_IV_case2(self):
        self.assertEqual(make_256_bits_keystream('000102030405060708090a0b0c0d0e0f', 'f0e0d0c0b0a090807060504030201000'), 'bc62430614b79b7171a66681c35542de7aba5b4fb80e82d70b96982890b6e143')
    

if __name__ == '__main__':
    unittest.main()