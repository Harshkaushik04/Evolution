# input is 8 digit hexadecimal number converted to 32 digit binary
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import copy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the desired logging level

# Create a logger
logger = logging.getLogger(__name__)
def hexadecimal_to_binary(hex_value,binary_length=32):
    binary_value = bin(int(hex_value, 16))[2:].zfill(binary_length)
    return binary_value
# state_at_error={}
# l=[4,5,6,7,0,1]
# checkpoint = {}
# for i in range(6):
#     try:
#         result=1
#         # Some critical operation
#         result+=1/l[i]
#         # Save checkpoint
#         checkpoint = {'i': i, 'result': result}
#     except Exception as e:
#         logger.error(f"Error occurred at iteration {i}: {e}")
#         # Recover state from the last checkpoint
#         i = checkpoint['i']
#         result = checkpoint['result']
#         #print(checkpoint['result'])
#         break  # Exit the loop or handle the error appropriately

mutation_prob=0.5
decider=[0,1]
# inp=random.choices(decider,weights=[1-mutation_prob,mutation_prob])
# print(inp==[1])
# s=['a']

# change_decider=['1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
# char_to_change=random.choices(change_decider,weights=np.ones(15)/15)
# print(char_to_change)
# dict={'wow':[2,3]}
# dict['wow']=[5,6]
# print(type(dict.keys()))
# l=list(dict.keys())
# print(type(l))
# print(l)

# for i in range(1,14):
#     print(f'{i}. S{i}:')
# class wow:
#     def __init__(self,l,dicti):
#         self.l=l
#         self.dicti=dicti
#
#
# hi1=wow(5,{'wow':3})
# hi2=wow([4,5,6],{})
#
# new1=copy.deepcopy(hi1.l)
# new2=copy.deepcopy(hi1.dicti)

# hi1.l=1
# hi1.dicti['wow']=9
# print(new1)
# print(new2)
# #print(hi1!=hi2)
# new_var=hi1.new
# new_var=4
# print(hi1.new)
#print(pow(11,2))
# hi=wow(new=2)
# l=[hi,'wow']
# for i in l[:]:
#     l.remove(i)
# print(l)
# a=1
# b=2
# c=3
# print(min(a,b,c))
# x=1
# y='abc'
# z=5
# l=[x,y,z]
# l[0]=2
# print(x)

# l1=[1,2,3]
# l2=l1
# l1=[5,6,7]
# l3=[100,120]
# l3=l1
# print(l2)
# print(l3)

#print(type(hexadecimal_to_binary('f1351fe3')))

# dicti={'hi1':hi1,'hi2':hi2}
# print(type(dicti))
# assert(type(dicti)==dict)
# #for player_name,player in dicti.items():
#     #del dicti[player_name]  #gives error
# print(dicti)
# l=[1,2,3]
# new=random.choices(l,weights=np.ones(3)/3)
# # print(new,type(new))
# print(5 not in [i for i in range(5)])
# x={'wow':6}
# del x
# x={'wow':7}
# print(x)
# print(1)
# print('\n')
# print(2)