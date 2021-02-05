import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
import networkx as nx

def display_graph(path):
    G = nx.Graph()
    G.add_edges_from(path)
    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=True)
    plt.show()

def uniform_cost_search(edges, initial_node, goal_node):
    priority_queue = pd.DataFrame([['R',initial_node,0]], columns=['from','to','weights'])
    traversed = pd.DataFrame(columns=['from','to','weights'])
    closed = []
    parent = { initial_node:'R' }
    success = False
    while not priority_queue.empty:
        from_node = priority_queue.iloc[0]['from']
        current_node =  priority_queue.iloc[0]['to']
        current_weight = priority_queue.iloc[0]['weights']
        priority_queue = priority_queue.iloc[1:]
        if current_node not in closed:
            parent[current_node] = from_node
            traversed = traversed.append(pd.DataFrame([[from_node, current_node, current_weight]], columns=['from','to','weights']))
            if current_node == goal_node:
                success = True
                break
            closed.append(current_node)
            next_rows = edges.loc[(edges['from']==current_node) |(edges['to']==current_node)]
            next_rows = next_rows.apply(lambda row: reversal_node(row, current_node, current_weight), axis=1)
            next_rows = next_rows[~next_rows.to.isin(closed)]
            priority_queue = priority_queue.append(next_rows)
            priority_queue = priority_queue.sort_values(by=['weights']).reset_index(drop=True)
    shortest_path = [current_node]
    while current_node != 'R':
        parent_node = traversed.loc[(traversed['to']==current_node)].iloc[0]['from']
        shortest_path.insert(0,parent_node)
        current_node = parent_node
    search_space = []
    for row in traversed.iterrows():
        search_space.append((row[1]['from'],row[1]['to']))
    display_graph(search_space)
    total_weight = traversed.loc[(traversed['to']==goal_node)].iloc[0]['weights']
    return { "success":success, "path": shortest_path[1:], "weights": total_weight}


if __name__ == '__main__':
    edges = pd.read_csv('Graph.csv')
    initial_node = 'A'
    goal_node = 'M'
    print(uniform_cost_search(edges, initial_node, goal_node))
