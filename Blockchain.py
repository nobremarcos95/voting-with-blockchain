from Block import Block
from Vote import Vote
from datetime import datetime
from fastecdsa import keys, curve

class Blockchain:
    def __init__(self):
        genesisBlock = self.generateGenBlock()
        self.chain = [genesisBlock]
        self.pendingVotes = []
        self.difficulty = 1


    # Gera o bloco genesis
    def generateGenBlock(self):
        vote = Vote("Easter", "Egg", "007")
        genBlock = Block(vote)
        return genBlock


    # Pega o último bloco da blockchain
    def getLastBlock(self):
        return self.chain[-1]

    
    # Responsável por minerar os blocos pendentes
    # que ainda não foram adicionados à blockchain
    def minePendingVotes(self):
        for vote in self.pendingVotes:
            previousHash = self.getLastBlock().blockHash

            vote.hasVoted = True
            vote.voteHash = vote.calculateHash()

            block = Block(vote, previousHash)

            block.mineBlock(self.difficulty)
            
            self.chain.append(block)

            # A cada novo bloco minerado, a dificuldade é incrementada
            # RECOMENDÁVEL comentar a linha abaixo para facilitar a execução do código
            # self.difficulty += 1;

        # Reseta o array de votos pendentes de mineração
        self.pendingVotes = []


    # Verifica se a blockchain é válida. Se não, identifica os blocos corrompidos
    def verifyChain(self):
        errors = []

        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i - 1]

            if (currentBlock.blockHash != currentBlock.calculateHash()):
                index = i
                errors.append(index)

            elif (currentBlock.previous_hash != previousBlock.blockHash):
                index = i
                errors.append(index)

            elif (currentBlock.vote.voteHash != currentBlock.vote.calculateHash()):
                index = i
                errors.append(index)
        
        if (errors == []):
            return ("Blockchain válida!")
        else:
            return ("Warning! Bloco(s) número(s) {} inválido(s)".format(errors))


    # Adiciona ao array de votos pendentes de mineração
    def createVote(self, voter, voted_for, zoneSection, privateKey):
        if (voter == "" or voted_for == ""):
            return False        # Forneça todos os campos! Sua chave, em quem vota e suas Zona e Seção

       # Pega a chave pública associada à chave privada fornecida
        publicKey = keys.get_public_key(privateKey, curve.secp256k1)
       
        if (voter != publicKey.__str__()):
            return False        # Chave inválida

        for vote in self.pendingVotes:
            if (publicKey == vote.voter):
                return False    # Voto já adicionado (pendente)

        for block in self.chain:
            if (block.vote.voter.__str__() == publicKey.__str__()):
                return False    # Voto já realizado

        # Cria uma nova cédula de votação
        vote = Vote(publicKey, voted_for, zoneSection)

        # Assina a cédula
        vote.signVote(privateKey)

        # Verifica se a assinatura é válida
        if (not vote.verifyVote(privateKey)):
            return False   # Assinatura inválida. Voto não computado

        # Caso tudo ocorra com sucesso, adiciona ao array de votos pendentes de mineração
        self.pendingVotes.append(vote)
        return True


    # Retorna todos os votos válidos computados para um determinado candidato
    def getVotes(self, candidate):
        total = 0
        for block in self.chain:
            if (block.vote.voted_for == candidate):
                total += 1
        
        return total


    # Retorna todos os votos válidos realizados na votação
    def getTotalVotes(self):
        return (len(self.chain) - 1)