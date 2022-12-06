# from ecdsa import SigningKey as sKey, SECP256k1
from fastecdsa import keys, curve
from hashlib import sha256

def gerar_chave():
    # Cria um novo par de chaves (privada, pública)
    privateKey, publicKey = keys.gen_keypair(curve.secp256k1)
    return privateKey, publicKey

