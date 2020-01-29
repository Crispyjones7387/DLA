# DLA
Diffusion Limited Aggregation

Algorithm:
 1. Place seed at the centre of the canvas.
 2. Release a random walker from the edge.
 3. Random walker sticks to the neighbouring sites of the seed/previous points if
    np.random.rand() < Sticking Coefficient
 4. Repeat N(particles) times.
 
![DLA Simulation for 500x500 matrix with 50,000 particles](https://github.com/Crispyjones7387/DLA/blob/master/DLA%20Sim1.png)
