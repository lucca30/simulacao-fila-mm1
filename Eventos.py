import random
import math

class Eventos:
    def __init__(self, globais):
        self.globais = globais
        self.auxiliar = []
        self.lista_eventos = []

    def start(self, start_function, rounds):
        start_function(self.globais, self.auxiliar, self.lista_eventos)

        for i in range(rounds):
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

    print(pessoa_saida)


    if(globais["N"] == 0):
        globais["em_servico"] = False
    
    else:
        nova_pessoa = auxiliar.pop(0)
        nova_pessoa["tempo_inicio_servico"] = tempo
        novos_eventos.append( (tempo + gerar_variavel_exp(globais["mi"]), termina_servico, nova_pessoa ) )
    return novos_eventos
    

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

e.start(funcao_inicio, 20)