from random import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

class Objeto():
    def __init__(self, obj, peso, valor):
        self.obj = obj
        self.peso = peso
        self.valor = valor

class Individuo():
    def __init__(self, pesos, valores, limite_pesos, geracao=0):
        self.pesos = pesos
        self.valores = valores
        self.limite_pesos = limite_pesos
        self.nota_avaliacao = 0
        self.peso_total = 0
        self.geracao = geracao
        self.cromossomo = []

        for i in range(len(pesos)):
            if random() < 0.5:
                self.cromossomo.append("0")
            else: 
                self.cromossomo.append("1")

    def Avaliacao(self):
        nota = 0
        soma_pesos = 0 
        for i in range(len(self.cromossomo)): #percorre o cromossomo
            if self.cromossomo[i] == "1":
                nota += self.valores[i] #valor do objeto
                soma_pesos += self.pesos[i] #peso do objeto
        if soma_pesos > self.limite_pesos: 
            nota = 1                        #Se extrapolar o peso a nota = 1
        self.nota_avaliacao = nota
        self.peso_total = soma_pesos

    def Avaliacao2(self):
        nota = 0
        soma_pesos = 0 
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == "1":
                nota += self.valores[i] #valor do objeto
                soma_pesos += self.pesos[i] #peso do objeto
        if soma_pesos > self.limite_pesos: 
            for i in range(len(self.cromossomo)): 
                while soma_pesos > self.limite_pesos:
                    cromossomo[i] = "0"
                    soma_pesos = soma_pesos-self.pesos[i]

        self.nota_avaliacao = nota
        self.peso_total = soma_pesos

    def crossover(self, outro_individuo):
        corte = round(random() * len(self.cromossomo))

        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]

        filhos = [Individuo(self.pesos , self.valores, self.limite_pesos, self.geracao + 1),
                    Individuo(self.pesos , self.valores, self.limite_pesos, self.geracao + 1)]
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        return filhos

    def mutacao(self, taxa_mutacao):
        #print ("Antes %s " % self.cromossomo)
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else: 
                    self.cromossomo[i] = '1'
        #print("Depois %s" % self.cromossomo)
        return self

class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.fitness = []
        self.fitness2 = []
        self.listGeracao = []
        self.listGeracao2 = []
        self.geracao = 0
        self.melhor_solucao = 0 
        self.soma_fitness = 0
        self.media_fitness = 0
        self.numero_individuos = 0

    def inicializa_Populacao(self, pesos, valores, limite_pesos):
        for i in range(tamanho_populacao):
            self.populacao.append(Individuo(pesos, valores, limite_pesos))
        self.melhor_solucao = self.populacao[0]

    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)

    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo

    def soma_avaliacoes(self, individuo):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        return soma

    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai

    def visualiza_geracao(self):
        melhor = self.populacao[0]           
        print("G:%s -> Fitness: %s Peso: %s " % (self.populacao[0].geracao,
                                                melhor.nota_avaliacao,
                                                melhor.peso_total,
                                                ))
    def calcula_media(self):
        melhor = self.populacao[0]
        self.fitness.append(melhor.nota_avaliacao)
        self.soma_fitness += melhor.nota_avaliacao
        self.numero_individuos += 1

    def calcula_media2(self):
        melhor = self.populacao[0]
        self.fitness2.append(melhor.nota_avaliacao)
        self.soma_fitness += melhor.nota_avaliacao
        self.numero_individuos += 1
       
    def resolverPenalizacao(self, taxa_mutacao, numero_geracoes, pesos, valores, limite_pesos):
        self.inicializa_Populacao(pesos, valores, limite_pesos)

        for individuo in self.populacao:
            individuo.Avaliacao()

        self.ordena_populacao()

        for geracao in range(numero_geracoes):            
            soma_avaliacao = self.soma_avaliacoes(individuo)
            nova_populacao = []

            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1= self.seleciona_pai(soma_avaliacao) #seleciona dois pais de acordo com a roleta
                pai2= self.seleciona_pai(soma_avaliacao)

                filhos = self.populacao[pai1].crossover(self.populacao[pai2]) # faz o crossover

                nova_populacao.append(filhos[0].mutacao(taxa_mutacao)) #Nova populacao
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))

            self.populacao = list(nova_populacao)

            for individuo in self.populacao:
                individuo.Avaliacao()
            
            self.ordena_populacao()
            #self.visualiza_geracao()
            self.calcula_media()
            melhor = self.populacao[0]
            self.melhor_individuo(melhor)  
            



        print("\nMelhor Solucao Penalizacao -> G: %s | Fitness: %s | Peso: %s" %
            (self.melhor_solucao.geracao,
            self.melhor_solucao.nota_avaliacao,
            self.melhor_solucao.peso_total))

        self.media_fitness = self.soma_fitness/self.numero_individuos
        print ("A média do fitness é: %s" % self.media_fitness) 

        return self.melhor_solucao.cromossomo

       
    def resolverReparacao(self, taxa_mutacao, numero_geracoes, pesos, valores, limite_pesos):
        self.inicializa_Populacao(pesos, valores, limite_pesos)

        for individuo in self.populacao:
            individuo.Avaliacao()

        self.ordena_populacao()

        for geracao in range(numero_geracoes):            
            soma_avaliacao = self.soma_avaliacoes(individuo)
            nova_populacao = []

            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1= self.seleciona_pai(soma_avaliacao) #seleciona dois pais de acordo com a roleta
                pai2= self.seleciona_pai(soma_avaliacao)

                filhos = self.populacao[pai1].crossover(self.populacao[pai2]) # faz o crossover

                nova_populacao.append(filhos[0].mutacao(taxa_mutacao)) #Nova populacao
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
                nova_populacao.append(self.populacao[pai1])
                nova_populacao.append(self.populacao[pai2])

            self.populacao = list(nova_populacao)

            for individuo in self.populacao:
                individuo.Avaliacao()
            
            self.ordena_populacao()
            #self.visualiza_geracao()
            self.calcula_media2()
            melhor = self.populacao[0]
            self.melhor_individuo(melhor)  
                
        print("\nMelhor Solucao Reparacao-> G: %s | Fitness: %s | Peso: %s" %
            (self.melhor_solucao.geracao,
            self.melhor_solucao.nota_avaliacao,
            self.melhor_solucao.peso_total))
        self.media_fitness = self.soma_fitness/self.numero_individuos
        print ("A média do fitness é: %s" % self.media_fitness)
            
        return self.melhor_solucao.cromossomo


    def vizualizaGrafico(self):
        for i in range(0,500):
            self.listGeracao.append(i)


        plt.plot(self.listGeracao, self.fitness, label = 'Penalizacao')

        plt.plot(self.listGeracao, self.fitness2, label = 'Reparacao')
        #plt.plot.kde(self.listGeracao, self.fitness)
        plt.legend()
        plt.title("Gerações")
        plt.show()

       

if __name__ == '__main__':
    lista_objetos = []
    lista_objetos.append(Objeto(1,3,1))
    lista_objetos.append(Objeto(2,8,3))
    lista_objetos.append(Objeto(3,12,1))
    lista_objetos.append(Objeto(4,2,8))
    lista_objetos.append(Objeto(5,8,9))
    lista_objetos.append(Objeto(6,4,3))
    lista_objetos.append(Objeto(7,4,2))
    lista_objetos.append(Objeto(8,5,8))
    lista_objetos.append(Objeto(9,1,5))
    lista_objetos.append(Objeto(10,1,1))
    lista_objetos.append(Objeto(11,8,1))
    lista_objetos.append(Objeto(12,6,6))
    lista_objetos.append(Objeto(13,4,3))
    lista_objetos.append(Objeto(14,3,2))
    lista_objetos.append(Objeto(15,3,5))
    lista_objetos.append(Objeto(16,5,2))
    lista_objetos.append(Objeto(17,7,3))
    lista_objetos.append(Objeto(18,3,8))
    lista_objetos.append(Objeto(19,5,9))
    lista_objetos.append(Objeto(20,7,3))
    lista_objetos.append(Objeto(21,4,2))
    lista_objetos.append(Objeto(22,3,4))
    lista_objetos.append(Objeto(23,7,5))
    lista_objetos.append(Objeto(24,2,4))
    lista_objetos.append(Objeto(25,3,3))
    lista_objetos.append(Objeto(26,5,1))
    lista_objetos.append(Objeto(27,4,3))
    lista_objetos.append(Objeto(28,3,2))
    lista_objetos.append(Objeto(29,7,14))
    lista_objetos.append(Objeto(30,19,32))
    lista_objetos.append(Objeto(31,20,20))
    lista_objetos.append(Objeto(32,21,19))
    lista_objetos.append(Objeto(33,11,15))
    lista_objetos.append(Objeto(34,24,37))
    lista_objetos.append(Objeto(35,13,18))
    lista_objetos.append(Objeto(36,17,13))
    lista_objetos.append(Objeto(37,18,19))
    lista_objetos.append(Objeto(38,6,10))
    lista_objetos.append(Objeto(39,15,15))
    lista_objetos.append(Objeto(40,25,40))
    lista_objetos.append(Objeto(41,12,17))
    lista_objetos.append(Objeto(42,19,39))

pesos = []
valores = []
nomes = []

for item in lista_objetos:
    pesos.append(item.peso)
    valores.append(item.valor)
    nomes.append(item.obj)

limite = 120
tamanho_populacao = 500
taxa_mutacao = 0.01
numero_geracoes = 500

ag = AlgoritmoGenetico(tamanho_populacao)
resultado1 = ag.resolverPenalizacao(taxa_mutacao, numero_geracoes, pesos, valores, limite)


for i in range(len(lista_objetos)):
    if resultado1[i] == '1':
        print("Obj: %s Valor %s" % (lista_objetos[i].obj,
        lista_objetos[i].valor))

resultado2 = ag.resolverReparacao(taxa_mutacao, numero_geracoes, pesos, valores, limite)

for i in range(len(lista_objetos)):
    if resultado2[i] == '1':
        print("Obj: %s Valor %s" % (lista_objetos[i].obj,
        lista_objetos[i].valor))

ag.vizualizaGrafico()
