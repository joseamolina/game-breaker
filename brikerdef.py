'''
@Authors: Adrián Eniquez, José Ángel Molina, Pablo berbel.
'''
import types

# ---------------------------------------------------------------------------------------------------------

class Move: 
    Left = "L"
    Right = "R"
    Up = "U"
    Down = "D"

# ---------------------------------------------------------------------------------------------------------
 
class Pos2D:
    __slots__ = ('row', 'col')
    
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def incRow(self, d) -> "Pos2D":
        return Pos2D(self.row + d, self.col)

    def incCol(self, d) -> "Pos2D":
        return Pos2D(self.row, self.col + d)
    
    def __eq__(self, other):
        if not isinstance(other, Pos2D): return False
        return self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.row, self.col))
    
    def __repr__(self):
        return "(Row:{0}, Col:{1})".format(self.row, self.col)

# ---------------------------------------------------------------------------------------------------------
  
class Level:
    __slots__ = ('rows', 'cols', '_mat', '_sPos', '_tPos')
    
    def __init__(self, filename: "string"):
        self._mat = [line.strip() for line in open(filename).readlines()]
        self.rows = len(self._mat)
        self.cols = len(self._mat[0])
        for i in range(self.rows):
            for j in range(self.cols):
                if self._mat[i][j] == 'S': self._sPos = Pos2D(i, j)
                if self._mat[i][j] == 'T': self._tPos = Pos2D(i, j)
        
    def isValid(self, pos: "Pos2D") -> "boolean":      
        return pos.row < self.rows and pos.col < self.cols and pos.row >= 0 and pos.col >= 0 and self._mat[pos.row][pos.col] != '-'
    def startPos(self) -> "Pos2D":
        return self._sPos
    
    def targetPos(self) -> "Pos2D":
        return self._tPos

# ---------------------------------------------------------------------------------------------------------
          
class Block: 
    __slots__ = ('_b1', '_b2', '_isValidPos')
    
    def __init__(self, b1: "Pos2D", b2: "Pos2D", isValidPos: "Pos2D -> boolean"):
        assert isinstance(b1, Pos2D) and isinstance(b2, Pos2D) and \
               type(isValidPos)==types.MethodType and \
               isValidPos(Pos2D(0,0)) in [True, False]
        if b2.row<b1.row or b2.col<b1.col: 
            self._b1, self._b2 = b2, b1
        else: 
            self._b1, self._b2 = b1, b2
        self._isValidPos = isValidPos
    
    # <BEGIN> Funciones para comparar correctamente objetos de tipo Block
    #    -Para que __eq__ y __hash__ funcionen correctamente, los dos bloques _b1
    #    y _b2 deben cumplir que _b1 sea siempre el más cercano al (0,0) 
    #    -Dos Block son iguales si sus _b1 y _b2 lo son.  
    def __eq__(self, other):
        if not isinstance(other, Block): return False
        return self._b1 == other._b1 and self._b2 == other._b2
        
    # Necesario para poder meter objetos de tipo Block en colecciones
    def __hash__(self): 
        # Un hash típico de dos valores que tienen un hash propio
        return hash(self._b1) ^ hash(self._b2)
    # <END> Funciones para comparar correctamente objetos de tipo Block
        
    def __repr__(self):
        return "[{0}, {1}]".format(self._b1, self._b2)
        
    def isStanding(self) -> "boolean": # true si el bloque está de pie
        return self._b1 == self._b2
    
    def isLyingOnSameRow(self) -> "boolean": # true si el bloque está tumbado en una fila
        return self._b1.row == self._b2.row and self._b1.col != self._b2.col

    def isLyingOnSameCol(self) -> "boolean": # true si el bloque está tumbado en una columna
        return self._b1.row != self._b2.row and self._b1.col == self._b2.col

    def isStandingAtPos(self, pos: "Pos2D") -> "bool":
        # Devuelve true si el bloque está de pie en la posición indicada en el parámetro
        return self.isStanding() and self._b1 == pos
    
    def validMoves(self) -> "Iterable<Move>":
        moves = []
        if self.isStanding():
            if self._isValidPos(self._b1.incCol(-1)) and self._isValidPos(self._b2.incCol(-2)):
                moves.append(Move.Left)
            if self._isValidPos(self._b1.incCol(1)) and self._isValidPos(self._b2.incCol(2)):
                moves.append(Move.Right)
            if self._isValidPos(self._b1.incRow(-1)) and self._isValidPos(self._b2.incRow(-2)):
                moves.append(Move.Up)
            if self._isValidPos(self._b1.incRow(1)) and self._isValidPos(self._b2.incRow(2)):
                moves.append(Move.Down)
        elif self.isLyingOnSameCol():
            if self._isValidPos(self._b1.incCol(-1)) and self._isValidPos(self._b2.incCol(-1)):
                moves.append(Move.Left)
            if self._isValidPos(self._b1.incCol(1)) and self._isValidPos(self._b2.incCol(1)):
                moves.append(Move.Right)
            if self._isValidPos(self._b2.incRow(-2)) and self._isValidPos(self._b1.incRow(-1)):
                moves.append(Move.Up)
            if self._isValidPos(self._b1.incRow(2)) and self._isValidPos(self._b1.incRow(1)):
                moves.append(Move.Down)
        else:
            if self._isValidPos(self._b2.incCol(-2)) and self._isValidPos(self._b1.incCol(-1)):
                moves.append(Move.Left)
            if self._isValidPos(self._b1.incCol(2)) and self._isValidPos(self._b2.incCol(1)):
                moves.append(Move.Right)
            if self._isValidPos(self._b1.incRow(-1)) and self._isValidPos(self._b2.incRow(-1)):
                moves.append(Move.Up)
            if self._isValidPos(self._b1.incRow(1)) and self._isValidPos(self._b2.incRow(1)):
                moves.append(Move.Down)
        return moves
            
    def move(self, m : "Move") -> "Block" :
        if m == Move.Left: 
            if self.isLyingOnSameCol():
                b1 = self._b1.incCol(-1)
                b2 = self._b2.incCol(-1)
            #Este caso agrupa también al caso de que esté de pie, ya que en ese caso no importa cuál de los dos se mueve 1 y cuál 2
            #Similar en los demás else de cada movimiento
            else:
                b1 = self._b1.incCol(-1)
                b2 = self._b2.incCol(-2)
        elif m == Move.Right:
            if self.isLyingOnSameCol():
                b1 = self._b1.incCol(1)
                b2 = self._b2.incCol(1)
            else:
                b1 = self._b1.incCol(2)
                b2 = self._b2.incCol(1)
        elif m == Move.Up:
            if self.isLyingOnSameRow():
                b1 = self._b1.incRow(-1)
                b2 = self._b2.incRow(-1)
            else:
                b1 = self._b1.incRow(-1)
                b2 = self._b2.incRow(-2)
        else:
            if self.isLyingOnSameRow():
                b1 = self._b1.incRow(1)
                b2 = self._b2.incRow(1)
            else:
                b1 = self._b1.incRow(2)
                b2 = self._b2.incRow(1)
        return Block(b1, b2, self._isValidPos)

# ---------------------------------------------------------------------------------------------------------