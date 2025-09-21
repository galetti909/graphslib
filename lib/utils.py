def decrement_input_nodes_index(nodes_index: int | list[int] | tuple[int]) -> None:
    if isinstance(nodes_index, (list, tuple)):
        for i in range(len(nodes_index)):
            nodes_index[i] -= 1
        return nodes_index  
    return nodes_index - 1

def increment_output_nodes_index(nodes_index: int | list[int] | tuple[int]) -> None:
    if isinstance(nodes_index, (list, tuple)):
        for i in range(len(nodes_index)):
            nodes_index[i] += 1
        return nodes_index
    return nodes_index + 1