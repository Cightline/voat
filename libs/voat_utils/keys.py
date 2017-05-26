
from Crypto.PublicKey import RSA
from Crypto           import Random


# http://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/#a_3
def generate_key(bits):

    random_gen = Random.new().read

    key = RSA.generate(bits, random_gen)

    return key



