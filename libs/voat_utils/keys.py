
from Crypto.PublicKey import RSA
from Crypto           import Random

def generate_key(bits):

    random_gen = Random.new().read

    key = RSA.generate(bits, random_gen)

    return key
