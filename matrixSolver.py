import math


class matrixSolver:
    def __init__(self, gCityList, fromCity=None, nextCity=None, Gstate=None, firstCity=None):
        # first call, pass in cityMatrix and firstCity, the rest will be none
        # fromCity is previous, not current
        self.state = Gstate
        self.firstCity = firstCity
        self.nextCity = nextCity
        self.fromCity = fromCity
        self.cityList = gCityList
        self.matrix = None
        self.visited = []
        self.unvisited = []
        distance = 0
        self.cost = 0
        if self.nextCity == None:
            # we are on the first city, and need to only create the state and return it
            self.matrix = self.firstCityMatrix(gCityList)
            # self.print2DMatrix(self.matrix)
            # cost stays 0 in this case, gets updated by state.cost in all others
            self.visited.append(firstCity)
            for givenCity in gCityList:
                self.unvisited.append(givenCity)
            self.unvisited.remove(firstCity)
            self.fromCity = firstCity
        else:
            # print("Going from: ", fromCity._index, " To: ",
            #       nextCity._index, " || total visited: ", len(self.visited))
            edgeLength = self.state.matrix[fromCity._index][nextCity._index]
            # print("RAW:")
            # self.print2DMatrix(self.state.matrix)
            self.matrix = self.updateDistanceVisited(
                self.state.matrix, fromCity, nextCity)
            # print("blocked:")
            # self.print2DMatrix(self.matrix)
            self.matrix, distance = self.updateDistance(self.matrix)
            # print("Reduced:")
            # self.print2DMatrix(self.matrix)
            # print("Cost of reduction:", distance, " edge length: ", edgeLength)
            for givenCity in Gstate.visited:
                self.visited.append(givenCity)
            for givenCity in Gstate.unvisited:
                self.unvisited.append(givenCity)
            # self.unvisited = Gstate.unvisited
            if nextCity != firstCity:
                self.unvisited.remove(nextCity)
                self.visited.append(nextCity)
            self.cost = self.state.cost
            self.cost += distance + edgeLength
            self.fromCity = nextCity

            # distance added to cost currently (I assume)
        # current cost/distance updated by state.cost

    def print2DMatrix(self, matrix):
        print("\n---------------\n")
        print('\n'.join(['\t'.join([str(cell) for cell in row])
              for row in matrix]))
        print("\n---------------\n")

    def updateDistance(self, state):
        size = 0
        # just push to new state and return that state instead of trying to update existing one. gross.
        updatedState = []
        finalState = []

        additionalDistance = 0

        for q in range(len(state)):
            col = []
            for s in range(len(state)):
                col.append(0)
            updatedState.append(col)
            finalState.append(col)
        outer = 0
        inner = 0
        for i in state:
            smallestRow = math.inf
            for r in i:
                if smallestRow > r:
                    smallestRow = r
            for nr in i:
                if smallestRow != math.inf and nr != math.inf:
                    temp = nr - smallestRow
                else:
                    temp = math.inf
                updatedState[outer][inner] = temp
                inner += 1
            if smallestRow != math.inf:
                # if additional distance is infinity, that means the route is impossible.
                additionalDistance += smallestRow
            size += 1
            inner = 0
            outer += 1
        outer = 0
        inner = 0
        temp = 0
        for j in range(len(updatedState)):
            smallestColumn = math.inf
            for c in updatedState:
                # print("c: ", c, " c[j]: ", c[j], " smallestColumn: ", smallestColumn)
                if smallestColumn > c[j]:
                    smallestColumn = c[j]
            for nc in updatedState:
                if smallestColumn != math.inf and nc != math.inf:
                    temp = nc[j] - smallestColumn
                else:
                    temp = math.inf
                finalState[inner][outer] = temp
                inner += 1
            if smallestColumn != math.inf:
                additionalDistance += smallestColumn
            outer += 1
            inner = 0
        # print("updatedState after columns: ", finalState)
        return finalState, additionalDistance
        # take the smallest number in the row, subtract whole row
        # take the smallest number in the column, subtract whole column

    def updateDistanceVisited(self, state, fromCity, toCity):
        # infinity out the current city and next city (to)
        copyState = []
        # make a copy
        for i in range(len(state)):
            newRow = []
            for j in range(len(state)):
                newRow.append(state[i][j])
            copyState.append(newRow)

        # city._index will give the index lolz
        for i in range(len(copyState)):
            # FROM
            copyState[i][toCity._index] = math.inf
        for j in range(len(copyState)):
            copyState[fromCity._index][j] = math.inf
        copyState[toCity._index][fromCity._index] = math.inf
        return copyState

    # def priority(self):
    #     # update priority (of next city) and return it
    #     ret = 0
    #     ret = cost/len(visited)
    #     return ret

    def firstCityMatrix(self, cities):
        matrix = []
        for q in range(len(cities)):
            col = []
            for s in range(len(cities)):
                col.append(0)
            matrix.append(col)
        iI = 0
        iJ = 0
        for i in cities:
            for j in cities:
                matrix[iI][iJ] = i.costTo(j)
                iJ += 1
            iI += 1
            iJ = 0
        # print(state)
        return matrix

    def returnUnvisited(self, cities):
        unvisited = []
        for i in cities:
            for j in self.visited:
                if i == j:
                    continue
            unvisited.append(i)
        return unvisited

    # def toString(self):
    #     ret = []
    #     # ret += self.state
    #     # ret += '\n'
    #     # ret += self.firstCity
    #     # ret += '\n'
    #     # ret += self.nextCity
    #     # ret += '\n'
    #     # ret += self.fromCity
    #     # ret += '\n'
    #     # ret += self.cityMatrix
    #     return ret

    def __lt__(self, nxt):
        return self.cost/len(self.visited) > nxt.cost/len(nxt.visited)
