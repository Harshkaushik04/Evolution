import copy
import json
from utils import hexadecimal_to_binary
import networkx as nx
from graph_data_structure import edges_list,neurons_dict,neuron,brain
import matplotlib.pyplot as plt
import os
import numpy as np
import random
from numba import njit
from pygame_env import player,circle
from hashing_encoding_colors import encode_players_with_same_genes
from networkx.drawing.nx_pylab import draw_networkx_nodes, draw_networkx_labels
from matplotlib.patches import FancyArrowPatch
import pygame

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def directions_dict_generator(population):
    directions_dict={}
    choices=['north','south','east','west']
    probs=np.ones(4)/4
    for i in range(population):
        directions_dict['player'+str(i)]=np.random.choice(choices,p=probs)
    return directions_dict

#print(directions_dict_generator(20,0))
def genes_hexa_dict_generator(population,seed,genome_length):
    genes_hexa_dict={}
    choices=[1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f']
    probs=np.ones(15)/15
    for i in range(population):
        np.random.seed(seed+i)
        genes_hexa_dict['player' + str(i)] = []
        for j in range(genome_length):
            genes_hexa_dict['player'+str(i)].append(''.join(np.random.choice(choices, size=8, p=probs)))
    return genes_hexa_dict
#print(genes_hexa_dict_generator(population=20,seed=0,genome_length=4))

def co_ordinates_initialize_dict(env_width,env_height,population,size_parameter):
    co_ordinates_dict={}
    used_co_ordinates=[]
    rect_co_ordinates_dict={}
    for i in range(population):
        rect_co_ordinates_dict['player'+str(i)]=[]
        while True:
            x=random.randint(3*size_parameter//2+1,env_width-3*size_parameter//2-1)
            y=random.randint(3*size_parameter//2+1,env_height-3*size_parameter//2-1)
            if [x,y] not in used_co_ordinates:
                for x_rect in range(x-3*size_parameter//2,x+3*size_parameter//2):
                    for y_rect in range(y-3*size_parameter//2,y+3*size_parameter//2):
                        used_co_ordinates.append([x_rect,y_rect])
                        rect_co_ordinates_dict['player'+str(i)].append([x_rect,y_rect])
                co_ordinates_dict['player'+str(i)]=[x,y]
                break
    return co_ordinates_dict,rect_co_ordinates_dict

# dict,rect_dict=co_ordinates_initialize_dict(1200,800,2000,0,3)

# 1:source type
# 2-8:source ID
# 9:sink type
# 10-16:sink ID
# 17-32 : connection weight

#converts gene(8 digit hexadecimal number) to unprocessed nodes data and weights
def gene_to_unprocessed_data(hex_value):
    binary=hexadecimal_to_binary(hex_value, binary_length=32) #binary string
    gene_data={}
    gene_data['source_type']=int(binary[0])
    gene_data['source_ID']=int(binary[2:9])
    gene_data['sink_type'] = int(binary[9])
    gene_data['sink_ID'] = int(binary[10:17])
    gene_data['connection_weight']  = int(binary[17:32], 2) - (1 << 16) if binary[17:32][0] == '1' else int(binary[17:32], 2)
 #binary to integer
    return gene_data
#assuming keys of gene_dict is 'gene_1','gene_2',.....

'''
all 5 characteristics:
1. source type: at 0,its sensory neuron and at 1,its internal neuron
2. source id: if source type is sensory neuron then total number of different types
of sensory neurons are num_sensory and hence we take remainder by dividing it from
gene_data['source_ID']
3. sink type: at 0,its output neuron and at 1,its internal neuron
4. sink id:same logic as source id
5. connection weights: normally it can give from about -32k to +32k so we generally keep
normalization factor to be about 8k
'''

def unprocessed_data_to_processed_data(gene_data,num_sensory,num_internal,num_output,normalization_factor=8000):
    if gene_data['source_type']==0:
        gene_data['source_type']='sensory_neuron'
        gene_data['source_ID'] %= num_sensory
        gene_data['source_ID']='S'+str(gene_data['source_ID'])
    elif gene_data['source_type']==1:
        gene_data['source_type']='internal_neuron'
        gene_data['source_ID'] %= num_internal
        gene_data['source_ID'] = 'I' + str(gene_data['source_ID'])

    if gene_data['sink_type']==0:
        gene_data['sink_type']='output_neuron'
        gene_data['sink_ID'] %= num_output
        gene_data['sink_ID'] = 'O' + str(gene_data['sink_ID'])
    elif gene_data['sink_type']==1:
        gene_data['sink_type']='internal_neuron'
        gene_data['sink_ID'] %= num_internal
        gene_data['sink_ID'] = 'I' + str(gene_data['sink_ID'])
    gene_data['connection_weight']/=normalization_factor
    return gene_data


#genes to neural network
def processed_data_to_brain(genes_hexa_list,genes_list,activation_inputs_dict,num_neurons):
    #print('last_go_genes_list:',genes_list)
    for gene in genes_list[:]:
        #print(gene['sink_ID'],'  ',gene['source_ID'])
        #print("======================================")
        if gene['sink_ID']==gene['source_ID']:
            genes_list.remove(gene)
    edge_list,input_neurons_list,output_neurons_list=edges_list(genes_list)
    neurons_dictionary,incoming_exhausted_list,useless_neurons_list,genes_list,edge_list=neurons_dict(genes_list,activation_inputs_dict,num_neurons,edge_list)
    #print('wow_genes_list:',genes_list)
    final_brain=brain(genes_hexa_list,genes_list,edge_list,neurons_dictionary,input_neurons_list,output_neurons_list,incoming_exhausted_list)
    #final_brain.forward_propagation()
    #print('last_go_self.genes_list:',final_brain.genes_list)
    return final_brain

# def graph_visuals(genes_list):
#     graph=nx.MultiDiGraph()
#     counter=0
#     for gene in genes_list:
#         graph.add_edge(gene['source_ID'],gene['sink_ID'],key=counter)
#         counter+=1
#     nx.draw_circular(graph,with_labels=True)
#     plt.show()

# def graph_visuals(genes_list):
#     graph = nx.MultiDiGraph()
#     counter = 0
#
#     # Add edges with connection weights
#     for gene in genes_list:
#         source = gene['source_ID']
#         sink = gene['sink_ID']
#         weight = gene['connection_weight']
#         color = 'green' if weight > 0 else 'red'
#         graph.add_edge(source, sink, key=counter, weight=weight, color=color)
#         counter += 1
#
#     # Get edge colors
#     edge_colors = [graph[u][v][k]['color'] for u, v, k in graph.edges(keys=True)]
#
#     # Draw the graph with curved arrows
#     pos = nx.circular_layout(graph)  # Use a circular layout for positioning nodes
#     arc_rad = 0.1  # Radius of curvature for the edges
#
#     # Draw the nodes
#     nx.draw_networkx_nodes(graph, pos, node_size=700)
#
#     # Draw the edges with curvature and colors
#     for (u, v, k, d) in graph.edges(data=True, keys=True):
#         edge_color = d['color']
#         connection_style = 'arc3,rad={}'.format(arc_rad)
#         nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], edge_color=edge_color, connectionstyle=connection_style)
#
#     # Draw labels
#     nx.draw_networkx_labels(graph, pos, font_size=12, font_family="sans-serif")
#
#     plt.title("Gene Interaction Network")
#     plt.show()

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from networkx.drawing.nx_pylab import draw_networkx_nodes, draw_networkx_labels

def graph_visuals(genes_list):
    graph = nx.MultiDiGraph()
    counter = 0

    # Add edges with connection weights
    for gene in genes_list:
        source = gene['source_ID']
        sink = gene['sink_ID']
        weight = gene['connection_weight']
        color = 'green' if weight > 0 else 'red'
        graph.add_edge(source, sink, key=counter, weight=weight, color=color)
        counter += 1

    # Draw the graph
    pos = nx.circular_layout(graph)  # Use a circular layout for positioning nodes
    fig, ax = plt.subplots()

    # Draw the nodes and labels
    draw_networkx_nodes(graph, pos, node_size=700, ax=ax)
    draw_networkx_labels(graph, pos, font_size=12, font_family="sans-serif", ax=ax)

    # Draw the curved edges with colors
    for (u, v, k, d) in graph.edges(data=True, keys=True):
        rad = 0.25 if u != v else 0.1  # Self-loops need a smaller curvature
        color = d['color']
        arrow = FancyArrowPatch(
            posA=pos[u], posB=pos[v],
            connectionstyle=f"arc3,rad={rad}",
            arrowstyle='-|>',
            color=color,
            mutation_scale=20,
            lw=1.5,
            shrinkA=10,  # Shrink start of the arrow away from the node
            shrinkB=10   # Shrink end of the arrow away from the node
        )
        ax.add_patch(arrow)

    plt.title("Gene Interaction Network")
    plt.axis('off')  # Turn off the axis
    plt.show()


def genes_to_brain(genes_hexa_list,activation_inputs_dict,num_neurons,show_graph=False):
    genes_list=[]
    for hex_value in genes_hexa_list:
        gene_data=gene_to_unprocessed_data(hex_value)
        gene_data=unprocessed_data_to_processed_data(gene_data, num_sensory=num_neurons[0], num_internal=num_neurons[1], num_output=num_neurons[2])
        flag=True
        for gene in genes_list: #removing bidirectional connections of neurons
            if gene['source_ID'] == gene_data['sink_ID'] and gene['sink_ID'] == gene_data['source_ID']:
                flag=False
            if gene['source_ID'] == gene_data['source_ID'] and gene['sink_ID'] == gene_data['sink_ID']:
                gene['connection_weight']+=gene_data['connection_weight']
                flag=False
        if flag==True:
            genes_list.append(gene_data)
            #print('gene_data:',gene_data)
    #print('genes_list:',genes_list)
    brain=processed_data_to_brain(genes_hexa_list,genes_list,activation_inputs_dict,num_neurons)
    if show_graph:
        graph_visuals(genes_list)
    #print('another self.genes_list:',brain.genes_list)
    return brain
#{neuron1:input_activations_dict_1,.......} => input_activation_dict1={'S0':0.1,.....}

def genes_hexa_list_to_genes_list(genes_hexa_list,num_neurons):
    genes_list = []
    for hex_value in genes_hexa_list:
        gene_data = gene_to_unprocessed_data(hex_value)
        gene_data = unprocessed_data_to_processed_data(gene_data, num_sensory=num_neurons[0],
                                                       num_internal=num_neurons[1], num_output=num_neurons[2])
        flag = True
        for gene in genes_list:  # removing bidirectional connections of neurons
            if gene['source_ID'] == gene_data['sink_ID'] and gene['sink_ID'] == gene_data['source_ID']:
                flag = False
            if gene['source_ID'] == gene_data['source_ID'] and gene['sink_ID'] == gene_data['sink_ID']:
                gene['connection_weight'] += gene_data['connection_weight']
                flag = False
        if flag == True:
            genes_list.append(gene_data)
    return genes_list
def sense_to_inputs_activations(screen,players_dict,step,steps_per_gen,size_parameter,seed=0):
    combined_activation_inputs_dict={}
    for i in range(len(list(players_dict.keys()))): #len(player_list)=population
        combined_activation_inputs_dict['player'+str(i)]={}
    '''
    1. S0:age
    2. S1:random input
    3. S2:blockage left-right
    4. S3:blockage forward
    5. S4:east border distance
    6. S5:west border distance
    7. S6:south border distance
    8. S7:north border distance
    9. S8:population long range forward
    10. S9:population density
    11. S10:nearest border distance
    12. S11:blockage long range
    13. S12:genetic similarity of forward neighbour
    14. S13:population gradient forward
    15. S14:last movement x
    16. S15:last movement y
    17. S16:population gradient left-right
    18. S17:pheromone gradient left-right
    19. S18:pheromone gradient forward
    20. S19:pheromone density
    '''
    for i in range(len(list(players_dict.keys()))):
        '''
        usually, we wouldnt define variables like my_player_co_ordinates_list,etc...
        because by changing these variables,out original variables done change
        they are basically a copy of out old variables(because they are lists or other
        objects), but here we only have to do 'sensing' and we dont have to change values
        of the original variables so its fine
        '''
        my_player_co_ordinates_list = players_dict['player' + str(i)].co_ordinates_list
        my_player_direction = players_dict['player' + str(i)].direction
        random.seed(seed+i)
        #S0:age
        age=step/steps_per_gen
        combined_activation_inputs_dict['player'+str(i)]['S0']=age
        #S1:random_input
        random_input=random.uniform(0,1)
        combined_activation_inputs_dict['player'+str(i)]['S1']=random_input
        #S2:blockage left-right
        for player_name,player in players_dict.items():
            flag=False
            if my_player_direction=='north' or my_player_direction=='south':
                '''
                ( _ and _ ) or ( _ and _ ) format
                if direction is north:
                first bracket for moving left case(moving west) and second bracket for moving right case(moving east)
                '''
                #first if statement for perpendicular axis and 2nd if statement for axial axis
                if abs(player.co_ordinates_list[1]-my_player_co_ordinates_list[1])<3*size_parameter:
                    if (player.co_ordinates_list[0]>(my_player_co_ordinates_list[0] - 4*size_parameter) and my_player_co_ordinates_list[0]>player.co_ordinates_list[0]) or (player.co_ordinates_list[0]< (my_player_co_ordinates_list[0] + 4*size_parameter) and my_player_co_ordinates_list[0]<player.co_ordinates_list[0]):
                        combined_activation_inputs_dict['player' + str(i)]['S2'] = 1
                        flag=True
            elif my_player_direction=='west' or my_player_direction=='east':
                '''
                ( _ and _ ) or ( _ and _ ) format
                if direction is east
                first bracket for moving left case(moving north) and second bracket for moving right case(moving south)
                '''
                # first if statement for perpendicular axis and 2nd if statement for axial axis
                if abs(player.co_ordinates_list[0] - my_player_co_ordinates_list[0]) < 3*size_parameter:
                    if (player.co_ordinates_list[1]>(my_player_co_ordinates_list[1] - 4*size_parameter) and my_player_co_ordinates_list[1]>player.co_ordinates_list[1]) or (player.co_ordinates_list[1]< (my_player_co_ordinates_list[1] + 4*size_parameter) and my_player_co_ordinates_list[1]<player.co_ordinates_list[1]):
                        combined_activation_inputs_dict['player' + str(i)]['S2'] = 1
                        flag=True
            if flag == False:
                combined_activation_inputs_dict['player' + str(i)]['S2'] = 0
            #S3:blockage forward
            flag=False
            if my_player_direction=='north':
                if abs(player.co_ordinates_list[0] - my_player_co_ordinates_list[0] < 3*size_parameter):
                    if (player.co_ordinates_list[1]>(my_player_co_ordinates_list[1] - 4*size_parameter) and my_player_co_ordinates_list[1]>player.co_ordinates_list[1]):
                        combined_activation_inputs_dict['player' + str(i)]['S3'] = 1
                        flag = True
            elif my_player_direction == 'south':
                if abs(player.co_ordinates_list[0] - my_player_co_ordinates_list[0] < 3*size_parameter):
                    if (player.co_ordinates_list[1]< (my_player_co_ordinates_list[1] + 4*size_parameter) and my_player_co_ordinates_list[1]<player.co_ordinates_list[1]):
                        combined_activation_inputs_dict['player' + str(i)]['S3'] = 1
                        flag = True
            elif my_player_direction == 'west':
                if abs(player.co_ordinates_list[1] - my_player_co_ordinates_list[1] < 3*size_parameter):
                    if (player.co_ordinates_list[0]>(my_player_co_ordinates_list[0] - 4*size_parameter) and my_player_co_ordinates_list[0]>player.co_ordinates_list[0]):
                        combined_activation_inputs_dict['player' + str(i)]['S3'] = 1
                        flag = True
            elif my_player_direction == 'east':
                if abs(player.co_ordinates_list[1] - my_player_co_ordinates_list[1] < 3*size_parameter):
                    if (player.co_ordinates_list[0]< (my_player_co_ordinates_list[0] + 4*size_parameter) and my_player_co_ordinates_list[0]<player.co_ordinates_list[0]):
                        combined_activation_inputs_dict['player' + str(i)]['S3'] = 1
                        flag = True
            if flag == False:
                combined_activation_inputs_dict['player' + str(i)]['S3'] = 0
        #S4:east border distance
        input=(screen.get_size()[0]-my_player_co_ordinates_list[0])/screen.get_size()[0]
        combined_activation_inputs_dict['player'+str(i)]['S4']=input
        #S5:west border distance
        input =(my_player_co_ordinates_list[0])/screen.get_size()[0]
        combined_activation_inputs_dict['player' + str(i)]['S5'] = input
        #S6:south border distance
        input=(screen.get_size()[1]-my_player_co_ordinates_list[1])/screen.get_size()[1]
        combined_activation_inputs_dict['player'+str(i)]['S6']=input
        #S7:north border distance
        input =(my_player_co_ordinates_list[0])/screen.get_size()[0]
        combined_activation_inputs_dict['player' + str(i)]['S7'] = input
        #S8:population long range forward
        forward_blocks = []
        input = 0
        if my_player_direction=='east':
            for x in range(my_player_co_ordinates_list[0]//size_parameter,screen.get_size()[0]//size_parameter):
                forward_blocks.append([x*size_parameter,my_player_co_ordinates_list[1]])
            for player_name,player in players_dict.items():
                if player.co_ordinates_list in forward_blocks:
                    input+=1
            if (screen.get_size()[0]-my_player_co_ordinates_list[0]+1)!=0:
                input/=(screen.get_size()[0]-my_player_co_ordinates_list[0]+1)
                input*=size_parameter
            else:
                input=0
            combined_activation_inputs_dict['player'+str(i)]['S8']=input
        elif my_player_direction=='west':
            for x in range(0,my_player_co_ordinates_list[0]//size_parameter):
                forward_blocks.append([x*size_parameter,my_player_co_ordinates_list[1]])
            for player_name,player in players_dict.items():
                if player.co_ordinates_list in forward_blocks:
                    input+=1
            if (my_player_co_ordinates_list[0]+1)!=0:
                input/=(my_player_co_ordinates_list[0]+1)
                input*=size_parameter
            else:
                input=0
            combined_activation_inputs_dict['player'+str(i)]['S8']=input
        elif my_player_direction=='north':
            for y in range(0,my_player_co_ordinates_list[1]//size_parameter):
                forward_blocks.append([my_player_co_ordinates_list[0],y*size_parameter])
            for player_name,player in players_dict.items():
                if player.co_ordinates_list in forward_blocks:
                    input+=1
            if (my_player_co_ordinates_list[1]+1)!=0:
                input/=(my_player_co_ordinates_list[1]+1)
                input*=size_parameter
            else:
                input=0
            combined_activation_inputs_dict['player'+str(i)]['S8']=input
        elif my_player_direction == 'south':
            for y in range(my_player_co_ordinates_list[1]//size_parameter, screen.get_size()[1]//size_parameter):
                forward_blocks.append([my_player_co_ordinates_list[0], y*size_parameter])
            for player_name, player in players_dict.items():
                if player.co_ordinates_list in forward_blocks:
                    input += 1
            if (screen.get_size()[1] - my_player_co_ordinates_list[1]+1)!=0:
                input /= (screen.get_size()[1] - my_player_co_ordinates_list[1]+1)
                input*=size_parameter
            combined_activation_inputs_dict['player' + str(i)]['S8'] = input
        #S9:population density:(5*size_parameter)*(5*size_parameter) rectangle with my_player at centre
        rectangle_list=[]
        input=0
        for x in range(my_player_co_ordinates_list[0]-6*size_parameter,my_player_co_ordinates_list[0]+5*size_parameter):
            for y in range(my_player_co_ordinates_list[1]-6*size_parameter,my_player_co_ordinates_list[1]+5*size_parameter):
                rectangle_list.append([x,y])
        for player_name, player in players_dict.items():
            if player.co_ordinates_list in rectangle_list:
                input += 1
        input/=pow(10*size_parameter-1,2)
        combined_activation_inputs_dict['player'+str(i)]['S9']=input
        #S10:nearest border distance
        # distances from borders:
        #[my_player_co_ordinates_list[0],my_player_co_ordinates_list[1],
        # screen.get_size()[0]-my_player_co_ordinates_list[0],
        # screen.get_size()[1]-my_player_co_ordinates_list[1]]
        nearest_distance=min(my_player_co_ordinates_list[0]-size_parameter//2+1,my_player_co_ordinates_list[1]-size_parameter//2+1,screen.get_size()[0]-my_player_co_ordinates_list[0]-size_parameter//2+1,screen.get_size()[1]-my_player_co_ordinates_list[1]-size_parameter//2+1)
        input=nearest_distance/max(screen.get_size()[0]-size_parameter,screen.get_size()[1]-size_parameter)
        combined_activation_inputs_dict['player'+str(i)]['S10']=input
        print(f'players sensed:{i}')
    return combined_activation_inputs_dict

'''
1. O0:move random
2. O1:move left/right(-1,1)
3. O2:move forward
4. O3:move reverse
5. O4:move south/north(1,-1)
6. O5:move west/east(-1,1)
7. O6:kill forward/reverse(1,-1)
'''
def update_activations(players_dict,combined_activation_inputs_dict):
    combined_stored_neurons_dict={}
    combined_stored_incoming_exhausted_dict={}
    for i in range(len(list(players_dict.keys()))):
        for input_neu in players_dict['player'+str(i)].brain.input_neurons_list:
            players_dict['player'+str(i)].brain.neurons_dict[input_neu].activation=combined_activation_inputs_dict['player'+str(i)][input_neu]
            #print(players_dict['player'+str(i)].brain.neurons_dict[input_neu].activation)
        print("player number:",i)
        stored_neurons_dict,stored_incoming_exhausted_dict=players_dict['player'+str(i)].brain.forward_propagation()
        combined_stored_neurons_dict['player'+str(i)]=stored_neurons_dict
        combined_stored_incoming_exhausted_dict['player'+str(i)]=stored_incoming_exhausted_dict
        # output_activations_list = []
        # for output_neu in players_dict['player' + str(i)].brain.output_neurons_list:
        #     x = players_dict['player' + str(i)].brain.neurons_dict[output_neu].activation
        #     output_activations_list.append(x)
        # print(output_activations_list)
    return players_dict,combined_stored_neurons_dict,combined_stored_incoming_exhausted_dict

def position_errors_resolve(my_player,players_dict,screen,size_parameter):
    for player_name, player in players_dict.items():
        if ((player!=my_player) and len(my_player.co_ordinates_history_list)>=2 and (abs(player.co_ordinates_list[0]-my_player.co_ordinates_list[0])<size_parameter) and (abs(player.co_ordinates_list[1]-my_player.co_ordinates_list[1])<size_parameter)):
            my_player.co_ordinates_history_list.remove(my_player.co_ordinates_list)
            #print(my_player.co_ordinates_history_list)
            my_player.co_ordinates_list = my_player.co_ordinates_history_list[-1]
            my_player.rect_co_ordinates_list = change_co_ordinates_to_rect_co_ordinates(my_player.co_ordinates_list, size_parameter)
            break
    if (len(my_player.co_ordinates_history_list)>=2) and (my_player.co_ordinates_list[0]+3*size_parameter//2> screen.get_size()[0] or my_player.co_ordinates_list[0]-3*size_parameter//2<0 or my_player.co_ordinates_list[1]+3*size_parameter//2>screen.get_size()[1] or my_player.co_ordinates_list[1]-3*size_parameter//2<0):
        my_player.co_ordinates_history_list.remove(my_player.co_ordinates_list)
        print(len(my_player.co_ordinates_history_list))
        my_player.co_ordinates_list = my_player.co_ordinates_history_list[-1]
        my_player.rect_co_ordinates_list = change_co_ordinates_to_rect_co_ordinates(my_player.co_ordinates_list, size_parameter)
    return my_player,players_dict

def change_co_ordinates_to_rect_co_ordinates(co_ordinates_list,size_parameter):
    x=co_ordinates_list[0]
    y=co_ordinates_list[1]
    rect_co_ordinates_list=[]
    for x_rect in range(x - 3*size_parameter//2 - 1, x + 3*size_parameter//2 + 1):
        for y_rect in range(y - 3*size_parameter//2 - 1, y + 3*size_parameter//2 + 1):
            rect_co_ordinates_list.append([x_rect, y_rect])
    return rect_co_ordinates_list
def change(players_dict,screen,size_parameter,kill_neuron=False):
    for i in range(len(list(players_dict.keys()))):
        combined_co_ordinates_list=[]
        for player_name, player in players_dict.items():
            if player!=players_dict['player'+str(i)]:
                for j in range(len(player.rect_co_ordinates_list)):
                    combined_co_ordinates_list.append(player.rect_co_ordinates_list[j])
            else:
                pass
        #print([players_dict['player' + str(i)].co_ordinates_list[0] + size_parameter, players_dict['player' + str(i)].co_ordinates_list[1]] not in combined_co_ordinates_list)
        for output_neu in players_dict['player'+str(i)].brain.output_neurons_list:
            output_activation=players_dict['player'+str(i)].brain.neurons_dict[output_neu].activation
            #O0:move random
            if output_neu=='O0':
                index=random.randint(1,4)
                if index==1 and [players_dict['player'+str(i)].co_ordinates_list[0]+size_parameter,players_dict['player'+str(i)].co_ordinates_list[1]] not in combined_co_ordinates_list:
                    players_dict['player'+str(i)].co_ordinates_list[0]+=size_parameter
                elif index==2 and [players_dict['player'+str(i)].co_ordinates_list[0]-size_parameter,players_dict['player'+str(i)].co_ordinates_list[1]] not in combined_co_ordinates_list:
                    players_dict['player'+str(i)].co_ordinates_list[0]-=size_parameter
                elif index==3 and [players_dict['player'+str(i)].co_ordinates_list[0],players_dict['player'+str(i)].co_ordinates_list[1]+size_parameter] not in combined_co_ordinates_list:
                    players_dict['player'+str(i)].co_ordinates_list[1]+=size_parameter
                elif index==4 and [players_dict['player'+str(i)].co_ordinates_list[0],players_dict['player'+str(i)].co_ordinates_list[1]-size_parameter]  not in combined_co_ordinates_list:
                    players_dict['player'+str(i)].co_ordinates_list[1]-=size_parameter
                players_dict['player'+str(i)].co_ordinates_history_list.append(players_dict['player'+str(i)].co_ordinates_list)
                players_dict['player' + str(i)].rect_co_ordinates_list = change_co_ordinates_to_rect_co_ordinates(players_dict['player' + str(i)].co_ordinates_list, size_parameter)
                players_dict['player'+str(i)],players_dict=position_errors_resolve(players_dict['player'+str(i)],players_dict,screen,size_parameter)

            #O1:move left/right(-1,1)
            elif output_neu=='O1':
                if output_activation>0:
                    inp=random.choices([0,1],weights=[1-output_activation,output_activation])
                    if inp==[1]:
                        if players_dict['player'+str(i)].direction=='north' and [players_dict['player'+str(i)].co_ordinates_list[0]+size_parameter,players_dict['player'+str(i)].co_ordinates_list[1]] not in combined_co_ordinates_list:
                            players_dict['player'+str(i)].co_ordinates_list[0]+=size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        elif players_dict['player'+str(i)].direction=='south' and [players_dict['player'+str(i)].co_ordinates_list[0]-size_parameter,players_dict['player'+str(i)].co_ordinates_list[1]] not in combined_co_ordinates_list:
                            players_dict['player'+str(i)].co_ordinates_list[0]-=size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        elif players_dict['player'+str(i)].direction=='west' and [players_dict['player'+str(i)].co_ordinates_list[0],players_dict['player'+str(i)].co_ordinates_list[1]-size_parameter] not in combined_co_ordinates_list:
                            players_dict['player'+str(i)].co_ordinates_list[1]-=size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        elif players_dict['player'+str(i)].direction=='east' and [players_dict['player'+str(i)].co_ordinates_list[0],players_dict['player'+str(i)].co_ordinates_list[1]+size_parameter] not in combined_co_ordinates_list:
                            players_dict['player'+str(i)].co_ordinates_list[1]+=size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        players_dict['player' + str(i)].rect_co_ordinates_list = change_co_ordinates_to_rect_co_ordinates(players_dict['player' + str(i)].co_ordinates_list, size_parameter)
                        players_dict['player' + str(i)], players_dict = position_errors_resolve(players_dict['player' + str(i)], players_dict, screen, size_parameter)
                elif output_activation<0:
                    inp=random.choices([0,1],weights=[1-abs(output_activation),abs(output_activation)])
                    if inp==[1]:
                        if players_dict['player' + str(i)].direction == 'north' and [players_dict['player' + str(i)].co_ordinates_list[0] - size_parameter,players_dict['player' + str(i)].co_ordinates_list[1]] not in combined_co_ordinates_list:
                            players_dict['player' + str(i)].co_ordinates_list[0] -= size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        elif players_dict['player' + str(i)].direction == 'south' and [players_dict['player' + str(i)].co_ordinates_list[0] + size_parameter,players_dict['player' + str(i)].co_ordinates_list[1]] not in combined_co_ordinates_list:
                            players_dict['player' + str(i)].co_ordinates_list[0] += size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        elif players_dict['player' + str(i)].direction == 'west' and [players_dict['player' + str(i)].co_ordinates_list[0],players_dict['player' + str(i)].co_ordinates_list[1] + size_parameter] not in combined_co_ordinates_list:
                            players_dict['player' + str(i)].co_ordinates_list[1] += size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        elif players_dict['player' + str(i)].direction == 'east' and [players_dict['player' + str(i)].co_ordinates_list[0],players_dict['player' + str(i)].co_ordinates_list[1] - size_parameter] not in combined_co_ordinates_list:
                            players_dict['player' + str(i)].co_ordinates_list[1] -= size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        players_dict['player' + str(i)].rect_co_ordinates_list = change_co_ordinates_to_rect_co_ordinates(players_dict['player' + str(i)].co_ordinates_list, size_parameter)
                        players_dict['player' + str(i)], players_dict = position_errors_resolve(players_dict['player' + str(i)], players_dict, screen, size_parameter)
            #O2:move forward
            elif output_neu=='O2':
                if output_activation > 0:
                    inp = random.choices([0, 1], weights=[1 - output_activation, output_activation])
                    if inp==[1]:
                        if players_dict['player' + str(i)].direction == 'north' and [players_dict['player' + str(i)].co_ordinates_list[0], players_dict['player' + str(i)].co_ordinates_list[1]-size_parameter] not in combined_co_ordinates_list:
                            players_dict['player' + str(i)].co_ordinates_list[1] -= size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        elif players_dict['player' + str(i)].direction == 'south' and [players_dict['player' + str(i)].co_ordinates_list[0] , players_dict['player' + str(i)].co_ordinates_list[1]+size_parameter] not in combined_co_ordinates_list:
                            players_dict['player' + str(i)].co_ordinates_list[1] += size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        elif players_dict['player' + str(i)].direction == 'west' and [players_dict['player' + str(i)].co_ordinates_list[0]-size_parameter, players_dict['player' + str(i)].co_ordinates_list[1]] not in combined_co_ordinates_list:
                            players_dict['player' + str(i)].co_ordinates_list[0] -= size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        elif players_dict['player' + str(i)].direction == 'east' and [players_dict['player' + str(i)].co_ordinates_list[0]+size_parameter, players_dict['player' + str(i)].co_ordinates_list[1]] not in combined_co_ordinates_list:
                            players_dict['player' + str(i)].co_ordinates_list[0] += size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        players_dict['player' + str(i)].rect_co_ordinates_list = change_co_ordinates_to_rect_co_ordinates(players_dict['player' + str(i)].co_ordinates_list, size_parameter)
                        players_dict['player' + str(i)], players_dict = position_errors_resolve(players_dict['player' + str(i)], players_dict, screen, size_parameter)
            #O3:move reverse
            elif output_neu=='O3':
                if output_activation > 0:
                    inp = random.choices([0, 1], weights=[1 - output_activation, output_activation])
                    if inp==[1]:
                        if players_dict['player' + str(i)].direction == 'north' and [players_dict['player' + str(i)].co_ordinates_list[0], players_dict['player' + str(i)].co_ordinates_list[1] + size_parameter] not in combined_co_ordinates_list:
                            players_dict['player' + str(i)].co_ordinates_list[1] += size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        elif players_dict['player' + str(i)].direction == 'south' and [players_dict['player' + str(i)].co_ordinates_list[0], players_dict['player' + str(i)].co_ordinates_list[1] - size_parameter] not in combined_co_ordinates_list:
                            players_dict['player' + str(i)].co_ordinates_list[1] -= size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        elif players_dict['player' + str(i)].direction == 'west' and [players_dict['player' + str(i)].co_ordinates_list[0] + size_parameter, players_dict['player' + str(i)].co_ordinates_list[1]] not in combined_co_ordinates_list:
                            players_dict['player' + str(i)].co_ordinates_list[0] += size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        elif players_dict['player' + str(i)].direction == 'east' and [players_dict['player' + str(i)].co_ordinates_list[0] - size_parameter, players_dict['player' + str(i)].co_ordinates_list[1]] not in combined_co_ordinates_list:
                            players_dict['player' + str(i)].co_ordinates_list[0] -= size_parameter
                            players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        players_dict['player' + str(i)].rect_co_ordinates_list = change_co_ordinates_to_rect_co_ordinates(players_dict['player' + str(i)].co_ordinates_list, size_parameter)
                        players_dict['player' + str(i)], players_dict = position_errors_resolve(players_dict['player' + str(i)], players_dict, screen, size_parameter)
                    # O3:move reverse
            #O4:move south/north(1,-1)
            elif output_neu=='O4':
                if output_activation>0:
                    inp=random.choices([0,1],weights=[1-output_activation,output_activation])
                    if inp==[1] and [players_dict['player' + str(i)].co_ordinates_list[0], players_dict['player' + str(i)].co_ordinates_list[1] + size_parameter] not in combined_co_ordinates_list:
                        players_dict['player' + str(i)].co_ordinates_list[1] += size_parameter
                        players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        players_dict['player' + str(i)].rect_co_ordinates_list = change_co_ordinates_to_rect_co_ordinates(players_dict['player' + str(i)].co_ordinates_list, size_parameter)
                        players_dict['player' + str(i)], players_dict = position_errors_resolve(players_dict['player' + str(i)], players_dict, screen, size_parameter)
                elif output_activation<0:
                    inp=random.choices([0,1],weights=[1-abs(output_activation),abs(output_activation)])
                    if inp==[1] and [players_dict['player' + str(i)].co_ordinates_list[0], players_dict['player' + str(i)].co_ordinates_list[1] - size_parameter] not in combined_co_ordinates_list:
                        players_dict['player' + str(i)].co_ordinates_list[1] -= size_parameter
                        players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        players_dict['player' + str(i)].rect_co_ordinates_list = change_co_ordinates_to_rect_co_ordinates(players_dict['player' + str(i)].co_ordinates_list, size_parameter)
                        players_dict['player' + str(i)], players_dict = position_errors_resolve(players_dict['player' + str(i)],players_dict, screen,size_parameter)
            #O5:move west/east(-1, 1)
            elif output_neu=='O5':
                if output_activation>0:
                    inp=random.choices([0,1],weights=[1-output_activation,output_activation])
                    if inp==[1] and [players_dict['player' + str(i)].co_ordinates_list[0]+size_parameter, players_dict['player' + str(i)].co_ordinates_list[1]] not in combined_co_ordinates_list:
                        players_dict['player' + str(i)].co_ordinates_list[0] += size_parameter
                        players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        players_dict['player' + str(i)].rect_co_ordinates_list = change_co_ordinates_to_rect_co_ordinates(players_dict['player' + str(i)].co_ordinates_list, size_parameter)
                        players_dict['player' + str(i)], players_dict = position_errors_resolve(players_dict['player' + str(i)], players_dict, screen, size_parameter)
                elif output_activation<0:
                    inp=random.choices([0,1],weights=[1-abs(output_activation),abs(output_activation)])
                    if inp==[1] and [players_dict['player' + str(i)].co_ordinates_list[0]-size_parameter, players_dict['player' + str(i)].co_ordinates_list[1]] not in combined_co_ordinates_list:
                        players_dict['player' + str(i)].co_ordinates_list[0] -= size_parameter
                        players_dict['player' + str(i)].co_ordinates_history_list.append(players_dict['player' + str(i)].co_ordinates_list)
                        players_dict['player' + str(i)].rect_co_ordinates_list = change_co_ordinates_to_rect_co_ordinates(players_dict['player' + str(i)].co_ordinates_list, size_parameter)
                        players_dict['player' + str(i)], players_dict = position_errors_resolve(players_dict['player' + str(i)],players_dict, screen,size_parameter)
            #O6:kill forward/reverse(1,-1)
            elif output_neu=='O6' and kill_neuron==True:
                killed_players_list=[]
                if output_activation>0:
                    kill_co_ordinates_list=[]
                    if players_dict['player' + str(i)].direction=='north':
                        for x in range(players_dict['player'+str(i)].co_ordinates_list[0]-size_parameter,players_dict['player'+str(i)].co_ordinates_list[0]):
                            for y in range(players_dict['player'+str(i)].co_ordinates_list[1]-4*size_parameter,players_dict['player'+str(i)].co_ordinates_list[0]-4*size_parameter):
                                kill_co_ordinates_list.append([x,y])
                    elif players_dict['player' + str(i)].direction=='south':
                        for x in range(players_dict['player'+str(i)].co_ordinates_list[0]-size_parameter,players_dict['player'+str(i)].co_ordinates_list[0]+size_parameter):
                            for y in range(players_dict['player'+str(i)].co_ordinates_list[1]+size_parameter//2,players_dict['player'+str(i)].co_ordinates_list[0]+2*size_parameter):
                                kill_co_ordinates_list.append([x,y])
                    elif players_dict['player' + str(i)].direction=='west':
                        for x in range(players_dict['player'+str(i)].co_ordinates_list[0]-2*size_parameter,players_dict['player'+str(i)].co_ordinates_list[0]-size_parameter//2):
                            for y in range(players_dict['player'+str(i)].co_ordinates_list[1]-size_parameter,players_dict['player'+str(i)].co_ordinates_list[0]+size_parameter):
                                kill_co_ordinates_list.append([x,y])
                    elif players_dict['player' + str(i)].direction=='east':
                        for x in range(players_dict['player'+str(i)].co_ordinates_list[0]+size_parameter//2,players_dict['player'+str(i)].co_ordinates_list[0]+2*size_parameter):
                            for y in range(players_dict['player'+str(i)].co_ordinates_list[1]-size_parameter,players_dict['player'+str(i)].co_ordinates_list[0]+size_parameter):
                                kill_co_ordinates_list.append([x,y])
                    inp=random.choices([0,1],weights=[1-output_activation,output_activation])
                    if inp==[1]:
                        for player_name,player in players_dict.items():
                            if player.co_ordinates_list in kill_co_ordinates_list:
                                killed_players_list.append(player_name)
                elif output_activation<0:
                    kill_co_ordinates_list=[]
                    if players_dict['player' + str(i)].direction=='south':
                        for x in range(players_dict['player'+str(i)].co_ordinates_list[0]-size_parameter,players_dict['player'+str(i)].co_ordinates_list[0]+size_parameter):
                            for y in range(players_dict['player'+str(i)].co_ordinates_list[1]-2*size_parameter,players_dict['player'+str(i)].co_ordinates_list[0]-size_parameter//2):
                                kill_co_ordinates_list.append([x,y])
                    elif players_dict['player' + str(i)].direction=='north':
                        for x in range(players_dict['player'+str(i)].co_ordinates_list[0]-size_parameter,players_dict['player'+str(i)].co_ordinates_list[0]+size_parameter):
                            for y in range(players_dict['player'+str(i)].co_ordinates_list[1]+size_parameter//2,players_dict['player'+str(i)].co_ordinates_list[0]+2*size_parameter):
                                kill_co_ordinates_list.append([x,y])
                    elif players_dict['player' + str(i)].direction=='east':
                        for x in range(players_dict['player'+str(i)].co_ordinates_list[0]-2*size_parameter,players_dict['player'+str(i)].co_ordinates_list[0]-size_parameter//2):
                            for y in range(players_dict['player'+str(i)].co_ordinates_list[1]-size_parameter,players_dict['player'+str(i)].co_ordinates_list[0]+size_parameter):
                                kill_co_ordinates_list.append([x,y])
                    elif players_dict['player' + str(i)].direction=='west':
                        for x in range(players_dict['player'+str(i)].co_ordinates_list[0]+size_parameter//2,players_dict['player'+str(i)].co_ordinates_list[0]+2*size_parameter):
                            for y in range(players_dict['player'+str(i)].co_ordinates_list[1]-size_parameter,players_dict['player'+str(i)].co_ordinates_list[0]+size_parameter):
                                kill_co_ordinates_list.append([x,y])
                    inp=random.choices([0,1],weights=[1-output_activation,output_activation])
                    if inp==1:
                        for player_name,player in players_dict.items():
                            if player.co_ordinates_list in kill_co_ordinates_list:
                                killed_players_list.append(player_name)
                for player_name in killed_players_list:
                    del players_dict[player_name]
        if players_dict['player' + str(i)].co_ordinates_list[0] + 3 * size_parameter // 2 > screen.get_width():
            # print("wow!")
            # print(players_dict['player' + str(i)].co_ordinates_list[0])
            # print(screen.get_width()-size_parameter//2)
            players_dict['player' + str(i)].co_ordinates_list[0] = screen.get_width() - 3 * size_parameter // 2 - 1
        if players_dict['player' + str(i)].co_ordinates_list[1] + 3 * size_parameter // 2 > screen.get_height():
            players_dict['player' + str(i)].co_ordinates_list[1] = screen.get_height() - 3 * size_parameter // 2 - 2
        if players_dict['player' + str(i)].co_ordinates_list[0] - 3 * size_parameter // 2 < 0:
            players_dict['player' + str(i)].co_ordinates_list[0] = 3 * size_parameter // 2 + 2
        if players_dict['player' + str(i)].co_ordinates_list[1] - 3 * size_parameter // 2 < 0:
            players_dict['player' + str(i)].co_ordinates_list[1] = 3 * size_parameter // 2 + 2
        output_activations_list=[]
        # for output_neu in players_dict['player'+str(i)].brain.output_neurons_list:
        #     x=players_dict['player'+str(i)].brain.neurons_dict[output_neu].activation
        #     output_activations_list.append(x)

        #print(f'players changed:{i},  ',players_dict['player'+str(i)].brain.output_neurons_list,'  ',output_activations_list)
        print(f'players changed:{i}')
    return players_dict

def back_to_normal(players_dict,combined_stored_neurons_dict,combined_stored_incoming_exhausted_dict):
    for i in range(len(players_dict.keys())):
        stored_neurons_dict=combined_stored_neurons_dict['player'+str(i)]
        stored_incoming_exhausted_dict=combined_stored_incoming_exhausted_dict['player'+str(i)]
        players_dict['player'+str(i)].brain.neurons_dict=copy.deepcopy(stored_neurons_dict)
        players_dict['player'+str(i)].brain.incoming_exhausted_dict=copy.deepcopy(stored_incoming_exhausted_dict)
    return players_dict
def change_char_in_string(s, index, new_char):
    s_list = list(s)
    s_list[index] = new_char
    return ''.join(s_list)

#mutation_prob is the probability of mutation in a gene
def mutate(players_dict,num_neurons,remaining_players_list,mutation_prob=0.01):
    num_mutations=0
    for i in range(len(list(players_dict.keys())[:])):
        for j in range(len(players_dict[remaining_players_list[i]].brain.genes_hexa_list[:])):
            decider=[0,1]
            inp=random.choices(decider,weights=[1-mutation_prob,mutation_prob])
            if inp==[1]:
                index=random.randint(0,7)
                change_decider=['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
                char_to_change=random.choices(change_decider,weights=np.ones(15)/15)[0]
                players_dict[remaining_players_list[i]].brain.genes_hexa_list[j]=change_char_in_string(players_dict[remaining_players_list[i]].brain.genes_hexa_list[j], index, char_to_change)
                genes_list = []
                num_mutations+=1
                for hex_value in players_dict[remaining_players_list[i]].brain.genes_hexa_list[j]:
                    gene_data = gene_to_unprocessed_data(hex_value)
                    gene_data = unprocessed_data_to_processed_data(gene_data, num_sensory=num_neurons[0],
                                                                   num_internal=num_neurons[1],
                                                                   num_output=num_neurons[2])
                    flag = True
                    for gene in genes_list:  # removing bidirectional connections of neurons
                        if gene['source_ID'] == gene_data['sink_ID'] and gene['sink_ID'] == gene_data['source_ID']:
                            flag = False
                        if gene['source_ID'] == gene_data['source_ID'] and gene['sink_ID'] == gene_data['sink_ID']:
                            gene['connection_weight'] += gene_data['connection_weight']
                            flag = False
                    if flag == True:
                        genes_list.append(gene_data)
                for gene in genes_list[:]:
                    # print(gene['sink_ID'],'  ',gene['source_ID'])
                    # print("======================================")
                    if gene['sink_ID'] == gene['source_ID']:
                        genes_list.remove(gene)
                edge_list, input_neurons_list, output_neurons_list = edges_list(genes_list)
                activation_inputs_dict={}
                for neu in input_neurons_list:
                    activation_inputs_dict[neu]=0
                neurons_dictionary, incoming_exhausted_list, useless_neurons_list, genes_list, edge_list = neurons_dict(
                    genes_list, activation_inputs_dict, num_neurons, edge_list)
                # print('wow_genes_list:',genes_list)
                genes_hexa_list=players_dict[remaining_players_list[i]].brain.genes_hexa_list
                final_brain = brain(genes_hexa_list, genes_list, edge_list, neurons_dictionary, input_neurons_list,
                                    output_neurons_list, incoming_exhausted_list)
                players_dict[remaining_players_list[i]].brain=final_brain
                players_dict[remaining_players_list[i]].genes_list=final_brain.genes_list
    return players_dict,num_mutations
def replicate(players_dict,env_width,env_height,size_parameter,remaining_players_list,default_population=400):
    babies_per_player=default_population//len(list(players_dict.keys()))
    population=babies_per_player*len(list(players_dict.keys()))
    new_players_dict={}
    genes_hexa_dict={}
    for i in range(len(list(players_dict.keys()))):
        genes_hexa_dict[remaining_players_list[i]]=players_dict[remaining_players_list[i]].brain.genes_hexa_list
    #print(genes_hexa_dict)
    colors_dict,max_gene,max_value = encode_players_with_same_genes(genes_hexa_dict)
    directions_dict=directions_dict_generator(default_population)
    co_ordinates_dict, rect_co_ordinates_dict = co_ordinates_initialize_dict(env_width, env_height, default_population,size_parameter)
    for i in range(len(list(players_dict.keys()))):
        for j in range(babies_per_player):
            new_players_dict['player'+str(i*babies_per_player+j)]=players_dict[remaining_players_list[i]].__deepcopy__()
            new_players_dict['player' + str(i * babies_per_player + j)].direction=directions_dict['player' + str(i * babies_per_player + j)]
            new_players_dict['player' + str(i * babies_per_player + j)].co_ordinates_list, new_players_dict['player' + str(i * babies_per_player + j)].rect_co_ordinates_list=co_ordinates_dict['player' + str(i * babies_per_player + j)],rect_co_ordinates_dict['player' + str(i * babies_per_player + j)]
            new_players_dict['player'+str(i*babies_per_player+j)].co_ordinates_history_list=[new_players_dict['player' + str(i * babies_per_player + j)].co_ordinates_list]
            color = colors_dict[remaining_players_list[i]]
            new_players_dict['player'+str(i*babies_per_player+j)].pygame_object=circle(new_players_dict['player'+str(i*babies_per_player+j)].co_ordinates_list, color, radius=size_parameter // 2)
    remaining_population=default_population-len(list(players_dict.keys()))*babies_per_player
    for k in range(remaining_population):
        new_players_dict['player'+str(len(players_dict.keys())*babies_per_player+k)]=players_dict[remaining_players_list[k]].__deepcopy__()
        new_players_dict['player' + str(len(players_dict.keys())*babies_per_player+k)].direction = directions_dict[
            'player' + str(len(players_dict.keys())*babies_per_player+k)]
        new_players_dict['player' + str(len(players_dict.keys())*babies_per_player+k)].co_ordinates_list, new_players_dict[
            'player' + str(len(players_dict.keys())*babies_per_player+k)].rect_co_ordinates_list = co_ordinates_dict[
            'player' + str(len(players_dict.keys())*babies_per_player+k)], rect_co_ordinates_dict[
            'player' + str(len(players_dict.keys())*babies_per_player+k)]
        co_ordinates_history_list=copy.deepcopy(new_players_dict['player' + str(k)].co_ordinates_list)
        new_players_dict['player' + str(len(players_dict.keys())*babies_per_player+k)].co_ordinates_history_list = [co_ordinates_history_list]
        color = colors_dict[remaining_players_list[k]]
        new_players_dict['player' + str(len(players_dict.keys())*babies_per_player+k)].pygame_object = circle(
            new_players_dict['player' + str(len(players_dict.keys())*babies_per_player+k)].co_ordinates_list, color,
            radius=size_parameter // 2)
    del players_dict
    return new_players_dict,population,max_gene,max_value

def condition(players_dict,screen,inp=1):
    remaining_players_list=[]
    to_remove=[]
    to_add=[]
    if inp==1:
        for i in range(len(list(players_dict.keys())[:])): #assuming no one dies before
            if players_dict['player'+str(i)].co_ordinates_list[0]>screen.get_width()//2:
                to_remove.append('player'+str(i))
            else:
                remaining_players_list.append('player'+str(i))
        for key in to_remove:
            del players_dict[key]
    elif inp==2:
        new_players_dict={}
        for i in range(len(list(players_dict.keys())[:])):
            if players_dict['player'+str(i)].co_ordinates_list[0]<screen.get_width()//5 and players_dict['player'+str(i)].co_ordinates_list[1]<screen.get_height()//5:
                to_add.append('player'+str(i))
            elif players_dict['player' + str(i)].co_ordinates_list[0] > 4*screen.get_width() // 5 and players_dict['player' + str(i)].co_ordinates_list[1] < screen.get_height() // 5:
                to_add.append('player' + str(i))
            elif players_dict['player'+str(i)].co_ordinates_list[0]<screen.get_width()//5 and players_dict['player'+str(i)].co_ordinates_list[1]>4*screen.get_height()//5:
                to_add.append('player'+str(i))
            elif players_dict['player'+str(i)].co_ordinates_list[0]>4*screen.get_width()//5 and players_dict['player'+str(i)].co_ordinates_list[1]>4*screen.get_height()//5:
                to_add.append('player'+str(i))
        for key in to_add:
            new_players_dict[key]=players_dict[key].__deepcopy__()
            remaining_players_list.append(key)
        del players_dict
        players_dict=new_players_dict
    return players_dict,remaining_players_list

def check(players_dict,screen):
    wrong_players_co_ordinates=[]
    for player_name,player in players_dict.items():
        if player.co_ordinates_list[0]>screen.get_width()//2:
            wrong_players_co_ordinates.append(player.co_ordinates_list)
    return wrong_players_co_ordinates

def restart_simulation(genes_hexa_dict,generations_done):
    size_parameter = 5
    num_neurons = [11, 2, 6]  # [sensory_neurons,internal_neurons,output_neurons]
    env_width = 500
    env_height = 500
    population = 300
    default_population = 300
    steps_per_gen = 120
    genome_length = 12
    generations = 500
    seed = 0
    remaining_players_number = []
    pygame.init()
    screen = pygame.display.set_mode((env_width, env_height), 0, 32)
    max_genes_list_combined = []
    co_ordinates_dict, rect_co_ordinates_dict = co_ordinates_initialize_dict(env_width, env_height, population, size_parameter)
    # print(f'co_ordinates_dict:{co_ordinates_dict}')
    directions_dict = directions_dict_generator(population)
    colors_dict, max_gene, max_value = encode_players_with_same_genes(genes_hexa_dict)
    max_genes_list_combined.append(copy.deepcopy(max_gene))
    activation_inputs_dict = {}
    players_dict = {}
    remaining_players_list=[f'player{i}' for i in range(len(list(genes_hexa_dict.keys())))]
    for i in range(num_neurons[0]):  # for unused brain input activations
        activation_inputs_dict['S' + str(i)] = 0.0
    for i in range(len(remaining_players_list)):
        # flag = False
        # if i==10:
        #     flag=True
        genes_hexa_list = genes_hexa_dict['player' + str(i)]
        # print('genes_hexa_list:',genes_hexa_list)
        unused_brain = genes_to_brain(genes_hexa_list, activation_inputs_dict, num_neurons, show_graph=False)
        # if i==10:
        #     genes_list=unused_brain.genes_list
        #     graph_visuals(unused_brain.genes_list)
        # print('unused_brain.genes_list:',unused_brain.genes_list)
        co_ordinates_list = co_ordinates_dict['player' + str(i)]
        rect_co_ordinates_list = rect_co_ordinates_dict['player' + str(i)]
        # print(rect_co_ordinates_list)
        direction = directions_dict['player' + str(i)]
        color = colors_dict['player' + str(i)]
        pygame_object = circle(co_ordinates_list, color, radius=size_parameter // 2)
        co_ordinates_history_list = [copy.deepcopy(co_ordinates_list)]
        players_dict['player' + str(i)] = player(co_ordinates_list, unused_brain.genes_list, unused_brain, pygame_object, direction, co_ordinates_history_list, rect_co_ordinates_list)
    for generation in range(generations_done+1,generations):
        players_dict, num_mutations = mutate(players_dict, num_neurons, remaining_players_list, mutation_prob=0.002)
        print('num_mutations:', num_mutations)
        print('num_players_after_mutation:', len(players_dict))
        players_dict, population, max_gene, max_value = replicate(players_dict, env_width, env_height, size_parameter, remaining_players_list, default_population=default_population)
        max_genes_list_combined.append(copy.deepcopy(max_gene))
        print('num_players_after_replication:', default_population, ' or ', len(players_dict))
        for step in range(steps_per_gen):
            # for i in range(len(players_dict)):
            #     for neu in players_dict['player' + str(i)].brain.output_neurons_list:
            #         print(f'before simulation activations (player{i}){neu}:',players_dict['player' + str(i)].brain.neurons_dict[neu].activation)
            # for i in range(len(list(players_dict.keys()))):
                # if step%2==0:
                #     print(f'player{i} co_ordinates history::',players_dict['player'+str(i)].co_ordinates_history_list)
                #     print(f'player{i} rect co ordinates:', players_dict['player' + str(i)].co_ordinates_history_list)
            print("step:",step)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
            screen.fill((255, 255, 255))
            for i in range(population):
                players_dict['player' + str(i)].pygame_object.draw(screen)
            # pygame.image.save(screen,rf'D:\Evolution\pygame_images_testing\images\image.png')
            pygame.display.flip()
            combined_activation_inputs_dict=sense_to_inputs_activations(screen,players_dict,step,steps_per_gen,size_parameter,seed=0)
            players_dict,stored_neurons_dict,stored_incoming_exhausted_dict=update_activations(players_dict,combined_activation_inputs_dict)
            players_dict=change(players_dict, screen, size_parameter, kill_neuron=False)
            players_dict=back_to_normal(players_dict,stored_neurons_dict,stored_incoming_exhausted_dict)
            #print(rf'D:\New_Evolution_improved_12_genome_length_images\generation{generation+1}\image{step+generation*steps_per_gen+1}.png')
            pygame.image.save(screen, rf'D:\New_Evolution_improved_12_genome_length_images\generation{generation+1}\image{step+generation*steps_per_gen+1}.png')
        players_dict,remaining_players_list=condition(players_dict,screen,inp=2)
        remaining_players_number.append(len(remaining_players_list))
        dicti = {}
        another_dicti={}
        for i in range(len(remaining_players_list)):
            dicti[f'player{i}_genes_list'] = players_dict[remaining_players_list[i]].genes_list
            another_dicti[f'player{i}_genes_hexa_list']=players_dict[remaining_players_list[i]].brain.genes_hexa_list
        players_json = json.dumps(dicti)
        players_another_json=json.dumps(another_dicti)
        list_json=json.dumps(remaining_players_number)
        max_gene_json=json.dumps(max_gene)
        max_genes_list_combined_json=json.dumps(max_genes_list_combined)
        with open('restarted_simulation.py', 'w') as f:
            f.write('players_genes_list=' + players_json)
            f.write('\n')
            f.write('players_genes_hexa_list='+players_another_json)
            f.write('\n')
            f.write('remaining_players_number='+list_json)
            f.write('\n')
            f.write('num_neurons=[11,2,6]')
            f.write('\n')
            f.write('max_genes_list_combined='+max_genes_list_combined_json)
            f.write('\n')
            f.write('max_gene='+max_gene_json)
            f.write('\n')
            f.write('max_number_of_same_genes='+str(max_value))
            f.write('\n')
            f.write('from useful_functions import graph_visuals,genes_hexa_list_to_genes_list')
            f.write('\n')
            f.write('max_genes_list=genes_hexa_list_to_genes_list(max_gene,num_neurons)')
            f.write('\n')
            f.write('graph_visuals(max_genes_list)')
