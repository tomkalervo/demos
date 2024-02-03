import networkx as nx
import matplotlib.pyplot as plt

def generate_star_shaped_graph(num_nodes = 10, center = 100):
    nodes = []
    nodes_bottom = []
    nodes_top = [(0,center)]
    x_list = [x for x in range(center*2//num_nodes,center*2,center*2//num_nodes)]

    k = 0
    for i,x in enumerate(x_list):
        k = 1 - k
        if x <= center:
            nodes_top.append((x,center+x-(k*(x//2))))
            nodes_bottom.append((x,center-x+(k*(x//2))))
        else:
            nodes_top.append((x,2*center+(center-x)-(k*((2*center-x)//2))))
            nodes_bottom.append((x,x-center+(k*((2*center-x)//2))))
    nodes.extend(nodes_top)
    nodes.append((2*center,center))
    nodes.extend(nodes_bottom[::-1])

    return nodes

def calculate_cartesian_distance(point1, point2):
    """Calculates the cartesian distance between to points in the plane.
    Distance between point1(x1,y1) and point2(x2,y2) is the square root of ( (x2-x1)^2 + (y2-y1)^2 ) 
    
    Args:
        point1 (tuple): A tuple representing the position of point1 in the plane as (x1, y1).
        point2 (tuple): A tuple representing the position of point2 in the plane as (x2, y2).

    Returns:
        float: The cartesian distance between point1 and point2.
    """
    x1, y1 = point1
    x2, y2 = point2
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance

def display_edge_distances(graph):
    for edge in graph.edges():
        distance = calculate_cartesian_distance(edge[0], edge[1])
        x_mid = (edge[0][0] + edge[1][0]) / 2
        y_mid = (edge[0][1] + edge[1][1]) / 2
        plt.text(x_mid, y_mid, f'{distance:.2f}', fontsize=8, color='red', ha='center', va='center')

def print_total_distance(graph):
    total_distance = sum(calculate_cartesian_distance(edge[0], edge[1]) for edge in graph.edges())
    print(f'Total Distance: {total_distance:.2f}')
    
def plot_ordered_graph(vertices):
    # Create a directed graph
    G = nx.DiGraph()

    # Add vertices to the graph
    G.add_nodes_from(vertices)

    # Add edges based on the order in the list
    edges = [(vertices[i], vertices[i + 1]) for i in range(len(vertices) - 1)]
    
    # Add an edge from the last vertex to the first vertex
    edges.append((vertices[-1], vertices[0]))
    
    G.add_edges_from(edges)
    
    # Plot the graph
    pos = {v: (v[0], v[1]) for v in vertices}  # Use the (x, y) coordinates as positions
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=500, node_color='skyblue', font_size=6, edge_color='gray', width=1.5)
    
    # Display edge distances on the plot
    display_edge_distances(G)

    # Print the total distance over the entire graph
    print_total_distance(G)

    # Show the plot
    plt.show()

def plot_complete_graph(vertices):
    """Plots a complete graph with edges to all other vertices.

    Args:
        vertices (list): A list of vertices in the form (x, y).
    """
    # Create a complete graph
    G = nx.complete_graph(len(vertices))

    # Assign the specified vertices to the nodes
    mapping = {i: vertices[i] for i in range(len(vertices))}
    G = nx.relabel_nodes(G, mapping)

    # Plot the complete graph
    pos = {v: (v[0], v[1]) for v in vertices}
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=500, node_color='skyblue', font_size=6,
            edge_color='gray', width=1)

    # Show the plot
    plt.show()