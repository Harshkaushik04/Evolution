import numpy as np
import pygame
import copy

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

def neurons_dict(genes_list,activation_inputs_dict,num_neurons,edge_list):
    neurons_dict={}
    incoming_exhausted_dict={}
    neurons_list=[]
    useless_neurons_list=[]
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
            neurons_dict[name].activation=activation_inputs_dict[name]
        incoming_exhausted_dict[name]=incoming_edges
    for neu in list(neurons_dict.keys())[:]:
        if neu[0]=='I' and (len(neurons_dict[neu].outgoing_edges)==0):
            del neurons_dict[neu]
            del incoming_exhausted_dict[neu]
            edge_list.remove(neu)
            for gene in genes_list[:]:
                if gene['sink_ID']==neu:
                    genes_list.remove(gene)
        elif neu[0]=='I' and (len(neurons_dict[neu].incoming_edges)==0):
            del neurons_dict[neu]
            del incoming_exhausted_dict[neu]
            edge_list.remove(neu)
            for gene in genes_list[:]:
                if gene['source_ID']==neu:
                    genes_list.remove(gene)
                    incoming_exhausted_dict[gene['sink_ID']].remove(neu)
        # for gene in genes_list[:]: #itterate over a copy of list
        #     if gene['sink_ID']==neu and gene['source_ID']==neu:
        #         genes_list.remove(gene)
        #         incoming_exhausted_dict[neu].remove(neu)
        #         neurons_dict[neu].incoming_edges.remove(neu)
        #         neurons_dict[neu].outgoing_edges.remove(neu)
    for name in neurons_list:
        if name not in list(neurons_dict.keys()):
            useless_neurons_list.append(name)
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
                        if gene['source_ID'] not in self.input_neurons_list:
                            self.neurons_dict[neu].activation=np.tanh(self.neurons_dict[neu].activation)
                            tanh_list.append(neu)
                            #print(self.neurons_dict[neu].activation)
                            #print(f'tanh_list:{tanh_list}')
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


