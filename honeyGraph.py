from sets import Set

class HNode:
  uID = None
  neighbors = None
  val = ''

  def __init__(self):
    self.neighbors = dict()

  def addNeightbor(self, val, node):
    if val in self.neighbors:
      self.neighbors[val].add(node)
    else:
      self.neighbors[val] = Set([node])


class HoneyGraph:
  graph = []
  uIDC = 0

  def setup(self, n,data): 
    # Load nodes
    for row in range(0,n):
      currentRow = data[row]
      hRow = []
      for i in currentRow:
        node = HNode()
        node.uID = self.uIDC
        self.uIDC += 1
        node.val = i
        hRow.append(node)
      self.graph.append(hRow)

    for row in range(0,n):
      currentRow = self.graph[row]
      nextRow = None
      if row < n-1:
        nextRow = self.graph[row+1]

      self.loadRowNeighbors(currentRow)
      if row < n-1:
        self.loadNextRowNeighborsVerts(currentRow, row, nextRow)
        if row > 1:
          self.loadNextRowNeighborsSide(currentRow, row, nextRow)

    for n in self.graph:
      for i in n:
        print i. uID
        print i.val
        print i.neighbors
        print "-------------"
        
  def loadRowNeighbors(self, row):
    n = len(row)
    for i,node in enumerate(row):
      if n > 1:
        if i < n-1:
          next = row[i + 1]
        else:
          next = row[0]
        node.addNeightbor(next.val, next)
        next.addNeightbor(node.val, node)

  def loadNextRowNeighborsVerts(self, currentRow, rN, nextRow):
    vertR = self.getVerts(rN)
    vertNR = self.getVerts(rN+1)

    if not vertR:
      atNode = currentRow[0]
      nodes = [nextRow[i] for i in vertNR]
      for n in nodes:
        atNode.addNeightbor(n.val, n)
        n.addNeightbor(atNode.val, atNode)

    for i, rVertI in enumerate(vertR):
      nRVertI = vertNR[i]
      atNode = currentRow[rVertI]
      (nextI,prevI) = self.getLoopNeighbors(nRVertI,len(nextRow))
      nodes = [nextRow[prevI], nextRow[nRVertI], nextRow[nextI]]
      for n in nodes:
        atNode.addNeightbor(n.val, n)
        n.addNeightbor(atNode.val, atNode)

  def loadNextRowNeighborsSide(self, currentRow, rN, nextRow):
    cRI = list(set(range(0,len(currentRow))) - set(self.getVerts(rN)))
    nRI = list(set(range(0,len(nextRow))) - set(self.getVerts(rN+1)))
    print currentRow, "------------------"
    chunksCR =[cRI[x:x+rN-1] for x in xrange(0, len(cRI), rN-1)]
    chunksNR =[nRI[x:x+rN] for x in xrange(0, len(nRI), rN)]

    for i, side in enumerate(chunksCR):
      nRSide = chunksNR[i]
      for j, nI in enumerate(side):
        atNode = currentRow[nI]
        nodes = [nextRow[nRSide[j]], nextRow[nRSide[j+1]]]
        for n in nodes:
          atNode.addNeightbor(n.val, n)
          n.addNeightbor(atNode.val, atNode)

  def getVerts(self, rN):
    return [x for x in range(0,(6 * rN)) if x % rN == 0]

  def getLoopNeighbors(self, i,n):
    next = None
    prev = None
    if n > 1:
      if i < n-1:
        next = i + 1
      else:
        next = 0

      if i > 0:
        prev = i - 1
      else:
        prev = n-1
    return (next,prev)


def main():
  n = 3
  a = list('A')
  b = list('BCDEFG')
  c = list('UANTCASTYSWQ')
  #d = list('EORNOTOBEKANGARTOB')
  data = [a,b,c]
  g = HoneyGraph()
  g.setup(n, data)

main()
