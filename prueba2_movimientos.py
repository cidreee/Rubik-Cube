import numpy as np
from queue import Queue
import random

class Node:
    def __init__(self, cube):
        self.cube = cube 
        self.path = []


class RubikCube:
    def __init__(self):
        # Arreglo tridimensional 
        self.cube = np.array([
            [[0] * 3 for _ in range(3)],  # Face 0 (Left)
            [[1] * 3 for _ in range(3)],  # Face 1 (Front)
            [[2] * 3 for _ in range(3)],  # Face 2 (Up)
            [[3] * 3 for _ in range(3)],  # Face 3 (Down)
            [[4] * 3 for _ in range(3)],  # Face 4 (Right)
            [[5] * 3 for _ in range(3)],  # Face 5 (Back)
        ])  

        self.initial_state = np.copy(self.cube)

        self.movements = {
            'R' : self.vertical_2_up, 
            'L' : self.vertical_0_down,
            'U' : self.horizontal_0_left,
            'R1' : self.vertical_2_down,
            'L1' : self.vertical_0_up,
            'U1' : self.horizontal_0_right,
            'D' : self.horizontal_2_right,
            'F' : self.z_front_right,
            'B' : self.z_back_left,
            'D1' : self.horizontal_2_left,
            'F1' : self.z_front_left,
            'B1' : self.z_back_right
        }

    def __rotate_face(self, face, clockwise=True):
        if clockwise:
            self.cube[face] = np.rot90(self.cube[face], -1)
        else:
            self.cube[face] = np.rot90(self.cube[face])
    
    # Funciones priv para movimientos
            
    # Horizontales
    # Derecha
    def __horizontal_right(self, row, face_rotate):
        if face_rotate == 2:
            self.__rotate_face(face_rotate, clockwise= False)
        elif face_rotate == 3:
            self.__rotate_face(face_rotate, clockwise= True)
        temp = np.copy(self.cube[0])
        self.cube[0][row] = self.cube[5][row]
        self.cube[5][row] = self.cube[4][row]
        self.cube[4][row] = self.cube[1][row]
        self.cube[1][row] = temp[row][::]
    
    # Movimientos verticales
    # Arriba
    def __vertical_up(self, col, face_rotate):
        if face_rotate == 0:
            self.__rotate_face(face_rotate, clockwise= False)
        elif face_rotate == 4:
            self.__rotate_face(face_rotate, clockwise= True)
        temp = np.copy(self.cube[1])
        self.cube[1][:, col] = self.cube[3][:, col]
        if col == 2:      
            self.cube[3][:, col] = self.cube[5][:, 0][::-1]
            self.cube[5][:, 0] = self.cube[2][:, col][::-1]
        elif col == 0:
            self.cube[3][:, col] = self.cube[5][:, 2][:: -1]
            self.cube[5][:, 2] = self.cube[2][:, col][::-1]
        self.cube[2][:, col] = temp[:, col]
    
    # Movimientos en z
    # Derecha
    def __z_right(self, z_col, face_rotate):
        if face_rotate == 1:
            self.__rotate_face(face_rotate, clockwise= True)
        elif face_rotate == 5:
            self.__rotate_face(face_rotate, clockwise= False)

        temp = np.copy(self.cube[2])
        if z_col == 0:
            self.cube[2][z_col] = self.cube[0][:, z_col][::-1]
            self.cube[0][:,z_col] = self.cube[3][2]
            self.cube[3][2] = self.cube[4][:, 2][::-1]
            self.cube[4][:, 2] = temp[z_col][::]    

        elif z_col == 2:
            self.cube[2][z_col] = self.cube[0][:, z_col][::-1]
            self.cube[0][:,z_col] = self.cube[3][0]
            self.cube[3][0] = self.cube[4][:, 0][::-1]
            self.cube[4][:, 0] = temp[z_col][::]    


    # --------------------- MOVIMIENTOS ----------------------------------

    # Horizontales
    def horizontal_0_right(self, N = 1):
        for _ in range(N):
            self.__horizontal_right(0, 2)
        return self.cube
    
    def horizontal_2_right(self, N = 1):
        for _ in range(N):
            self.__horizontal_right(2, 3)
        return self.cube
    
    def horizontal_0_left(self, N = 1):
        for _ in range(N):
            self.__horizontal_right(0, 2)
            self.__horizontal_right(0, 2)
            self.__horizontal_right(0, 2)
        return self.cube

    def horizontal_2_left(self, N = 1):
        for _ in range(N):
            self.__horizontal_right(2, 3)
            self.__horizontal_right(2, 3)
            self.__horizontal_right(2, 3)
        return self.cube

    # Verticales
    def vertical_0_up(self, N = 1):
        for _ in range (N):
            self.__vertical_up(0, 0)
        return self.cube
    
    def vertical_2_up(self, N = 1):
        for _ in range (N):
            self.__vertical_up(2, 4)
        return self.cube
    
    def vertical_0_down(self, N=1):
        for _ in range(N):
            self.__vertical_up(0, 0)
            self.__vertical_up(0, 0)
            self.__vertical_up(0, 0)
        return self.cube

    def vertical_2_down(self, N = 1):
        for _ in range (N):
            self.__vertical_up(2, 4)
            self.__vertical_up(2, 4)
            self.__vertical_up(2, 4)
        return self.cube
    
    # En z
    def z_front_right(self, N=1):
        for _ in range(N):
            self.__z_right(2, 1)
        return self.cube
    
    def z_back_right(self, N=1):
        for _ in range(N):
            self.__z_right(0, 5)
        return self.cube
    
    def z_front_left(self, N=1):
        for _ in range(N):
            self.__z_right(2, 1)
            self.__z_right(2, 1)
            self.__z_right(2, 1)
        return self.cube
    
    def z_back_left(self, N=1):
        for _ in range(N):
            self.__z_right(0, 5)
            self.__z_right(0, 5)
            self.__z_right(0, 5)
        return self.cube

    def is_solved(self):
        for i in range (6):
            if not np.array_equal(self.cube[i], self.initial_state[i]):
                return False
        
        return True


class RubikSolver:
    def __init__(self):
        self.cube = RubikCube()
    
    def beradth_first_search(self, node):
        visited = set()
        q = Queue()
        q.put(node)
        visited.add(node)

        while not q.empty():
            current_node = q.get()

            if self.cube.is_solved():
                return current_node.path
            
            for move in self.cube.movements.keys():
                next_cube = RubikCube()
            
            



    
    

    
rubik = RubikSolver()

print("Estado inicial:")
print(rubik.cube)
print("Estado despues:")
rubik.z_back_left()
print(rubik.cube)
