import math
from collections import defaultdict


def hexadecimal_to_binary(hex_value, binary_length=32):
    return bin(int(hex_value, 16))[2:].zfill(binary_length)


def gene_to_unprocessed_data(hex_value):
    binary = hexadecimal_to_binary(hex_value, binary_length=32)
    gene_data = {
        'source_type': int(binary[0]),
        'source_ID': int(binary[2:9], 2),
        'sink_type': int(binary[9]),
        'sink_ID': int(binary[10:17], 2),
        'connection_weight': int(binary[17:32], 2)
    }
    return gene_data


def unprocessed_data_to_processed_data(gene_data, num_sensory, num_internal, num_output, normalization_factor=8000):
    if gene_data['source_type'] == 0:
        gene_data['source_type'] = 'sensory_neuron'
        gene_data['source_ID'] %= num_sensory
    elif gene_data['source_type'] == 1:
        gene_data['source_type'] = 'internal_neuron'
        gene_data['source_ID'] %= num_internal

    if gene_data['sink_type'] == 0:
        gene_data['sink_type'] = 'output_neuron'
        gene_data['sink_ID'] %= num_output
    elif gene_data['sink_type'] == 1:
        gene_data['sink_type'] = 'internal_neuron'
        gene_data['sink_ID'] %= num_internal

    gene_data['connection_weight'] /= normalization_factor
    return gene_data


class Neuron:
    def __init__(self, neuron_type, neuron_id):
        self.neuron_type = neuron_type
        self.neuron_id = neuron_id
        self.activation = 0.0
        self.incoming_edges = []
        self.outgoing_edges = []

    def activate(self, value):
        self.activation = value

    def apply_activation_function(self, input_sum):
        self.activation = math.tanh(input_sum)


class NeuralGraph:
    def __init__(self):
        self.neurons = defaultdict(dict)
        self.adjacency_list = defaultdict(list)

    def add_neuron(self, neuron_type, neuron_id):
        if neuron_id not in self.neurons[neuron_type]:
            self.neurons[neuron_type][neuron_id] = Neuron(neuron_type, neuron_id)
        return self.neurons[neuron_type][neuron_id]

    def add_edge(self, from_type, from_id, to_type, to_id, weight):
        from_neuron = self.add_neuron(from_type, from_id)
        to_neuron = self.add_neuron(to_type, to_id)

        from_neuron.outgoing_edges.append((to_neuron, weight))
        to_neuron.incoming_edges.append((from_neuron, weight))
        self.adjacency_list[(from_type, from_id)].append((to_type, to_id, weight))

    def set_sensory_activation(self, neuron_id, value):
        if 'sensory_neuron' in self.neurons and neuron_id in self.neurons['sensory_neuron']:
            self.neurons['sensory_neuron'][neuron_id].activate(value)


def forward_pass(neural_graph):
    for neuron_type, neurons in neural_graph.neurons.items():
        for neuron in neurons.values():
            if not neuron.incoming_edges:  # Skip sensory neurons
                continue

            input_sum = sum(in_neuron.activation * weight for in_neuron, weight in neuron.incoming_edges)
            neuron.apply_activation_function(input_sum)


# Example usage
hex_genes = [
    '1A2B3C4D',
    '2B3C4D5E',
    '3C4D5E6F',
    '4D5E6F7A'
]

num_sensory = 10
num_internal = 10
num_output = 10

neural_graph = NeuralGraph()

for hex_value in hex_genes:
    unprocessed_data = gene_to_unprocessed_data(hex_value)
    processed_data = unprocessed_data_to_processed_data(unprocessed_data, num_sensory, num_internal, num_output)

    neural_graph.add_edge(
        processed_data['source_type'], processed_data['source_ID'],
        processed_data['sink_type'], processed_data['sink_ID'],
        processed_data['connection_weight']
    )

# Set activations for sensory neurons
neural_graph.set_sensory_activation(1, 0.8)
neural_graph.set_sensory_activation(2, 0.6)

# Perform forward pass
forward_pass(neural_graph)

# Print output neuron activations
# for neuron_type, neurons in neural_graph.neurons.items():
#     for neuron_id, neuron in neurons.items():
#         print(f'Neuron {neuron_type} {neuron_id} activation: {neuron.activation}')
