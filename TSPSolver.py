#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


import time
import numpy as np
from TSPClasses import *
import heapq
import itertools
import matrixSolver


class TSPSolver:
    def __init__(self, gui_view):
        self._scenario = None

    def setupWithScenario(self, scenario):
        self._scenario = scenario

    ''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

    def defaultRandomTour(self, time_allowance=60.0):
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        bssf = None
        start_time = time.time()
        while not foundTour and time.time()-start_time < time_allowance:
            # create a random permutation
            perm = np.random.permutation(ncities)
            route = []
            # Now build the route using the random permutation
            for i in range(ncities):
                route.append(cities[perm[i]])
            bssf = TSPSolution(route)
            count += 1
            if bssf.cost < np.inf:
                # Found a valid route
                print("TOUR: ", route)
                foundTour = True
        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results

    ''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

    def greedy(self, time_allowance=60.0):
        pass

    ''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''

    def branchAndBound(self, time_allowance=60.0):

        count = 0
        pruned = 0
        results = self.defaultRandomTour()
        cities = self._scenario.getCities()
        t0 = time.process_time()
        S = []  # heap
        oCity = cities[0]
        firstCityMatrix = matrixSolver.matrixSolver(
            cities, None, None, None, oCity)
        total = 1
        # create initial state
        # insert first state in heap
        heapq.heappush(S, firstCityMatrix)
        # while loop (while heap is not empty or a for loop)
        while len(S) != 0:
            t1 = time.process_time() - t0
            curr = heapq.heappop(S)
            # check time
            if t1 >= time_allowance:
                print("MAX TIME MET! || pruned: ", pruned,
                      " || Length of unvisited nodes: ", len(curr.unvisited))
                break
            # another for loop checking all the cities that haven't been visited by the current state
            for unvisitedCity in curr.unvisited:
                # if the cost of travelling to that city (computed in the matrixSolver) is less than bssf
                testingCityMatrix = matrixSolver.matrixSolver(
                    cities, curr.fromCity, unvisitedCity, curr, firstCityMatrix)
                total += 1
                if testingCityMatrix.cost < results['cost']:
                    heapq.heappush(S, testingCityMatrix)
                    # add to the heap (including priority)
                else:
                    pruned += 1
                    # otherwise, update the pruned objects
            # if visited is empty
            if len(curr.unvisited) == 0:
                # then check that you can get back to initial city
                backToFirst = matrixSolver.matrixSolver(
                    cities, curr.fromCity, oCity, curr, oCity)
                total += 1
                # update bssf
                if backToFirst.cost < results['cost']:
                    tN = time.process_time() - t0
                    print("TN: ", tN, " || cost: ",
                          backToFirst.cost, " || pruned: ", pruned)
                    count += 1
                    # add current city/path everything to solutions list
                    # 		results['cost'] = bssf.cost if foundTour else math.inf
                    # 		results['time'] = end_time - start_time
                    # 		results['count'] = count
                    # 		results['soln'] = bssf
                    # 		results['max'] = None
                    # 		results['total'] = None
                    # 		results['pruned'] = None
                    results['cost'] = backToFirst.cost
                    results['time'] = tN
                    print("VISITED: ", backToFirst.visited)
                    ss = TSPSolution(backToFirst.visited)
                    results['soln'] = ss
                    results['total'] = total
                    results['max'] = None
                    results['count'] = count
                    results['pruned'] = pruned
                # update 'count' in result (to tell us how many solutions there are)
        return results
        pass

    ''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''

    def fancy(self, time_allowance=60.0):
        pass
