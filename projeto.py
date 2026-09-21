from collections import deque

 
def reconstruir_caminho(visitados_ida, visitados_volta, intersecao):
    """Junta o caminho da origem até a interseção, e da interseção até o destino"""
    caminho = []
 
    # Do início até a interseção
    atual = intersecao
    while atual is not None:
        caminho.append(atual)
        atual = visitados_ida[atual]
    caminho.reverse()  # Inverte para ficar na ordem: origem -> interseção
 
    # Da interseção até o destino
    atual = visitados_volta[intersecao]
    while atual is not None:
        caminho.append(atual)
        atual = visitados_volta[atual]
 
    return caminho
 
 
def bfs_passo(fila, visitados_atuais, visitados_opostos, grafo):
    """Executa um passo da Busca em Largura: retira um nó da fila e expande seus vizinhos"""
    atual = fila.popleft()
 
    for vizinho in grafo.get(atual, []):
        if vizinho not in visitados_atuais:
            visitados_atuais[vizinho] = atual  # Guarda quem é o "pai" do vizinho
            fila.append(vizinho)
 
            # Se o vizinho já foi visitado pela outra busca, encontramos a interseção!
            if vizinho in visitados_opostos:
                return vizinho
    return None
 
 
def busca_bidirecional(grafo, origem, destino):
    if origem == destino:
        return [origem]
 
    # Filas para a busca
    fila_ida = deque([origem])
    fila_volta = deque([destino])
 
    # Dicionários para guardar os nós visitados e seus "pais"
    visitados_ida = {origem: None}
    visitados_volta = {destino: None}
 
    while fila_ida and fila_volta:
        # Expande a partir da origem
        intersecao = bfs_passo(fila_ida, visitados_ida, visitados_volta, grafo)
        if intersecao:
            return reconstruir_caminho(visitados_ida, visitados_volta, intersecao)
 
        # Expande a partir do destino
        intersecao = bfs_passo(fila_volta, visitados_volta, visitados_ida, grafo)
        if intersecao:
            return reconstruir_caminho(visitados_ida, visitados_volta, intersecao)
 
    return None  # Retorna None se não houver caminho
 
 
# ----------------------------------------------------------------------
# Grafo do slide: 16 cidades entre São Paulo e Rio de Janeiro
# ----------------------------------------------------------------------
 
grafo_rodovias = {
    # Via Dutra (rota principal)
    'São Paulo':      ['SJC', 'Atibaia', 'Santos'],
    'SJC':            ['São Paulo', 'Taubaté'],
    'Taubaté':        ['SJC', 'Resende'],
    'Resende':        ['Taubaté', 'Barra Mansa', 'Cruzeiro'],
    'Barra Mansa':    ['Resende', 'Piraí'],
    'Piraí':          ['Barra Mansa', 'Rio de Janeiro'],
    'Rio de Janeiro': ['Piraí', 'Itaguaí'],
 
    # Rota da serra (norte)
    'Atibaia':        ['São Paulo', 'Bragança'],
    'Bragança':       ['Atibaia', 'Cruzeiro'],
    'Cruzeiro':       ['Bragança', 'Resende'],
 
    # Rota do litoral (sul)
    'Santos':         ['São Paulo', 'Ubatuba'],
    'Ubatuba':        ['Santos', 'Paraty'],
    'Paraty':         ['Ubatuba', 'Angra'],
    'Angra':          ['Paraty', 'Mangaratiba'],
    'Mangaratiba':    ['Angra', 'Itaguaí'],
    'Itaguaí':        ['Mangaratiba', 'Rio de Janeiro'],
}
 
# Quilometragem de cada trecho (usada só para exibir o total no final)
distancias = {
    ('São Paulo', 'SJC'): 80,        ('SJC', 'Taubaté'): 50,
    ('Taubaté', 'Resende'): 70,      ('Resende', 'Barra Mansa'): 50,
    ('Barra Mansa', 'Piraí'): 60,    ('Piraí', 'Rio de Janeiro'): 50,
    ('São Paulo', 'Atibaia'): 90,    ('Atibaia', 'Bragança'): 70,
    ('Bragança', 'Cruzeiro'): 110,   ('Cruzeiro', 'Resende'): 80,
    ('São Paulo', 'Santos'): 70,     ('Santos', 'Ubatuba'): 120,
    ('Ubatuba', 'Paraty'): 130,      ('Paraty', 'Angra'): 90,
    ('Angra', 'Mangaratiba'): 60,    ('Mangaratiba', 'Itaguaí'): 50,
    ('Itaguaí', 'Rio de Janeiro'): 110,
}
 
 
def km_total(caminho):
    """Soma a quilometragem do caminho encontrado"""
    total = 0
    for a, b in zip(caminho, caminho[1:]):
        total += distancias.get((a, b)) or distancias.get((b, a))
    return total
 
 
def testar(origem, destino):
    print(f"\nBusca Bidirecional: {origem} -> {destino}")
    caminho = busca_bidirecional(grafo_rodovias, origem, destino)
 
    if caminho is None:
        print("Não existe caminho entre as duas cidades.")
    else:
        print(f"Rota encontrada: {' -> '.join(caminho)}")
        print(f"{len(caminho) - 1} trechos | {km_total(caminho)} km")
 
 
# Uso de exemplo
if __name__ == "__main__":
    testar('São Paulo', 'Rio de Janeiro')
    testar('Santos', 'Cruzeiro')