from collections import deque

def reconstruir_caminho(visitados_ida, visitados_volta, intersecao):
    """Junta o caminho da origem até a interseção, e da interseção até o destino"""
    caminho = []
    
    # Do início até a interseção
    atual = intersecao
    while atual is not None:
        caminho.append(atual)
        atual = visitados_ida[atual]
    caminho.reverse() # Inverte para ficar na ordem: origem -> interseção
    
    # Da interseção até o destino
    atual = visitados_volta[intersecao]
    while atual is not None:
        caminho.append(atual)
        atual = visitados_volta[atual]
        
    return caminho

def bfs_passo(fila, visitados_atuais, visitados_opostos, grafo):
    """Executa apenas um passo da Busca em Largura (expande um nível)"""
    atual = fila.popleft()
    
    for vizinho in grafo.get(atual, []):
        if vizinho not in visitados_atuais:
            visitados_atuais[vizinho] = atual # Guarda quem é o "pai" do vizinho
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
        # Expande um nível a partir da origem
        intersecao = bfs_passo(fila_ida, visitados_ida, visitados_volta, grafo)
        if intersecao:
            return reconstruir_caminho(visitados_ida, visitados_volta, intersecao)
            
        # Expande um nível a partir do destino
        intersecao = bfs_passo(fila_volta, visitados_volta, visitados_ida, grafo)
        if intersecao:
            return reconstruir_caminho(visitados_ida, visitados_volta, intersecao)
            
    return None # Retorna None se não houver caminho

# Uso de exemplo
if __name__ == "__main__":
    # Grafo de exemplo (Lista de Adjacência)
    grafo_exemplo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'G'],
        'F': ['C', 'H'],
        'G': ['E', 'I'],
        'H': ['F', 'I'],
        'I': ['G', 'H']
    }

print("\nBusca Bidirecional: A -> I")
caminho = busca_bidirecional(grafo_exemplo, 'A', 'I')
print(f"Caminho encontrado: {' -> '.join(caminho)}")

print("\nBusca Bidirecional: A -> H")
caminho = busca_bidirecional(grafo_exemplo, 'A', 'H')
print(f"Caminho encontrado: {' -> '.join(caminho)}")