import numpy as np

def viral_centrality(inList, inWeight, outList, Niter=5, beta=1.0, tol=0.0001):
    ''' User has a choice to either run each simulation until the probabilities have converged within
    a specified relative tolerance, or just iterate for 'Niter' iterations for each seed node. If Niter is less than 1, the former option is selected, and
    if Niter is 1 or greater, the latter option is selected.
    inList[i] is list of all the nodes sending connections to i; inWeight[i] is list of corresponding weights (ie transmission probabilities)
    outList[i] is  a list of all the nodes i sends connections to
    All transmission probabilities are universally multiplied by 'beta' '''

    N = len(inList)
    avg_infections = np.zeros(N)
    epsilon = 1e-10  # Small value to avoid division by zero

    if Niter < 1:
        for seed in range(N):
            prev_uninfected = np.ones(N)
            uninfected = np.ones(N)
            last_infected = np.zeros(N)
            cur_infected = np.zeros(N)
            last_infected[seed] = 1
            uninfected[seed] = 0

            t = 0
            bfs_queue = -1 * np.ones(N, dtype=int)
            bfs_queue[0] = seed
            seed_distance = -1 * np.ones(N, dtype=int)
            seed_distance[seed] = 0
            read = 0
            write = 1

            while np.nanmax((prev_uninfected[bfs_queue[0:write]] - uninfected[bfs_queue[0:write]]) / (prev_uninfected[bfs_queue[0:write]] + epsilon)) > tol:
                prev_uninfected = np.copy(uninfected)

                if read != write:
                    write_start = write
                    while read < write_start:
                        for neighb in outList[bfs_queue[read]]:
                            if seed_distance[neighb] < 0:
                                seed_distance[neighb] = t + 1
                                bfs_queue[write] = neighb
                                write += 1
                        read += 1

                for node in bfs_queue[0:write]:
                    prob_uninfected = 1
                    for con in range(len(inList[node])):
                        prob_uninfected *= (1 - (last_infected[inList[node][con]] * (beta * inWeight[node][con])))
                    cur_infected[node] = (1 - prob_uninfected) * uninfected[node]

                uninfected -= cur_infected
                last_infected = np.copy(cur_infected)
                cur_infected.fill(0)
                t += 1

            avg_infections += (1 - uninfected)

    else: #if Niter is a positive integer, then just iterate for that number of time steps
    
        for seed in range(N):
            prev_uninfected = np.ones(N) 
            uninfected = np.ones(N) #probabilty that node hasn't been infected yet. starts at one for each node
            last_infected = np.zeros(N) #probability that node was infected on last timestep
            cur_infected = np.zeros(N) #probability that node was infected on current timestep
            last_infected[seed] = 1
            uninfected[seed] = 0
            
            t = 0
            #breadth-first search (BFS)
            bfs_queue = -1 * np.ones(N, dtype=int) #first-in/first-out buffer to perform breadth-first search (see section 10.3.3 of Newman's textbook)
            bfs_queue[0] = seed
            seed_distance = -1 * np.ones(N, dtype=int) #array of distance from seed node
            seed_distance[seed] = 0
            read=0
            write=1
            while t < Niter: #in contrast to original algorithm, just iterate for fixed number of time steps
                prev_uninfected = np.copy(uninfected)
                
                #expand BFS to find next ring of nodes that are within seed node's reach (see section 10.3.3 of Newman's text)
                if read != write: #if read==write, then breadth-first search is exhausted
                    write_start = write
                    while read < write_start: #when read is equal to write_start, that signifies reaching the end of the "t+1st ring"
                        for neighb in outList[bfs_queue[read]]:
                            if seed_distance[neighb] < 0: #if distance from seed node has not yet been determined, then record it
                                seed_distance[neighb] = t+1
                                bfs_queue[write] = neighb 
                                write += 1
                        read += 1
                    
                    
                for node in bfs_queue[0:write]: #for all nodes within reach of the seed node at this point in time
                    prob_uninfected = 1 #set probability of being uninfected to one
                    for con in range(len(inList[node])): #look at each incoming connection to node
                        prob_uninfected = prob_uninfected*(1-(last_infected[inList[node][con]]*(beta*inWeight[node][con])))
                        #prob that node remains uninfected decreases as we go through each connection. beta again multiplies weights to reset max
                    cur_infected[node] = (1-prob_uninfected)*uninfected[node]
                    #prob of current infection is prob of being infected times the prob that node hasn't been infected yet
                
                for node in bfs_queue[0:write]:
                    last_infected[node] = cur_infected[node] 
                    #update our last infected list for each timestep
                    uninfected[node] = uninfected[node] - cur_infected[node]
                    #new prob of being uninfected is old prob - the prob that node is currently infected
                
                t = t+1
                    
            avg_infections[seed] = sum(1 - uninfected) - 1 #dont want to include seed node infection in total
    
    return avg_infections / N
