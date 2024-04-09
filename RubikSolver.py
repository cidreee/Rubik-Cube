    # Funcion A* 
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
                    next_node.heuristic_value = next_node.calculate_heuristic(heuristic, target_node)
                    next_node.path = current_node.path + [move]
                    next_node.distance = current_node.distance + 1  # Incrementar la distancia
                    next_node.total = next_node.heuristic_value + next_node.distance  # Recalcular el total
                    q.put(next_node)
