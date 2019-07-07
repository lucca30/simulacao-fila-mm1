import random
import math

#Definição da classe

class Eventos:
    # Construtor da classe
    def __init__(self, globais):
        #Gere o valor de todas as variáveis globais
        self.globais = globais

        #Estrutura auxiliar de dados, para o problema específico da M/M/1 essa estrutura armazena as chegadas pela ordem de chegada
        self.auxiliar = [] 

        #Lista de eventos que é composta por 3-uplas nas quais:
        # 1 - o primeiro elemento é o instante que o evento ocorre,
        # 2 - o segundo elemento é o evento, que em termos programáticos é um ponteiro para a função
        # 3 - o terceiro elemento são os dados complementares passados entre eventos, no caso estamos utilizando apenas para transmitir
        # os dados referentes a pessoa que sairá do sistema quando o evento termina_servico ocorrer
        self.lista_eventos = []


    # Método para generalizar o início de uma simulação, recebe um ponteiro para uma função que definirá os valores iniciais e logo após
    # começa as iterações sobre a lista de eventos
    def start(self, start_function, rounds):
        start_function(self.globais, self.auxiliar, self.lista_eventos)

        for i in range(rounds):
            # obtém o evento de menor instante na lista de eventos e o remove da lista
            self.lista_eventos.sort()
            evento_atual = self.lista_eventos.pop(0)
            
            novos_eventos = evento_atual[1](evento_atual[0], self.globais, self.auxiliar, evento_atual[2])
            self.lista_eventos.extend(novos_eventos)


random.seed(20)
# ==============================================================


def gerar_variavel_exp(lamb):
    y = random.random()
    
    return -(math.log(1-y)/lamb)



def chegada_fila(tempo, globais, auxiliar, dados):
    novos_eventos = []
    #print(tempo, ": Comeca fila")

    globais["N"] += 1
    pessoa = {
        "tempo_chegada" : tempo,
        "tempo_inicio_servico" : None,
        "tempo_fim_servico" : None
    }

    if(not globais["em_servico"]):
        pessoa["tempo_inicio_servico"] = tempo
        coleta_estatistica("W", 0, globais) # coletando a estatística de uma pessoa que chegou imediatamente ao sistema
        novos_eventos.append( (tempo + gerar_variavel_exp(globais["mi"]) , termina_servico, pessoa) )
        globais["em_servico"] = True
    else:
        auxiliar.append(pessoa)


    novos_eventos.append( (tempo + gerar_variavel_exp(globais["lamb"]), chegada_fila, None) )

    return novos_eventos



def termina_servico(tempo, globais, auxiliar, dados):
    novos_eventos = []
    #print(tempo, ": Termina Fila")
    globais["N"] -= 1

    pessoa_saida = dados
    pessoa_saida["tempo_fim_servico"] = tempo



    if(globais["N"] == 0):
        globais["em_servico"] = False
    
    else:
        nova_pessoa = auxiliar.pop(0)
        nova_pessoa["tempo_inicio_servico"] = tempo
        coleta_estatistica("W", nova_pessoa["tempo_inicio_servico"] - nova_pessoa["tempo_chegada"], globais)
        novos_eventos.append( (tempo + gerar_variavel_exp(globais["mi"]), termina_servico, nova_pessoa ) )
    return novos_eventos

count_w = 0
soma_w = 0
def coleta_estatistica(tipo ,dados, globais):
    global soma_w, count_w
    if(tipo == "W"):
        soma_w += dados
        count_w += 1
        if(count_w % 100000 == 0):
            print(soma_w/count_w, ((globais["lamb"])/(globais["mi"]**2))/(1-(globais["lamb"]/globais["mi"])) )


def funcao_inicio(globais, auxiliar, lista_eventos):
    lista_eventos.clear()
    globais["N"] = 0
    
    globais["mi"] = 1.0
    globais["lamb"] = 0.8
    globais["em_servico"] = False

    lista_eventos.append( (gerar_variavel_exp(globais["lamb"]), chegada_fila, None) )


g = {
    "em_servico" : False,
    "mi" : 1.0,
    "lamb" : 0.8,
    "N" : 0
}

e = Eventos(g)

e.start(funcao_inicio, 20000000)

