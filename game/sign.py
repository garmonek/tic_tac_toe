from enum import Enum

class Sign(Enum):
     X = 'X'
     O = 'O'

     def opposite(self):
     	return Sign.X if self == Sign.O else Sign.O