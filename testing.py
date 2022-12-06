from Blockchain import Blockchain
from fastecdsa import keys, curve
from Vote import Vote

"""
ATENÇÃO:
Este arquivo é usado apenas para TESTES da blockchain (verificar se a chain é válida ou não)
Para rodar o sistema de votação, execute o arquivo main.py
"""

if __name__ == "__main__":
    # Forneça sua chave privada
    privateKey1 = 113558315420403508367311906460429656638361481150115281133521902836381902043031
    

    # Cria uma nova blockchain    
    coin = Blockchain()

    # Pega as chaves públicas associadas a cada chave privada
    voter1 = keys.get_public_key(privateKey1, curve.secp256k1).__str__()
    

    # Cada votante é identificado pela sua chave pública
    person1 = coin.createVote(voter1, 'Marta', '007009', privateKey1)


    # Descomente as linhas abaixo caso queira testar para mais de um voto por vez
    # privateKey2 = 44349737184028424801385249308431473038729504722135845776392277521241694533923
    # privateKey3 = 37599569584355171779365870629894873988606780142964722643044422774098580168702
    # voter2 = keys.get_public_key(privateKey2, curve.secp256k1).__str__()
    # voter3 = keys.get_public_key(privateKey3, curve.secp256k1).__str__()
    # person2 = coin.createVote(voter1, 'Maria', '007009', privateKey1)
    # person3 = coin.createVote(voter2, 'Maria', '007009', privateKey2)
    # person4 = coin.createVote(voter3, 'Maria', '007009', privateKey3)


    print("Votação iniciada...")
    coin.minePendingVotes()

    if (not person1):
        print ("Houve um erro 1. Voto não computado.")


    # Descomente as linhas abaixo caso queira testar para mais de um voto po vez
    # if (not person2):
    #     print ("Houve um erro 2. Voto não computado.")

    # if (not person3):
    #     print ("Houve um erro 3. Voto não computado.")
    
    # if (not person4):
    #     print ("Houve um erro 4. Voto não computado.")


    # Pega o total de votos de um candidato
    print("Votos da Marta:", coin.getVotes('Marta'))
    print("Total de votos envolvidos:", coin.getTotalVotes())

    print(coin.verifyChain())
    print("Testando adulteração de um bloco...")
    coin.chain[1].vote.voted_for = "Maria"
    print("Voto alterado de Marta para Maria")
    print(coin.verifyChain())