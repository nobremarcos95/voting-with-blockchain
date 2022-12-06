import hashlib as hl
from fastecdsa import ecdsa, keys, curve
from fastecdsa.encoding.der import DEREncoder
import json
from datetime import datetime

# voter == chave pública
class Vote:
    # Construtor
    def __init__(self, voter, voted_for, zoneSection):
        self.signature = ""                         # assinatura digital do voto
        self.voter = voter                          # quem votou
        self.voted_for = voted_for                  # quem recebeu o voto
        self.zoneSection = zoneSection              # zona e seção eleitorais onde o voto foi realizado
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.hasVoted = False
        self.voteHash = self.calculateHash()
    

    # Usado para printar um objeto Vote
    def __repr__(self):
        string = "Voter: {} Voted_for: {} ZoneSection: {} Timestamp: {} HasVoted: {} VoteHash: {}".format(self.voter.__str__(), self.voted_for, self.zoneSection, self.timestamp, self.hasVoted, self.voteHash)
        return string


    # Calcula o hash da cédula de votação
    def calculateHash(self):
        # Cria um JSON com os dados da cédula
        votingCell = json.dumps({
            "voter": self.voter.__str__(),
            "voted_for": self.voted_for,
            "zoneSection": self.zoneSection,
            "timestamp": self.timestamp,
            "hasVoted": self.hasVoted
        }, sort_keys = True).encode()

        #Aplica o hash no JSON
        voteHash = hl.sha256(votingCell).hexdigest()
        return voteHash


    # Realiza a assinatura digital do voto
    def signVote(self, privateKey):
        # Assina a cédula
        r,s = ecdsa.sign(self.voteHash, privateKey, curve = curve.secp256k1, hashfunc = hl.sha256)

        # Transforma a assinatura para DER
        self.signature = DEREncoder.encode_signature(r, s)


    # Verifica se a assinatura do voto é válida
    def verifyVote(self, privateKey):
        if (self.signature == "" or len(self.signature) == 0):
            return False

        r,s = ecdsa.sign(self.voteHash, privateKey, curve = curve.secp256k1, hashfunc = hl.sha256)
        decoded_r, decoded_s = DEREncoder.decode_signature(self.signature)

        # Se os parâmetros são diferentes, a assinatura é inválida
        if (r != decoded_r or s != decoded_s):
            return False

        # Verifica a assinatura
        valid = ecdsa.verify((r, s), self.voteHash, self.voter, curve = curve.secp256k1, hashfunc = hl.sha256)

        if (not valid):
            return False
        
        return True
        
