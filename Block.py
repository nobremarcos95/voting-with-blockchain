import hashlib as hl
import json

class Block:
    def __init__(self, vote, previous_hash = "None"):
        self.nonce = 0
        self.previous_hash = previous_hash
        self.vote = vote
        self.blockHash = self.calculateHash()
    
    def __repr__(self):
        string = "{} {} {} {}".format(self.nonce, self.previous_hash, self.vote, self.blockHash)
        return string

    def calculateHash(self):
        # Converte o objeto Vote em uma string
        string = "{} {} {} {} {}".format(self.vote.voter, self.vote.voted_for, self.vote.zoneSection, self.vote.timestamp, self.vote.hasVoted)

        # Insere as informacoes num JSON
        block = json.dumps({
            "nonce": self.nonce,
            "previous_hash": self.previous_hash,
            "vote": string
        }, sort_keys = True).encode()
        
        # Aplica o hash no JSON
        blockHash = hl.sha256(block).hexdigest()
        return blockHash

    # Responsável por minerar um bloco
    def mineBlock(self, difficulty):
        # Proof of work
        # O hash deverá ser iniciado pela quantidade de zeros indicada por difficulty
        string = "0" * difficulty

        while(self.blockHash[:difficulty] != string):
            self.nonce += 1
            self.blockHash = self.calculateHash()
        
        print("+1 voto computado para: ", self.vote.voted_for)