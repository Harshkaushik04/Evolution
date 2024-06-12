8th june 2024:
i have (hopefully)implemented the genes hexadecimal all the way upto genes list and
brain.Many obstacles came like bidirectional connections,self connected nodes,etc in
forward propagation of brain, which i resolved by adding some objects like
incoming_exhausted_list,etc.

also made circle,player,env,neuron,brain classes(env not much useful till now, may
use in future)
-neuron class is for representation of a neuron of brain
-brain contains the network of neurons(not graph, but contains all the
edges list-genes_list,so can make graph through it)
-circle basically is a pseudo representation of a pygame circle object and we can
make pygame circle anytime by using its function .draw()
-player is basically the "outermost" class and contains all the information about
the "player" including its brain,its pygame object,its genes_list,direction,color
and co-ordinates list
-env is not much used yet

players_list contains all the players
-main() worked perfectly for making graph of a configuration and pygame was able
to simulate(place) all the players on screen

upcoming work:
1. sense function-for sensory neurons
2. update function+change function-for output neurons,will do forward propagation and change so will need the
input of sense function:input_activations
3. replicate function- at the end of each generation replicate and also a mutation
factor.
4. condition- the condition is most important for observing the evolution since
it decides whom gets to replace or survive
eg. 1. all the players on left side of the screen dies and all on right side survives
    2. radioactivity
5. kill output neuron
6. maybe add new features like strength,social relations,not kill infront of
others but can kill otherwise,etc

9th june 2024:
1. completed sense and update function
2. introduced a very important parameter: size_parameter and did all the modifications in the
code according to that.
3. did bug fix for 2 players co-inciding symmetrically and wall-player co-inciding

to do tomorrow:
1. further bugfix the co inciding problem since we only considered, for example my_player
is moving right and player is there so only wrote 2 conditions which were for x direction
but we have to write 2 more conditions for y direction(since if y of my_player and player
are very different then they will not coincide)
2. correct the position_errors_resolve function
3. complete change and replicate function,make condition: run simulation

12th june 2024:
simulation is running on condition that all players on east side(50 percent dies),
improvements needed in code:
1. better boundaries of each player so they dont come into each others boundary
2. every time generation starts,make population to {default population} and not to a
'convenient' number, as it reduces the effectiveness of evolution actual impact.
3. high mutation rate