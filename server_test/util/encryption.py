# encryption
# coding by Shinichiro Sonoda
# Oct. 30th 2020

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# key_load
def key_load(file_name):
    with open(file_name, 'br') as f:
        key = RSA.import_key(f.read())
        return key
 
# 暗号化
def cipher_text(message, public_key): 
    public_cipher = PKCS1_OAEP.new(public_key)
    ciphertext = public_cipher.encrypt(message.encode())
    return ciphertext

# 復号化
def decode_cipher(ciphertext, private_key): 
    private_cipher = PKCS1_OAEP.new(private_key)
    message = private_cipher.decrypt(ciphertext).decode("utf-8")
    return message

if __name__ == "__main__":
    # メッセージを暗号化
    message1 = "1054495" # instax SN
    print("平文1", message1)
    public_key1 = key_load("./pem/public1.pem")
    ciphertext1 = cipher_text(message1, public_key1)
    print("暗号文1", ciphertext1)

    #　ファイル保存
    path_w = './request/test.rq'
    with open(path_w, mode='wb') as f:
        f.write(ciphertext1)
        f.close()

    # ファイル開く
    with open(path_w, mode='rb') as f:
        ciphertext2 = f.read()
        f.close()
    
    print(ciphertext1 == ciphertext2)

    # メッセージを復号
    private_key1 = key_load("./pem/private1.pem")
    message1d = decode_cipher(ciphertext2, private_key1)
    print("復元文1", message1d)
