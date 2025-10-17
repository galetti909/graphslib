class IndexedMinHeap:
    def __init__(self):
        # Initializes the heap and the position map.
        self.heap = []
        self.position = {} # Maps: node -> index_in_heap

    def _swap(self, i: int, j: int):
        #Swaps two elements in the heap and updates their positions in the map.
        node_i = self.heap[i][1]
        node_j = self.heap[j][1]
        
        self.position[node_i], self.position[node_j] = j, i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _sift_up(self, i: int):
        # Moves an element up the tree to maintain the heap property.
        parent_index = (i - 1) // 2
        while i > 0 and self.heap[i][0] < self.heap[parent_index][0]:
            self._swap(i, parent_index)
            i = parent_index
            parent_index = (i - 1) // 2
    
    def _sift_down(self, i: int):
        # Moves an element down the tree to maintain the heap property.
        min_index = i
        left_child = 2 * i + 1
        right_child = 2 * i + 2
        
        # Find the smallest among the node and its children
        if left_child < len(self.heap) and self.heap[left_child][0] < self.heap[min_index][0]:
            min_index = left_child
        if right_child < len(self.heap) and self.heap[right_child][0] < self.heap[min_index][0]:
            min_index = right_child
            
        if i != min_index:
            self._swap(i, min_index)
            self._sift_down(min_index)

    def is_empty(self) -> bool:
        # Checks if the heap is empty.
        return len(self.heap) == 0

    def push(self, node: int, distance: float):
        # Adds a new node to the heap.
        if node in self.position:
            return

        self.heap.append((distance, node))
        index = len(self.heap) - 1
        self.position[node] = index
        self._sift_up(index)
    
    def pop_min(self) -> tuple[float, int]:
        # Removes and returns the item with the smallest distance (the root).
        if self.is_empty():
            raise IndexError("pop from an empty heap")

        min_item = self.heap[0]
        del self.position[min_item[1]]

        if len(self.heap) == 1:
            self.heap.pop()
            return min_item

        # Move the last item to the root and sift down
        last_item = self.heap.pop()
        self.heap[0] = last_item
        self.position[last_item[1]] = 0
        self._sift_down(0)
        
        return min_item

    def decrease_key(self, node: int, new_distance: float):
        # Updates a node's distance and adjusts its position in the heap.
        if node not in self.position:
            return

        index = self.position[node]
        if new_distance < self.heap[index][0]:
            self.heap[index] = (new_distance, node)
            # Since priority increased (distance decreased), the node must move up.
            self._sift_up(index)

    def __contains__(self, node: int) -> bool:
        # Allows for 'node in heap' checks.
        return node in self.position