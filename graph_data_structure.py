import numpy as np
import pygame
import copy
import random

def edges_list(genes_list):
    edge_list=set()
    input_neurons_list=set()
    output_neurons_list=set()
    for gene in genes_list:
        edge_list.add(gene['source_ID'])
        edge_list.add(gene['sink_ID'])
        if gene['source_ID'][0]=='S':
            input_neurons_list.add(gene['source_ID'])
        if gene['sink_ID'][0]=='O':
            output_neurons_list.add(gene['sink_ID'])
    return list(edge_list),list(input_neurons_list),list(output_neurons_list)

# def detect_cycle(neurons_dict, neu, forming_chain, visited):
#     if len(forming_chain) > 4:
#         return False, forming_chain
#
#     forming_chain.append(neu)
#     visited.add(neu)
#
#     for next_neuron in neurons_dict[neu].outgoing_edges:
#         if next_neuron in forming_chain and len(forming_chain) >= 3:
#             forming_chain.append(next_neuron)
#             return True, forming_chain
#         if next_neuron[0] == 'I' and next_neuron not in visited:
#             found, forming_chain = detect_cycle(neurons_dict, next_neuron, forming_chain, visited)
#             if found:
#                 return True, forming_chain
#
#     forming_chain.pop()
#     visited.remove(neu)
#     return False, forming_chain
#
# def remove_random_edge_from_cycle(neurons_dict, incoming_exhausted_dict, cycle):
#     cycle_edges = [(cycle[i], cycle[i+1]) for i in range(len(cycle) - 1)]
#     if cycle_edges:
#         edge_to_remove = random.choice(cycle_edges)
#         source, sink = edge_to_remove
#         neurons_dict[source].outgoing_edges.remove(sink)
#         neurons_dict[sink].incoming_edges.remove(source)
#         incoming_exhausted_dict[sink].remove(source)
def useless_internal_neuron_detection(neurons_dict,incoming_exhausted_dict,edge_list,genes_list,flag=True):
    if flag:
        count=0
        for neu in list(neurons_dict.keys())[:]:
            # if neu not in list(numbering_dict.keys()):
            #     numbering_dict[neu]=0
            # numbering_dict[neu]+=1
            # if 'I1' in list(neurons_dict.keys())[:]:
            #     print(neurons_dict['I1'].outgoing_edges)
            count+=1
            #print(f'{neu}:wow:{neurons_dict[neu].outgoing_edges}')
            if neu[0]=='I' and (len(list(neurons_dict[neu].outgoing_edges)[:])==0):
                for new_neu in list(neurons_dict[neu].incoming_edges)[:]:
                    neurons_dict[new_neu].outgoing_edges.remove(neu)
                del neurons_dict[neu]
                del incoming_exhausted_dict[neu]
                edge_list.remove(neu)
                for gene in genes_list[:]:
                    if gene['sink_ID']==neu:
                        genes_list.remove(gene)
                #print(neu)
                break
            elif neu[0]=='I' and (len(list(neurons_dict[neu].incoming_edges)[:])==0):
                for new_neu in list(neurons_dict[neu].outgoing_edges)[:]:
                    neurons_dict[new_neu].incoming_edges.remove(neu)
                del neurons_dict[neu]
                del incoming_exhausted_dict[neu]
                edge_list.remove(neu)
                for gene in genes_list[:]:
                    if gene['source_ID']==neu:
                        genes_list.remove(gene)
                        incoming_exhausted_dict[gene['sink_ID']].remove(neu)
                break
        if count!=len(list(neurons_dict.keys())):
            neurons_dict,incoming_exhausted_dict,edge_list,genes_list=useless_internal_neuron_detection(neurons_dict, incoming_exhausted_dict, edge_list, genes_list, flag=True)

    return neurons_dict,incoming_exhausted_dict,edge_list,genes_list
# def useless_internal_neuron_detection(neurons_dict, incoming_exhausted_dict, edge_list, genes_list):
#     flag = True
#     while flag:
#         flag = False
#         for neu in list(neurons_dict.keys())[:]:
#             if neu[0] == 'I' and len(neurons_dict[neu].outgoing_edges) == 0:
#                 for new_neu in list(neurons_dict[neu].incoming_edges)[:]:
#                     neurons_dict[new_neu].outgoing_edges.remove(neu)
#                 del neurons_dict[neu]
#                 del incoming_exhausted_dict[neu]
#                 edge_list.remove(neu)
#                 for gene in genes_list[:]:
#                     if gene['sink_ID'] == neu:
#                         genes_list.remove(gene)
#                 flag = True
#                 break
#             elif neu[0] == 'I' and len(neurons_dict[neu].incoming_edges) == 0:
#                 for new_neu in list(neurons_dict[neu].outgoing_edges)[:]:
#                     neurons_dict[new_neu].incoming_edges.remove(neu)
#                 del neurons_dict[neu]
#                 del incoming_exhausted_dict[neu]
#                 edge_list.remove(neu)
#                 for gene in genes_list[:]:
#                     if gene['source_ID'] == neu:
#                         genes_list.remove(gene)
#                         incoming_exhausted_dict[gene['sink_ID']].remove(neu)
#                 flag = True
#                 break
#     return neurons_dict, incoming_exhausted_dict, edge_list, genes_list
def neurons_dict(genes_list,activation_inputs_dict,num_neurons,edge_list):
    #print('+1')
    neurons_dict={}
    incoming_exhausted_dict={}
    neurons_list=[]
    useless_neurons_list=[]
    numbering_dict={}
    for i in range(num_neurons[0]):
        neurons_list.append('S'+str(i))
    for i in range(num_neurons[1]):
        neurons_list.append('I'+str(i))
    for i in range(num_neurons[2]):
        neurons_list.append('O'+str(i))
    for name in edge_list:
        incoming_edges=[]
        outgoing_edges=[]
        for gene in genes_list:
            if gene['sink_ID']==name:
                incoming_edges.append(gene['source_ID'])
            elif gene['source_ID']==name:
                outgoing_edges.append(gene['sink_ID'])
        neurons_dict[name]=neuron(name=name,incoming_edges=incoming_edges,outgoing_edges=outgoing_edges)
        if name[0]=='S':
            neurons_dict[name].activation=copy.deepcopy(activation_inputs_dict[name])
        incoming_exhausted_dict[name]=copy.deepcopy(incoming_edges)
    # neurons_dict, incoming_exhausted_dict, edge_list, genes_list = useless_internal_neuron_detection(neurons_dict, incoming_exhausted_dict, edge_list, genes_list, flag=True)
    neurons_dict, incoming_exhausted_dict, edge_list, genes_list = useless_internal_neuron_detection(neurons_dict, incoming_exhausted_dict, edge_list, genes_list)
    # for neu in list(neurons_dict.keys())[:]:
    #     # if neu not in list(numbering_dict.keys()):
    #     #     numbering_dict[neu]=0
    #     # numbering_dict[neu]+=1
    #     # if 'I1' in list(neurons_dict.keys())[:]:
    #     #     print(neurons_dict['I1'].outgoing_edges)
    #     print(f'{neu}:{neurons_dict[neu].outgoing_edges}')
    #     if neu[0]=='I' and (len(list(neurons_dict[neu].outgoing_edges))==0):
    #         for new_neu in list(neurons_dict[neu].incoming_edges):
    #             neurons_dict[new_neu].outgoing_edges.remove(neu)
    #         del neurons_dict[neu]
    #         del incoming_exhausted_dict[neu]
    #         edge_list.remove(neu)
    #         for gene in genes_list[:]:
    #             if gene['sink_ID']==neu:
    #                 genes_list.remove(gene)
    #         print(neu)
    #     elif neu[0]=='I' and (len(list(neurons_dict[neu].incoming_edges))==0):
    #         for new_neu in list(neurons_dict[neu].outgoing_edges):
    #             neurons_dict[new_neu].incoming_edges.remove(neu)
    #         del neurons_dict[neu]
    #         del incoming_exhausted_dict[neu]
    #         edge_list.remove(neu)
    #         for gene in genes_list[:]:
    #             if gene['source_ID']==neu:
    #                 genes_list.remove(gene)
    #                 incoming_exhausted_dict[gene['sink_ID']].remove(neu)
    #detect 3-cycle(only works if no. of internal neurons<=3
    for neu in list(neurons_dict.keys())[:]:
        count=0
        if neu[0]=='I':
            count+=1
            for next in list(neurons_dict[neu].outgoing_edges)[:]:
                if next[0]=='I':
                    #print(neurons_dict[neu].outgoing_edges)
                    #print(neurons_dict.keys())
                    for next1 in list(neurons_dict[next].outgoing_edges)[:]:
                        if next1[0] == 'I':
                            for next2 in list(neurons_dict[next1].outgoing_edges)[:]:
                                if next2 ==neu:
                                    #directed cycle detected
                                    #break I1-I2 connection
                                    print('directed cycle detected!')
                                    if 'I2' in neurons_dict['I1'].outgoing_edges:
                                        neurons_dict['I1'].outgoing_edges.remove('I2')
                                        neurons_dict['I2'].incoming_edges.remove('I1')
                                        for gene in genes_list[:]:
                                            if gene['source_ID']=='I1' and gene['sink_ID']=='I2':
                                                genes_list.remove(gene)
                                                break
                                        incoming_exhausted_dict['I2'].remove('I1')
                                        neurons_dict, incoming_exhausted_dict, edge_list, genes_list = useless_internal_neuron_detection(neurons_dict, incoming_exhausted_dict, edge_list, genes_list)
                                    elif 'I1' in neurons_dict['I2'].outgoing_edges:
                                        neurons_dict['I2'].outgoing_edges.remove('I1')
                                        neurons_dict['I1'].incoming_edges.remove('I2')
                                        for gene in genes_list[:]:
                                            if gene['source_ID']=='I2' and gene['sink_ID']=='I1':
                                                genes_list.remove(gene)
                                                break
                                        incoming_exhausted_dict['I1'].remove('I2')
                                        neurons_dict, incoming_exhausted_dict, edge_list, genes_list = useless_internal_neuron_detection(neurons_dict, incoming_exhausted_dict, edge_list, genes_list)
        if count==1:
            break
    for neu in list(incoming_exhausted_dict.keys())[:]:
        if neu not in list(neurons_dict.keys())[:]:
            del incoming_exhausted_dict[neu]
    # # Detect and break cycles
    # cycle_detected = True
    # while cycle_detected:
    #     cycle_detected = False
    #     for neu in list(neurons_dict.keys())[:]:
    #         forming_chain = []
    #         visited = set()
    #         if neu[0] == 'I':  # neu is internal neuron
    #             found, forming_chain = detect_cycle(neurons_dict, neu, forming_chain, visited)
    #             if found:
    #                 cycle_start = forming_chain[-1]
    #                 cycle = forming_chain[forming_chain.index(cycle_start):]
    #                 remove_random_edge_from_cycle(neurons_dict, incoming_exhausted_dict, cycle)
    #                 cycle_detected = True
    #                 break

    # # detecting 3 or 4 cycle
    # for neu in list(neurons_dict.keys())[:]:
    #     forming_chain=[]
    #     flag=False
    #     ultimate_flag=False
    #     if neu[0]=='I': #neu is internal neuron
    #         forming_chain.append(neu)
    #         for next in neurons_dict[neu].outgoing_edges:
    #             for next_again in neurons_dict[next].outgoing_edges:
    #                 if next_again[0]=='I':
    #                     flag=True
    #             if next[0]=='I' and flag is True:
    #                 forming_chain.append(next)
    #                 for next2 in neurons_dict[next].outgoing_edges:
    #                     if next2[0]=='I':
    #                         forming_chain.append(next2)
    #                         for next3 in neurons_dict[next2].outgoing_edges:
    #                             if next3[0] == 'I':
    #                                 forming_chain.append(next3)
    #             flag=False



    # for gene in genes_list[:]:
    #     if (gene['source_ID']+gene['sink_ID']) not in numbering_dict.keys():
    #         numbering_dict[gene['source_ID']+gene['sink_ID']]=0
    #     numbering_dict[gene['source_ID'] + gene['sink_ID']]+=1
    # for gene_combo in list(numbering_dict.keys())[:]:
    #     if len(gene_combo)==4:
    #         input_neu=gene_combo[:2]
    #         output_neu=gene_combo[2:3]
    #     elif len(gene_combo)==5:
    #         input_neu = gene_combo[:3]
    #         output_neu = gene_combo[3:4]
    #     for gene in genes_list[:]:
    #         if gene['source_ID']==input_neu and gene['sink_ID']==output_neu and numbering_dict[gene_combo]-1>0:
    #             print(numbering_dict[gene_combo]-1)
    #             genes_list.remove(gene)
    #             numbering_dict[gene_combo]-=1
    #             incoming_exhausted_dict[gene['sink_ID']].remove(input_neu)
    #             neurons_dict[gene['sink_ID']].incoming_edges.remove(input_neu)
    #             neurons_dict[gene['source_ID']].outgoing_edges.remove(output_neu)
    # print(numbering_dict)



    # for neu in list(numbering_dict.keys())[:]:
    #     for gene in genes_list[:]:
    #         for i in range(numbering_dict[neu] - 1):




        # for gene in genes_list[:]: #itterate over a copy of list
        #     if gene['sink_ID']==neu and gene['source_ID']==neu:
        #         genes_list.remove(gene)
        #         incoming_exhausted_dict[neu].remove(neu)
        #         neurons_dict[neu].incoming_edges.remove(neu)
        #         neurons_dict[neu].outgoing_edges.remove(neu)

    for name in neurons_list:
        if name not in list(neurons_dict.keys()):
            useless_neurons_list.append(name)
    #print('incoming:',incoming_exhausted_dict)
    return neurons_dict,incoming_exhausted_dict,useless_neurons_list,genes_list,edge_list

class neuron:
    def __init__(self,name,incoming_edges,outgoing_edges):
        self.activation=0.0
        self.name=name
        self.incoming_edges=incoming_edges
        self.outgoing_edges=outgoing_edges


class brain:
    def __init__(self,genes_hexa_list,genes_list,edge_list,neurons_dict,input_neurons_list,output_neurons_list,incoming_exhausted_dict):
        self.genes_hexa_list=genes_hexa_list
        self.genes_list=genes_list
        self.edge_list=edge_list
        self.neurons_dict=neurons_dict
        self.input_neurons_list=input_neurons_list
        self.output_neurons_list=output_neurons_list
        self.incoming_exhausted_dict=incoming_exhausted_dict

    '''
    in this forward propogation algo we are assuming that internal neuron--->internal neuron
    is an identity function(despite any connection weights or anything
    '''
    def forward_propagation(self):
        # already solved these problems:
        # bidirectional connections,multi unidirectional connections, connection from
        # one gene to same gene,if incoming connection from internal neuron=0 => remove it,
        # if outgoing connection from internal neuron=> remove it.
        # basic principle of forward propogation after this:
        # start from input neurons
        # multiply the connection weights with input neuron activation and sum it over to
        # sink neuron,now do the same if self.exhausted_incoming=[],if not then wait till it
        # becomes []
        inputs_list=self.input_neurons_list
        already_expressed_genes=[]
        outputs_set=set()
        tanh_list=[]
        stored_neurons_dict=copy.deepcopy(self.neurons_dict)
        stored_incoming_exhausted_dict=copy.deepcopy(self.incoming_exhausted_dict)
        #print(f'self.genes_list:{self.genes_list}')
        #print(f'new_genes_list:{new_genes_list}')
        #i=0
        #print("edge",self.edge_list)
        #print("wow",self.incoming_exhausted_dict)
        while len(inputs_list)!=0:
            #print('inputs_list:',inputs_list)
            for neu in inputs_list:
                for gene in self.genes_list:
                    #i+=1
                    #if i%10==0:
                        #print("wow:",self.incoming_exhausted_dict)
                    if gene['source_ID']==neu and gene not in already_expressed_genes and len(self.incoming_exhausted_dict[gene['source_ID']])==0:
                        if gene['source_ID'] not in self.input_neurons_list and gene['source_ID'] not in tanh_list:
                            self.neurons_dict[neu].activation=np.tanh(self.neurons_dict[neu].activation)
                            tanh_list.append(neu)
                            # print(self.neurons_dict[neu].activation)
                            #print(f'tanh_list:{tanh_list}')
                            #print("=================================================")
                        #print(f'neu:{neu}')
                        #print(f'inputs_list:{inputs_list}')
                        #print(f'outputs_list:{outputs_set}')
                        self.neurons_dict[gene['sink_ID']].activation+=gene['connection_weight']*self.neurons_dict[neu].activation
                        #print('self.incoming_exhausted_dict:',self.incoming_exhausted_dict)
                        #print('gene[sink_ID]:',gene['sink_ID'])
                        #print('neu:',neu)
                        self.incoming_exhausted_dict[gene['sink_ID']].remove(neu)
                        already_expressed_genes.append(gene)
                        outputs_set.add(gene['sink_ID'])
                        #print(self.neurons_dict[neu].activation)
                        #print(gene['sink_ID'])
                    if gene['source_ID'] == neu and gene not in already_expressed_genes and len(self.incoming_exhausted_dict[gene['source_ID']]) != 0:
                        outputs_set.add(gene['source_ID'])
                        #print(f'neu:{neu}')
                        #print(f'outputs_set:{outputs_set}')
                        #print(self.incoming_exhausted_dict[gene['source_ID']])
                        #print(f'outputs_list:{inputs_list}')
                        #print("============================================")
            outputs_list = list(outputs_set)
            inputs_list=outputs_list
            #print(inputs_list)
            outputs_set=set()
        for edge in self.edge_list:
            if (edge[0]=='I' or 'O') and edge not in tanh_list:
                #print(self.neurons_dict[edge],edge)
                self.neurons_dict[edge].activation = np.tanh(self.neurons_dict[edge].activation)
                #print(f'outputs_list:{outputs_set}')
                #print("==================================")
        #for neu in self.output_neurons_list:
            #print(self.neurons_dict[neu].activation)
        #print("=========================================")
        return stored_neurons_dict,stored_incoming_exhausted_dict