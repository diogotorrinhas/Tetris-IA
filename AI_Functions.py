#AI methods
import copy

#TODAS AS AÇOES PARA CADA POSIÇAO DE CADA PEÇA
ACTIONS = [[], ["a"], ["a","a"], ["a","a","a"], ["d"], ["d","d"], ["d","d","d"], ["d","d","d","d"]]

#criar uma função para ver as melhores posições para cada peça 
def best_position(original_grid,piece): #Piece é a peça que vem(utilizar a função piece) OU peça que vem como SHAPE
    positions_list, action_list = next_actions(piece)
    key = calculate_score_and_keys(positions_list,action_list,original_grid) 

    return key

#Retorna o número de buracos em cada linha 
def calculate_holes(grid,lastposition):     #OTIMIZAR ESTA FUNÇÃO
    
   holes = 0
   aux_array = []  # array auxiliar para adicionar os elementos com a msm row
   
   aux_grid = grid + lastposition

   for j in range(len(aux_grid)):
        
      element = aux_grid[j]
      actual_row = element[1]  # por exemplo actual_row = 28
      aux_array.append(element)
           

      if element[1] == 29:
         aux_array.remove(element)

      for index in range(len(aux_array)):  # search for an hole
         actualElement = aux_array[index]  # por exemplo [3,28]
               
         col = actualElement[0]  # 3
         row = actualElement[1]  # 28
              
         for new_row in range(row+1,30):
            if [col, new_row] not in aux_grid:  # se [3,29] não estiver no grid,há um buraco
               holes += 1
            else:
               break
         aux_array.clear()  # limpar o array auxliar para voltarmos a usa-lo

   return holes

def Column_heights(grid_map,lastposition):    #retorna a soma de tds as colunas / lastposition é a posição final da peça q vamos juntar ao grid do tabuleiro
    aux = grid_map + lastposition
    heights= []
     
    matriz = [[0 for i in range(8)] for j in range(30)]
    for x,y in aux:
        matriz[y][x-1] = 1

    for row in range(8):
        tempHeight = []
        for col in range(30):
            if matriz[col][row] > 0:
               tempHeight.append(30 - col)
        if len(tempHeight) > 0:
            heights.append(max(tempHeight))
        else:
            heights.append(0)
               
    return heights

def Aggregate_Height(ColumnHeights):    #passar como argumento a função Collumn_Heights
    return sum(ColumnHeights)

def complete_lines(grid,lastPosition):  #voltar a ver melhor esta função
    numero_linhas_completas = 0  #linhas completas
    numerodelementos = 0
    array = []
    arraytest = []
    aux_grid = grid + lastPosition

    for ola in range(len(aux_grid)):
        elementotest = aux_grid[ola]
        linhaola = elementotest[1]
        arraytest.append(linhaola)
    
    yminimo = min(arraytest)

    for x in range(29, yminimo, -1):
        for j in range(len(aux_grid)):
            element = aux_grid[j]    #vai dar por exemplo [5,28], temos de procurar se existe a coluna na linha e count++
            actual_row = element[1]     #por exemplo actual_row = 28
            if actual_row == x:
                array.append(element)
        numerodelementos = len(array)
        if(numerodelementos == 8):
             numero_linhas_completas = numero_linhas_completas +1
        array.clear()

    return numero_linhas_completas
   
def calculate_smotheness(ColumnHeights):     #variation of its column heights
    smoothness = 0
    for i in range(len(ColumnHeights)-1):
        smoothness += abs(ColumnHeights[i] - ColumnHeights[i+1])
    return smoothness

def last_Position(grid, position):
    Position = []  # posição final da peça
    lastPos = []
    aux = []  # lista para armazenar os valores da peça com o y incrementado
    aux_y = []  # lista auxiliar para armazenar o y min da peça
    primeiro_quadrado = position[0]  # [2, 2]
    segundo_quadrado = position[1]  # [3, 2]
    terceiro_quadrado = position[2]  # [3, 3]
    quarto_quadrado = position[3]  # [4, 3]
    for x in range(len(position)):
        elemento = position[x]  # por exemplo [2,2]
        y_element = elemento[1]  # por exemplo 2
        aux_y.append(y_element)  # [2,2,3,3]
    y = max(aux_y)  # y = 4, ou seja, partimos dessa posição
    aux1 = primeiro_quadrado[1]
    aux2 = segundo_quadrado[1]
    aux3 = terceiro_quadrado[1]
    aux4 = quarto_quadrado[1]
    for j in range((y+1), 30):
        aux1 = aux1 + 1
        aux2 = aux2 + 1
        aux3 = aux3 + 1
        aux4 = aux4 + 1
        newPrimeiroQuadrado = [primeiro_quadrado[0], aux1]
        newSegundoQuadrado = [segundo_quadrado[0], aux2]
        newTerceiroQuadrado = [terceiro_quadrado[0], aux3]
        newQuartoQuadrado = [quarto_quadrado[0], aux4]
        pos = [newPrimeiroQuadrado] + [newSegundoQuadrado] + [newTerceiroQuadrado] + [newQuartoQuadrado]
        aux.append(pos)
    count = 0
        # percorrer o array com os valores com o y incrementado
    verify_lastPos = False
    for arrayPosition in range(len(aux)):
      p = aux[arrayPosition]  # [[2, 3], [3, 3], [3, 4], [4, 4]]
      for i in range(len(p)):
         if p[i] not in grid:
            count += 1  # um quadrado da peça não está no grid
      if count == 4:  # se os 4 quadrados não estiverem na grid, significa que a peça não está no grid
         Position = p
      else:
         Position = lastPos  # caso esteja no grid, a posição final é igual à anterior
         verify_lastPos = True
      lastPos = Position  # [[4,7],[4,8],[5,8],[4,9]]
      count = 0
      if verify_lastPos:
         break
    #aux.clear()  # limpar o array auxiliar para meter lá os valores da peça com o novo valor de y incrementado
    return Position

def rotate_piece(piece):   #piece é a shape da peça, usar funçao piece OU a posição atual da peça, tipo [4,3],[2,6],[2,3],[4,5], passar como parametro função piece
    if piece == [[4,2], [4,3], [5,3], [5,4]]:        #"S"  [[4,2], [4,3], [5,3], [5,4]]
        return [[[4,2], [4,3], [5,3], [5,4]],
                [[4,2], [5,2], [3,3], [4,3]]]
    elif piece == [[4,2], [3,3], [4,3], [3,4]]:      #"Z"  [[4,2], [3,3], [4,3], [3,4]]
        return [[[4,2], [3,3], [4,3], [3,4]],     
                [[3,2], [4,2], [4,3], [5,3]]]
    elif piece == [[2,2], [3,2], [4,2], [5,2]]:      #"I"  [[2,2], [3,2], [4,2], [5,2]]
        return [[[2,2], [3,2], [4,2], [5,2]],     
                [[4,2], [4,3], [4,4], [4,5]]]
    elif piece == [[3,3], [4,3], [3,4], [4,4]]:      #"O"  [[3,3], [4,3], [3,4], [4,4]]
        return [[[3,3], [4,3], [3,4], [4,4]]]
    elif piece == [[4,2], [5,2], [4,3], [4,4]]:      #"J"  [[4,2], [5,2], [4,3], [4,4]]
        return [[[4,2], [5,2], [4,3], [4,4]],     
                [[3,3], [4,3], [5,3], [5,4]],     
                [[4,2], [4,3], [3,4], [4,4]],     
                [[3,2], [3,3], [4,3], [5,3]]]
    elif piece == [[4,2], [4,3], [4,4], [5,4]]:      #"L"  [[4,2], [4,3], [4,4], [5,4]]
        return [[[4,2], [4,3], [4,4], [5,4]],     
                [[3,3], [4,3], [5,3], [3,4]],     
                [[3,2], [4,2], [4,3], [4,4]],     
                [[5,2], [3,3], [4,3], [5,3]]]
    elif piece == [[4,2], [4,3], [5,3], [4,4]]:      #"T"  [[4,2], [4,3], [5,3], [4,4]]
        return [[[4,2], [4,3], [5,3], [4,4]],     
                [[3,3], [4,3], [5,3], [4,4]],     
                [[4,2], [3,3], [4,3], [4,4]],     
                [[4,2], [3,3], [4,3], [5,3]]]
    return None

def moveLeft(piece):
    primeiro_quadrado = piece[0]     #[4,6]
    segundo_quadrado = piece[1]      #[4,7]
    terceiro_quadrado = piece[2]     #[5,7]
    quarto_quadrado = piece[3]       #[4,8]
    new_x1 = primeiro_quadrado[0]-1  #3
    new_x2 = segundo_quadrado[0]-1  #3
    new_x3 = terceiro_quadrado[0]-1 #4
    new_x4 = quarto_quadrado[0]-1   #3

    for i in range(len(piece)):
        elemento = piece[i]
        if i == 0:
            elemento[0] = new_x1
        elif i == 1:
            elemento[0] = new_x2
        elif i == 2:
            elemento[0] = new_x3
        elif i == 3:
            elemento[0] = new_x4
    return piece

def moveRight(piece):
    primeiro_quadrado = piece[0]     #[4,6]
    segundo_quadrado = piece[1]      #[4,7]
    terceiro_quadrado = piece[2]     #[5,7]
    quarto_quadrado = piece[3]       #[4,8]
    new_x1 = primeiro_quadrado[0]+1  #5
    new_x2 = segundo_quadrado[0]+1  #5
    new_x3 = terceiro_quadrado[0]+1 #6
    new_x4 = quarto_quadrado[0]+1   #5

    for i in range(len(piece)):
        elemento = piece[i]
        if i == 0:
            elemento[0] = new_x1
        elif i == 1:
            elemento[0] = new_x2
        elif i == 2:
            elemento[0] = new_x3
        elif i == 3:
            elemento[0] = new_x4
    return piece


def calculate_heuristics_and_Score(grid,lastPosition):          #state é a grid + lastP
    lines_completed = complete_lines(grid,lastPosition)
    holes_grid = calculate_holes(grid,lastPosition)         #holes atuais no grid, ainda sem a peça que está a cair
    listOfCollumnHeights = Column_heights(grid,lastPosition)    #lista com a soma de cada coluna
    AggregateHeight = Aggregate_Height(listOfCollumnHeights)
    Bumpinees = calculate_smotheness(listOfCollumnHeights)

    #a = -0.510066
    #b = 0.760666               
    #c = -0.35663       #valores heuristica 1
    #d = -0.184483
    
    a = -0.695545
    b = 0.608533        #valores heuristica 2
    c = -0.38905
    d = -0.201254    

    result = (a*AggregateHeight) + (b*lines_completed) + (c*holes_grid) + (d*Bumpinees)
    return result
   
def out_of_board(piece):
    min_x = 8
    max_x = 1
    for point in piece:
        if min_x > point[0]:
            min_x = point[0]
        if max_x < point[0]:
            max_x = point[0]
    return min_x < 1 or max_x > 8

def next_actions(piece):
    possible_actions = []
    possible_positions = []
    rotations = rotate_piece(piece)
    for i in range(len(rotations)):
        for action_list in ACTIONS:
            position = copy.deepcopy(rotations[i])  #posiçao atual
            for action in action_list:
                if action == "a":
                    position = moveLeft(position)
                elif action == "d":
                    position = moveRight(position)  #[[1,2],[2,2],[3,2],[4,2]]
            if not out_of_board(position):
                possible_positions.append(position)
                possible_actions.append(["w"]*i + action_list)
    return possible_positions,possible_actions                            

def calculate_score_and_keys(possible_positions,possible_actions,original_grid):
    scores = []
    for i in range(len(possible_positions)):
        grid = [ p.copy() for p in original_grid ]
        position = possible_positions[i]
        lastPosition = last_Position(grid,position) 
        #new_grid = grid + lastPosition
        score = calculate_heuristics_and_Score(grid,lastPosition)
        scores.append(score)
    index_max = max(range(len(scores)), key=scores.__getitem__) #achar o indice do valor máximo da lista scores
    keys = possible_actions[index_max]
    return keys
        