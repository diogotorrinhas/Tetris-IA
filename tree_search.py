# Problemas concretos a resolver
# dentro de um determinado dominio

# Nos de uma arvore de pesquisa
class State:
    def __init__(self,piece,parent,depth,cost,heuristic):
        self.piece = piece
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + "," + str(self.depth) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'):
        self.problem = problem
        root = State(problem.initial, None,0,0,0)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.length = None
        self.terminals = 0
        self.non_terminals = 0
        self.ratio = 0
        self.cost = None

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # procurar a solucao
    def search(self,limit=100):     
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            #path = self.get_path(node)
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes)+1
                self.length = self.solution.depth
                self.ratio = round(self.terminals+self.non_terminals-1/self.non_terminals)
                self.cost = node.cost
                return self.get_path(node)
            self.non_terminals += 1  
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):   #o state é o estado atual(cidade atual=aveiro) e a action é (ex) de aveiro para viseu 
                newstate = self.problem.domain.result(node.state,a) #se o state for aveiro, e a ação for [viseu,aveiro] e a ação existir, o resultado é viseu
                if newstate not in self.get_path(node) and node.depth < limit: 
                    p = node.depth + 1
                    custo = node.cost + self.problem.domain.cost(node.state,a)
                    newnode = SearchNode(newstate,node,p,custo, self.problem.domain.heuristic(newstate,self.problem.goal))
                    lnewnodes.append(newnode)
            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key=lambda node: node.cost)
        elif self.strategy == 'greedy':
            self.open_nodes == sorted(self.open_nodes + lnewnodes, key=lambda node: node.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes ==  sorted(self.open_nodes + lnewnodes, key=lambda node: node.cost + node.heuristic)
        

