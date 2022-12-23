class Rock:
    height: int
    width: int
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def canMoveDown(self, room, coordinates) -> bool:
        return False

    def canMoveLeft(self, room, coordinates) -> bool:
        return False

    def canMoveRight(self, room, coordinates) -> bool:
        return False

    def stop(self, room, coordinates) -> None:
        pass
        
class Line(Rock):
    ''' #### '''
    def __init__(self):
        super().__init__(1, 4)

    def canMoveDown(self, room, coordinates) -> bool:
        x,y = coordinates
        for xCheck in range(self.width):
            if room[y-self.height][x + xCheck] != '.':
                return False
        return True

    def canMoveLeft(self, room, coordinates) -> bool:
        x,y = coordinates
        return room[y][x - 1] == '.'

    def canMoveRight(self, room, coordinates) -> bool:
        x,y = coordinates
        return room[y][x + self.width] == '.'

    def stop(self, room, coordinates) -> None:
        x,y = coordinates
        for xPos in range(self.width):
            room[y][x + xPos] = 'a'
        

class Plus(Rock):
    '''
      #
     ###
      #
    '''
    def __init__(self):
        super().__init__(3, 3)
        
    def canMoveDown(self, room, coordinates) -> bool:
        x,y = coordinates
        for xCheck, yCheck in [(0,2), (1,3), (2,2)]:
            if room[y - yCheck][x + xCheck] != '.':
                return False
        return True

    def canMoveLeft(self, room, coordinates) -> bool:
        x,y = coordinates
        for xCheck, yCheck in [(0,0), (-1,1), (0,2)]:
            if room[y - yCheck][x + xCheck] != '.':
                return False
        return True

    def canMoveRight(self, room, coordinates) -> bool:
        x,y = coordinates
        for xCheck, yCheck in [(2,0), (3,1), (2,2)]:
            if room[y - yCheck][x + xCheck] != '.':
                return False
        return True
        
    def stop(self, room, coordinates) -> None:
        x,y = coordinates
        for xPos in range(self.width):
            room[y - 1][x + xPos] = 'b'
            
        for yPos in range(self.height):
            room[y - yPos][x + 1] = 'b'

class Corner(Rock):
    '''
       #
       #
     ###
    '''
    def __init__(self):
        super().__init__(3, 3)

    def canMoveDown(self, room, coordinates):
        x,y = coordinates
        for xCheck in range(self.width):
            if room[y-self.height][x + xCheck] != '.':
                return False
        return True

    def canMoveLeft(self, room, coordinates):
        x,y = coordinates
        for xCheck, yCheck in [(1,0), (1,1), (-1,2)]:
            if room[y - yCheck][x + xCheck] != '.':
                return False
        return True

    def canMoveRight(self, room, coordinates):
        x,y = coordinates
        for yCheck in range(self.height):
            if room[y - yCheck][x + self.width] != '.':
                return False
        return True

    def stop(self, room, coordinates):
        x,y = coordinates
        for xPos in range(self.width):
            room[y - 2][x + xPos] = 'c'
            
        for yPos in range(self.height):
            room[y - yPos][x + 2] = 'c'

class Column(Rock):
    '''
    #
    #
    #
    #
    '''
    def __init__(self):
        super().__init__(4, 1)

    def canMoveDown(self, room, coordinates):
        x,y = coordinates
        return room[y-self.height][x] == '.'

    def canMoveLeft(self, room, coordinates):
        x,y = coordinates
        for yCheck in range(self.height):
            if room[y - yCheck][x - 1] != '.':
                return False
        return True

    def canMoveRight(self, room, coordinates):
        x,y = coordinates
        for yCheck in range(self.height):
            if room[y - yCheck][x + self.width] != '.':
                return False
        return True

    def stop(self, room, coordinates):
        x,y = coordinates
        for yPos in range(self.height):
            room[y - yPos][x] = 'd'

class Box(Rock):
    '''
    ##
    ##
    '''
    def __init__(self):
        super().__init__(2, 2)

    def canMoveDown(self, room, coordinates):
        x,y = coordinates
        for xCheck in range(self.width):
            if room[y - self.height][x + xCheck] != '.':
                return False
        return True

    def canMoveLeft(self, room, coordinates):
        x,y = coordinates
        for yCheck in range(self.height):
            if room[y - yCheck][x - 1] != '.':
                return False
        return True
        
    def canMoveRight(self, room, coordinates):
        x,y = coordinates
        for yCheck in range(self.height):
            if room[y - yCheck][x + self.width] != '.':
                return False
        return True

    def stop(self, room, coordinates):
        x,y = coordinates
        for xPos in range(self.width):
            for yPos in range(self.height):
                room[y - yPos][x + xPos] = 'e'