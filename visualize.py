hi=['2c4352bd', 'fa499428', '386b6fca', 'aa5c5b1b', '996391db', '121f936d', '7f3beffb', 'f871d3bf', 'ed9637c7', '23f5e3f7', 'ab7e1846', 'c6af7124', '56d2dd5b', 'ffbe6a36', 'fcd31dbd', 'dc825a95']
hi2=['a8e3dcaf', '41adc125', 'bd3ab6cd', '3f8a4d55', '5d93ba89', '1b9215f4', '216d4ff1', 'cb85ac8f', '8b74fba1', 'e783653c', '8eca2c68', '23661436', 'dcd3a98a', '89e7aa4c', '95e15f89', '1e2ae369']
hi3=['f9527813', '2adaf8a5', 'fb758248', '46d2e4b2', 'a7d47942', 'b5d72ec2', 'd233ea44', 'fb71745a', 'b835328f', 'e35afb13', '17d9fcfb', '4eb2ac4f', 'd7bb8599', '17f482f7', '12263247', '2636cee2']
from useful_functions import graph_visuals,genes_hexa_list_to_genes_list
wow=genes_hexa_list_to_genes_list(hi,[11,4,6])
wow2=genes_hexa_list_to_genes_list(hi2,[11,4,6])
wow3=genes_hexa_list_to_genes_list(hi3,[11,3,6])
# flag=False
# for gene in wow:
#     if gene['source_ID']=='O2':
#         print(gene)
#         flag=True
# if not flag:
#     print('no')
# print(wow)
graph_visuals(wow3)