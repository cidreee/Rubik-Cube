import numpy as np
from queue import Queue
import random
from queue import PriorityQueue
from copy import deepcopy

class Heuristics:
    @staticmethod
    def hamming_distance(node_a, node_b):
        cube_a = node_a.cube.flatten()
        cube_b = node_b.cube.flatten()

        return np.count_nonzero(cube_a != cube_b)
    
    @staticmethod
    def heuristic3(node1, node2):
        p = len(node1.path)
        return p

    @staticmethod
    def cruz(node1, node2):
        # Cara 0
        sum = 15
        for i in range(5):
            faceACT = node1.cube[i]
            faceMETA = node2.cube[i]
            # Línea horizontal central de la cara 
            horizontal_lineACT = faceACT[1].flatten()
            horizontal_lineMETA = faceMETA[1].flatten()
            # Línea vertical central de la cara 
            vertical_lineACT = [faceACT[j][1] for j in range(3)]
            vertical_lineMETA = [faceMETA[j][1] for j in range(3)]
            if(np.all(vertical_lineACT == vertical_lineMETA) and np.all(horizontal_lineACT == horizontal_lineMETA)):
                sum -= 2
            elif np.all(vertical_lineACT == vertical_lineMETA):
                sum -= 1
            elif np.all(horizontal_lineACT == horizontal_lineMETA):
                sum -= 1
        return sum
    

    @staticmethod
    def esquinas(node1, node2):
        sum = 15
        for i in range(5):  # Para cada cara
            face1 = node1.cube[i]
            face2 = node2.cube[i]
            
            # Obtener las esquinas de la cara actual
            corners1 = [(0, 0), (0, 2), (2, 0), (2, 2)]

            
            for corner1 in corners1:
                corner_value1 = face1[corner1[0], corner1[1]]
                corner_value2 = face2[corner1[0], corner1[1]]
                if np.all(corner_value1 == corner_value2):
                    sum -= 0.4

        return sum
    

class Node:
    def __init__(self, cube):
        self.cube = cube 
        self.path = []
    
    def is_cube_solved(self, resolved_cube):
        return np.array_equal(self.cube, resolved_cube)
    
class Node_A_Star:
    def __init__(self, cube):
        self.cube = cube
        self.path = []
        self.distance = 0
        self.total = 0
        self.heuristic_value = -1
    
    def is_cube_solved(self, resolved_cube):
        return np.array_equal(self.cube, resolved_cube)
    
    def calculate_heuristic(self, heuristic_function, target):
        return heuristic_function(self, target)

    def __lt__(self, other):
        if not isinstance(other, Node_A_Star):
            return False
        return self.total < other.total
        

class HeuristicNode:
    def __init__(self, cube):
        self.cube = cube

        self.heuristic_value = -1
        self.path =  []
    
    def calculate_heuristic(self, heuristic_function, target):
        return heuristic_function(self, target)
    
    def is_cube_solved(self, resolved_cube):
        return np.array_equal(self.cube, resolved_cube)
    
    '''
    def __eq__(self, other):
        if not isinstance(other, HeuristicNode):
            return False
        return np.array_equal(self.cube, other.cube)
    '''
    def __lt__(self, other):
        if not isinstance(other, HeuristicNode):
            return False
        return self.heuristic_value < other.heuristic_value
    '''
    def __gt__(self, other):
        if not isinstance(other, HeuristicNode):
            return False    
        return self.heuristic_value > other.heuristic_value
        '''
    
class RubikCube:
    resolved_cube = np.array([
        [[0] * 3 for _ in range(3)],  # Face 0 (Left)
        [[1] * 3 for _ in range(3)],  # Face 1 (Front)
        [[2] * 3 for _ in range(3)],  # Face 2 (Up)
        [[3] * 3 for _ in range(3)],  # Face 3 (Down)
        [[4] * 3 for _ in range(3)],  # Face 4 (Right)
        [[5] * 3 for _ in range(3)],  # Face 5 (Back)
    ])

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

        self.movements_opuestos = {
            'R': 'L',
            'L': 'R',
            'U': 'U1',
            'R1': 'L1',
            'L1': 'R1',
            'U1': 'U',
            'D': 'D1',
            'F': 'F1',
            'B': 'B1',
            'D1': 'D',
            'F1': 'F',
            'B1': 'B'
        }

    
    def __rotate_face(self, face, clockwise=True):
        if clockwise:
            temp = np.copy(self.cube[face])
            temp_rotated = np.zeros((3, 3), dtype=int)
            for i in range(3):
                for j in range(3):
                    temp_rotated[i][j] = temp[2 - j][i]
            self.cube[face] = temp_rotated

        else:
            temp = np.copy(self.cube[face])
            temp_rotated = np.zeros((3, 3), dtype=int)
            for i in range(3):
                for j in range(3):
                    temp_rotated[i][j] = temp[j][2 - i]
            self.cube[face] = temp_rotated
    
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
    
    # Funcion shuffle para revolver el cubo
    def shuffle(self, N):
        for _ in range(N):
            movement = random.randint(0, 11)
            if movement == 0:
                self.horizontal_0_left()
            elif movement == 1:
                self.horizontal_0_right()
            elif movement == 2:
                self.horizontal_2_left()
            elif movement == 3:
                self.horizontal_2_right()
            elif movement == 4:
                self.vertical_0_down()
            elif movement == 5:
                self.vertical_0_up()
            elif movement == 6:
                self.vertical_2_down()
            elif movement == 7:
                self.vertical_2_up()
            elif movement == 8:
                self.z_back_left()
            elif movement == 9:
                self.z_back_right()
            elif movement == 10:
                self.z_front_left()
            elif movement == 11:
                self.z_front_right()  
            
            print(movement)

    def move_list(self, moves_list):
        moves = moves_list.split()
        for move in moves:
            if move in self.movements:
                self.movements[move]()

    # Funcion shuffle para revolver el cubo
    def shuffle_unrepeat(self, N):
        prev_movement = None
        for _ in range(N):
            movement_key = random.choice(list(self.movements.keys()))
            movement = self.movements[movement_key]

            # Verificar si el movimiento actual es opuesto al movimiento anterior
            if prev_movement is not None and self.movements_opuestos[prev_movement] == movement_key:
                while self.movements_opuestos[prev_movement] == movement_key:
                    movement_key = random.choice(list(self.movements.keys()))
                    movement = self.movements[movement_key]

            movement()
            prev_movement = movement_key
    
    
class RubikSolver:

    INF = float("inf")

    def __init__(self):
        self.cube = RubikCube()

    # BFS sin heuristica
    def breadth_first_search(self):
        node = Node(np.copy(self.cube.cube))
        visited = set()
        q = Queue()
        q.put(node)
        visited.add(tuple(node.cube.flatten()))

        while not q.empty():
            current_node = q.get()

            if current_node.is_cube_solved(RubikCube.resolved_cube):
                return current_node.path
 
            for move in self.cube.movements.keys():
                next_cube = np.copy(current_node.cube)
                self.cube.cube = next_cube
                self.cube.movements[move]()

                if tuple(self.cube.cube.flatten()) not in visited:
                    next_node = Node(np.copy(self.cube.cube))
                    next_node.path = current_node.path + [move]
                    q.put(next_node)
                    visited.add(tuple(next_node.cube.flatten()))
    
    # BFS con heuristica
    def best_first_search(self, heuristic):
        node = HeuristicNode(np.copy(self.cube.cube))  
        target_node = HeuristicNode(RubikCube.resolved_cube)
        node.heuristic_value = node.calculate_heuristic(heuristic, target_node)
        visited = set()
        q = PriorityQueue()
        q.put(node)
        visited.add(tuple(node.cube.flatten()))
        
        while not q.empty():
            current_node = q.get()

            if current_node.is_cube_solved(RubikCube.resolved_cube):
                return current_node.path
            
            for move in self.cube.movements.keys():
                next_cube = np.copy(current_node.cube)
                self.cube.cube = next_cube
                self.cube.movements[move]()

                if tuple(self.cube.cube.flatten()) not in visited:
                    next_node = HeuristicNode(np.copy(self.cube.cube))
                    next_node.path = current_node.path + [move]
                    next_node.heuristic_value = next_node.calculate_heuristic(heuristic, target_node)
                    q.put(next_node)
                    visited.add(tuple(next_node.cube.flatten()))
                

    def a_star(self, heuristic):
        target_node = Node_A_Star(RubikCube.resolved_cube)
        node = Node_A_Star(np.copy(self.cube.cube))  
        node.heuristic_value = node.calculate_heuristic(heuristic, target_node)
        visited = set()
        q = PriorityQueue()
        q.put(node)
        visited.add(tuple(node.cube.flatten()))
        
        while not q.empty():
            current_node = q.get()
            visited.add(tuple(current_node.cube.flatten()))

            if current_node.is_cube_solved(RubikCube.resolved_cube):
                return current_node.path
            
            for move in self.cube.movements.keys():
                next_cube = np.copy(current_node.cube)
                self.cube.cube = next_cube
                self.cube.movements[move]()
                
                if tuple(self.cube.cube.flatten()) not in visited:
                    next_node = Node_A_Star(np.copy(self.cube.cube))
                    next_node.path = current_node.path + [move]
                    next_node.heuristic_value = next_node.calculate_heuristic(heuristic, target_node)
                    next_node.distance = current_node.distance + 1  # Incrementar la distancia
                    next_node.total = next_node.heuristic_value + next_node.distance  # Recalcular el total
                    q.put(next_node)
    
    def ida_star(self, heuristic):
        target_node = Node_A_Star(RubikCube.resolved_cube)
        node = Node_A_Star(np.copy(self.cube.cube))
        node.heuristic_value = node.calculate_heuristic(heuristic, target_node)
        threshold = node.heuristic_value
        path = []

        while True:
            result, new_threshold = self.ida_star_search(node, target_node, threshold, path, heuristic)
            if result == 'FOUND':
                return path
            if result == float('inf'):
                return None
            threshold = new_threshold

    def ida_star_search(self, node, target_node, threshold, path, heuristic):
        visited = set()
        stack = [(node, 0)]
        visited.add(tuple(node.cube.flatten()))
        min_distance = float('inf')

        while stack:
            current_node, g_cost = stack.pop()
            f_cost = g_cost + current_node.heuristic_value

            if f_cost > threshold:
                min_distance = min(min_distance, f_cost)
                continue

            if current_node.is_cube_solved(target_node.cube):
                path[:] = current_node.path
                return 'FOUND', threshold

            for move in self.cube.movements.keys():
                next_cube = np.copy(current_node.cube)
                self.cube.cube = next_cube
                self.cube.movements[move]()

                if tuple(self.cube.cube.flatten()) not in visited:
                    next_node = Node_A_Star(np.copy(self.cube.cube))
                    next_node.path = current_node.path + [move]
                    next_node.heuristic_value = next_node.calculate_heuristic(heuristic, target_node)
                    stack.append((next_node, g_cost + 1))
                    visited.add(tuple(self.cube.cube.flatten()))

        return min_distance, min_distance


    
rubik = RubikSolver()
rubik.cube.move_list("U1 R1 D D R U")
#rubik.cube.shuffle(10)  # Revuelve el cubo con movimientos aleatorios
print(rubik.cube.cube)
print('\n')
solution = rubik.ida_star(Heuristics.esquinas)
print(solution)
