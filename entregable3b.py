'''
@Authors: Adrián Eniquez, José Ángel Molina, Pablo berbel.
'''

from bt_scheme import PartialSolutionWithOptimization, bt_solve_opt
from brikerdef import Move, Block, Level
import sys
   
def bricker_opt_solver(level):
    class Briker_opt_PS(PartialSolutionWithOptimization):
        def __init__(self, block, decisions):
            self.block = block
            self.decisions = decisions

         #Es solución cuando se ha alcanzado la posición final del tablero
        def is_solution(self)-> "bool":
            return self.block.isStandingAtPos(level.targetPos())
    
        def get_solution(self)  -> "solution":
            return self.decisions
    
        def successors(self) -> "IEnumerable<Briker_opt_PS> o List<Briker_opt_PS>":
            #Creamos un sucesor por cada movimiento válido desde la situación actual del bloque
            #No nos preocupamos de volver a la posición anterior, ya que el control de visitados de encargará de que no genere sucesores
            for movement in self.block.validMoves():
                decisions = self.decisions[:]
                decisions.append(movement)
                yield Briker_opt_PS(self.block.move(movement), decisions)
        
        #El estado del bloque es el propio bloque, ya que crea su código hash a partir de su posición, que es lo que consideramos estado
        def state(self) -> "state": 
            return self.block
        
        #La función objetivo devuelve el número de decisiones tomadas, que es lo que queremos minimizar
        def f(self) -> "int o float":
            return len(self.decisions)
    
    # Implementar bricker_opt_solver:
    # crea initial_ps y llama a bt_solve_opt
    # Creamos el bloque inicial, en la posición inicial del tablero y la partida inicial con la lista de decisiones vacía
    initial_block = Block(level.startPos(), level.startPos(), level.isValid)
    initial_ps = Briker_opt_PS(initial_block, [])
    yield from bt_solve_opt(initial_ps)

if len(sys.argv)!=2:
    print("No se indicó: <nombre fichero>")
    exit()

  
level_filename = sys.argv[1]

print("<BEGIN BACKTRACKING>\n")

# la última solución que devuelva será la más corta
solutions = list(bricker_opt_solver(Level(level_filename)))

if len(solutions)==0:
    print("El puzle no tiene solución.")
else:
    best_solution = solutions[-1]
    string_solution = "".join(best_solution) #convierte la solución de lista  a  string
    print("La solución más corta es: {0} (longitud: {1})".format(string_solution, len(string_solution)))
    
print("\n<END BACKTRACKING>")