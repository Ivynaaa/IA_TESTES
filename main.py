import heapq
import itertools

class No:
    def __init__(self, posicao, g, h, pai=None):
        self.posicao = posicao  # Posição do nó no mapa
        self.g = g  # Custo do início até este nó
        self.h = h  # Estimativa do custo até o destino (heurística)
        self.f = g + h  # Função de custo total
        self.pai = pai  # Nó pai para reconstruir o caminho

    def __lt__(self, outro):
        return self.f < outro.f

def heuristica(a, b):
    """Função heurística (distância de Manhattan)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def busca_a_estrela(mapa, inicio, fim):
    """Executa o algoritmo A* para encontrar o caminho mais curto entre inicio e fim."""
    lista_aberta = []
    lista_fechada = set()
    no_inicio = No(inicio, 0, heuristica(inicio, fim))
    heapq.heappush(lista_aberta, no_inicio)

    while lista_aberta:
        no_atual = heapq.heappop(lista_aberta)
        lista_fechada.add(no_atual.posicao)

        # Se o nó final for alcançado, reconstrua o caminho
        if no_atual.posicao == fim:
            caminho = []
            while no_atual:
                caminho.append(no_atual.posicao)
                no_atual = no_atual.pai
            return caminho[::-1]  # Caminho do início ao fim

        # Movimentos possíveis (cima, baixo, esquerda, direita)
        vizinhos = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for movimento in vizinhos:
            posicao_vizinha = (no_atual.posicao[0] + movimento[0], no_atual.posicao[1] + movimento[1])

            # Verifique se o movimento é válido
            if (0 <= posicao_vizinha[0] < len(mapa)) and (0 <= posicao_vizinha[1] < len(mapa[0])):
                if posicao_vizinha in lista_fechada:
                    continue
                custo_terreno = mapa[posicao_vizinha[0]][posicao_vizinha[1]]
                custo_g = no_atual.g + custo_terreno
                custo_h = heuristica(posicao_vizinha, fim)
                no_vizinho = No(posicao_vizinha, custo_g, custo_h, no_atual)
                
                # Adiciona o nó à lista aberta se for um melhor caminho
                if all(no_vizinho.posicao != n.posicao or no_vizinho.f < n.f for n in lista_aberta):
                    heapq.heappush(lista_aberta, no_vizinho)
    
    return None  # Retorna None se não houver caminho

def calcular_custo_total(mapa, inicio, caminho):
    """Calcula o custo total de um caminho usando o A* para cada segmento."""
    custo_total = 0
    caminho_total = []
    inicio_atual = inicio

    for parada in caminho:
        segmento_caminho = busca_a_estrela(mapa, inicio_atual, parada)
        if segmento_caminho is None:
            return float('inf'), []  # Caminho impossível
        custo_segmento = sum(mapa[x][y] for x, y in segmento_caminho)
        custo_total += custo_segmento
        caminho_total += segmento_caminho[:-1]
        inicio_atual = parada
        print(f"Custo para a parada {parada}: {custo_segmento}")

    caminho_total.append(caminho[-1])
    return custo_total, caminho_total

def forca_bruta_com_a_estrela(mapa, inicio, paradas):
    """Usa força bruta para encontrar a melhor ordem de paradas e o menor custo."""
    melhor_custo = float('inf')
    melhor_caminho = []

    for permutacao in itertools.permutations(paradas):
        custo, caminho = calcular_custo_total(mapa, inicio, permutacao)
        if custo < melhor_custo:
            melhor_custo = custo
            melhor_caminho = caminho

    return melhor_custo, melhor_caminho

# Exemplo de uso:
mapa = [
    [1, 1, 2, 3],
    [1, 2, 3, 1],
    [3, 1, 1, 1],
    [1, 1, 1, 1]
]

inicio = (0, 0)
paradas = [(0, 2), (2, 2), (3, 3)]

melhor_custo, melhor_caminho = forca_bruta_com_a_estrela(mapa, inicio, paradas)
print("Melhor custo encontrado:", melhor_custo)
print("Melhor caminho encontrado:", melhor_caminho)
print("\nCaminho percorrido ponto a ponto:")
for ponto in melhor_caminho:
    print(ponto)
