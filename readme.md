Project working:
We can set any condition on survival of the simulated beings, here i have tested 3 conditions of survival and sharing the results:
1. beings which are in up 20 percent survive(Generation 1 and Generation 130)
   
![generation1](https://github.com/user-attachments/assets/05469adf-c2aa-4d7e-a4ad-44f960980d43)
![generation130](https://github.com/user-attachments/assets/b5fa4204-c15b-4c61-8e6d-c1c48e126486)

2. beings which are in left 20 percent survive(Generation 1 and Generation 130)
   
![generation1](https://github.com/user-attachments/assets/e59f5ca7-adec-4106-b2f6-6401af8793b6)
![generation130](https://github.com/user-attachments/assets/e1153fe2-15fd-448f-b249-e6215b14e1e3)

3. beings which are in middle 20 percent survive(Generation 1 and Generation 100)
   
![generation1](https://github.com/user-attachments/assets/677e37af-22e9-489b-a31c-129ed6d67f3b)
![generation100](https://github.com/user-attachments/assets/54e3c28a-8877-4a66-8390-b8881be4c810)

4. beings which are in 4 corners survive(1 corner= 0.2*total_length,0.2*total_width)(Generation 1 and Generation 110)

![generation1](https://github.com/user-attachments/assets/e6aa19b0-0a99-4ed4-bf69-fefdbbe1e0fb)
![generation110](https://github.com/user-attachments/assets/2ab6f1eb-b681-4b47-aff0-f7462c9afd31)

Progress Tracking 
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

14th june:
1.fixed a major bug which was that i had initialized co_ordiantes_history_list as
[co_ordinates_list] which is wrong because i had to deepcopy the variable and not
use the variable itself,whcih would hopefully make player collision less probable
2.also removed player_size and generalised play_size to size_parameter
3.did major bug fix with combined_rect_co_ordinates in change function
4. for the wall coincide problem, did fix by shifting the logic to the end of the
change function instead of front since, after a player does action, i can revert it

24th june:
did major bugfix in the restart_simulation function by adding an inp argument
to change input of condition function.

29th june:
did major bugfix in blockage_left_right and blockage_forward of sensory neurons

8 july:
did bugfix in tanhlist multiple repetition,working on 3-cycle avoidance in brain graph

9 july:
(major bugfix) made 3-cycle avoidance work by adding a mechanism to remove internal neuron having
no outgoing or incoming edges after the cycle avoidance code

12th july:
did major bugfix in restart_simulation function by adding basic_info argument for
much needed customization
