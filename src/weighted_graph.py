import heapq
import math
from vertex import Vertex


class WeightedGraph(object):
    def __init__(self):
        self._vertices = []
        self._adjMat = {}

    def nVertices(self):
        return len(self._vertices)

    def nEdges(self):
        return len(self._adjMat) // 2

    def addVertex(self, vertex):
        self._vertices.append(vertex) #this one

    def validIndex(self, n):
        if n < 0 or self.nVertices() <= n:
            raise IndexError
        return True

    def getVertex(self, n):
        if self.validIndex(n):
            return self._vertices[n]

    def addEdge(self, A, B, w): #this one
        self.validIndex(A)
        self.validIndex(B)
        if A == B:
            raise ValueError
        self._adjMat[A, B] = w
        self._adjMat[B, A] = w

    def hasEdge(self, A, B):
        return ((A, B) in self._adjMat and  #this one
                self._adjMat[A, B] < math.inf)

    def edgeWeight(self, A, B):
        self.validIndex(A)
        self.validIndex(B)
        return (self._adjMat[A, B] if (A, B) in self._adjMat
                else math.inf)

    def adjacentVertices(self, n):
        self.validIndex(n)
        for j in range(self.nVertices()):
            if j != n and self.hasEdge(n, j):
                yield j

    def shortestPath(self, start, end):
        dist = {u: float('inf') for u in range(self.nVertices())}
        parent = {u: None for u in range(self.nVertices())}
        dist[start] = 0
        pq = [(0, start)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue
            if u == end:
                break
            for v in self.adjacentVertices(u):
                w = self.edgeWeight(u, v)
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    parent[v] = u
                    heapq.heappush(pq, (nd, v))
        
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        
        if path[0] != start:
            return []
        
        return path
    
    def letters_instead_of_indexes(self, path):
        return [self.getVertex(i).name for i in path]
    
    def total_time (self, path):
        total = 0
        for i in range(len(path) - 1):
            total += self.edgeWeight(path[i], path[i+1])
        return total