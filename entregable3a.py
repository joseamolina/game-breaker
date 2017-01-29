'''
@Authors: Adrián Eniquez, José Ángel Molina, Pablo berbel.
'''

from bt_scheme import PartialSolutionWithVisitedControl, bt_solve_vc
from brikerdef import Move, Block, Level
import sys

def bricker_vc_solver(level):
    class Briker_vc_PS(PartialSolutionWithVisitedControl):
        def __init__(self, block, decisions):
            self.block = block
            self.decisions = decisions

        #Es solución cuando se ha alcanzado la posición final del tablero
        def is_solution(self)-> "bool":
            return self.block.isStandingAtPos(level.targetPos())
    
        def get_solution(self)  -> "solution":
            return self.decisions
    
        def successors(self) -> "IEnumerable<Briker_vc_PS> o List<Briker_vc_PS>":
            #Creamos un sucesor por cada movimiento válido desde la situación actual del bloque
            #No nos preocupamos de volver a la posición anterior, ya que el control de visitados de encargará de que no genere sucesores
            for movement in self.block.validMoves():
                decisions = self.decisions[:]
                decisions.append(movement)
                yield Briker_vc_PS(self.block.move(movement), decisions)
        
        #El estado del bloque es el propio bloque, ya que crea su código hash a partir de su posición, que es lo que consideramos estado
        def state(self)-> "state": 
            return self.block
    
    # Implementar bricker_vc_solver:
    # crea initial_ps y llama a bt_solve_vc
    # Creamos el bloque inicial, en la posición inicial del tablero y la partida inicial con la lista de decisiones vacía
    initial_block = Block(level.startPos(), level.startPos(), level.isValid)
    initial_ps = Briker_vc_PS(initial_block, [])
    yield from bt_solve_vc(initial_ps)
    
level_filename = sys.argv[1]

print("<BEGIN BACKTRACKING>\n")

for solution in bricker_vc_solver(Level(level_filename)):
    string_solution = "".join(solution) #convierte la solución de lista a string
    print("La primera solución encontrada es: {0} (longitud: {1})".format(string_solution, len(string_solution)))
    break
    
print("\n<END BACKTRACKING>")
