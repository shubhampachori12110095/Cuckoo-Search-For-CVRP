from CVRP import CVRPInfo as CVRP
import operator as o
import math
import random
from copy import deepcopy
from scipy.stats import levy

class CuckooSearch:
    """
    For this implementation of Cuckoo Search for the CVRP, the given pseudocode will be followed:
    - Initialize randomly generated solutions
    - With fraction Pc (fraction of cuckoos to perform levy flights), randomly select a cuckoo to
      perform levy flights. If the new solution found is better than a randomly selected nest, 
      replace the randomly selected nest.
    - The worse Pa (fraction of nest to be abandoned) nests will be replaced with randomly generated solutions
    - Rank solutions
    - Keep best solutions
    """


    def __init__(self, CVRPInstance, numCuckoos = 15, Pa = 0.2, Pc = 0.6, generations = 5000, pdf_type = 'levy'):
        self.instance = CVRPInstance
        self.Pa = Pa
        self.Pc = Pc
        self.generations = generations
        self.pdf_type = pdf_type
        self.numCuckoos = numCuckoos
        self.nests = []
        random.seed()
        self.solveInstance()
        

    def solveInstance(self):
        
        # Initialize Solutions
        for i in range(self.numCuckoos):
            sol = self.instance.create_random_solution() # Initialize Solution
            self.nests.append(sol)
        
        for i in range(self.generations):   
            print('DEBUG: Generation num: ' + str(i))

            # sort nests by cost
            self.nests.sort(key = o.attrgetter('cost'))
            best_solution = self.nests[0]
            random.shuffle(self.nests)

            # Search, and Evaluate with fraction Pc of Cuckoos
            for j in range(math.floor(self.numCuckoos * self.Pc)):
                print('DEBUG: Levy Flights iteration number ' + str(j))
                self.__performLevyFlights(self.nests[j])
                print('DEBUG: Levy Flights iteration number ' + str(j) +  ' success')
            

                # Randomly select another nest to compare with, 
                # Is Fi > Fj? replace

    def __performLevyFlights(self, nest):
        # Generate random value x from levy 
        # According to randomly generated value, perform 2-opt x time or double-bridge

        # temporary random num gen
        r = random.random()
        
        twoOptIter = 0
        doubleBridgeIter = 0
        if r >= 0 and r <= 0.2:
            twoOptIter = 1
        elif r > 0.2 and r <= 0.4:
            twoOptIter = 2
        elif r > 0.4 and r <= 0.6:
            twoOptIter = 3
        elif r > 0.6 and r <= 0.8:
            twoOptIter = 4
        elif r > 0.8 and r <= 1.0:
            doubleBridgeIter = 1
        
        for i in range(twoOptIter):
            print('DEBUG: Levy Flights twoOpt')
            nest = self.__twoOptInter(nest)

        for i in range(doubleBridgeIter):
            print('DEBUG: Levy Flights doubleBridge')
            nest = self.__doubleBridgeInter(nest)
        
        # validate nest
        # nest.
        # recalculate nest 

    def __twoOptInter(self, sol): 
        # takes solution as input
        # gets 2 routes randomly
        # Select random node from each
        # Swap nodes, until valid route is generated
        numRoutes = len(sol.routes) # sol.routes - list

        # Randomly select 2 routes to swap
        r1 = random.randrange(0,numRoutes)
        r2 = random.randrange(0,numRoutes)

        # Check if n2 == n1. If true, generate new value for n2.
        while r2 == r1: 
            r2 = random.randrange(0,numRoutes)

        # Perform Swap
        IsSwapInvalid = True
        while IsSwapInvalid:
            # Temporary variables for checking if swap is valid
            _solr1 = deepcopy(sol.routes[r1])
            _solr2 = deepcopy(sol.routes[r2])
            # Randomly select nodes to swap from each route
            n1 = random.randrange(1, len(_solr1.route) - 1) # start with 1 to disregard depot
            n2 = random.randrange(1, len(_solr2.route) - 1)

            _ = _solr1.route[n1]
            _solr1.route[n1] = _solr2.route[n2]
            _solr2.route[n2] = _

            if _solr1.demand <= self.instance.capacity:
                if _solr2.demand <= self.instance.capacity:
                    sol.routes[r1] = _solr1
                    sol.routes[r2] = _solr2
                    IsSwapInvalid = False
        return sol

    def __doubleBridgeInter(self, sol):
        # takes solution as input
        # gets 4 routes randomly
        # Select random node from each
        # Swap nodes, until valid route is generated
        numRoutes = len(sol.routes) # sol.routes - list

        # Randomly select 4 routes to swap
        r = list(range(numRoutes))
        random.shuffle(r)
        r1, r2, r3, r4 = r[0], r[1], r[2], r[3]
        
    
        # Perform Swap - r1 & r3, r2 & r4
        IsSwapInvalid = True
        while IsSwapInvalid:
            # Temporary variables for checking if swap is valid
            _solr1 = deepcopy(sol.routes[r1])
            _solr2 = deepcopy(sol.routes[r2])
            _solr3 = deepcopy(sol.routes[r3])
            _solr4 = deepcopy(sol.routes[r4])
            # Randomly select nodes to swap from each route
            n1 = random.randrange(1, len(sol.routes[r1].route) - 1)
            n2 = random.randrange(1, len(sol.routes[r2].route) - 1)
            n3 = random.randrange(1, len(sol.routes[r3].route) - 1)
            n4 = random.randrange(1, len(sol.routes[r4].route) - 1)

            _ = sol.routes[r1].route[n1]
            sol.routes[r1].route[n1] = sol.routes[r3].route[n3]
            sol.routes[r3].route[n3] = _
            _ = sol.routes[r2].route[n2]
            sol.routes[r2].route[n2] = sol.routes[r4].route[n4]
            sol.routes[r4].route[n4] = _

            if _solr1.demand <= self.instance.capacity:
                if _solr2.demand <= self.instance.capacity:
                    if _solr3.demand <= self.instance.capacity:
                       if _solr4.demand <= self.instance.capacity:
                            sol.routes[r1] = _solr1
                            sol.routes[r2] = _solr2
                            sol.routes[r3] = _solr3
                            sol.routes[r4] = _solr4
                            IsSwapInvalid = False

        return sol

    def __repr__(self):
        pass
        # return filename, 
        # string = {
        #     "Name" : self.instance.,
        #     "listDemand" : self.listDemand,
        #     #"dists"  : self.dist
        # }
        # return str(string)
    