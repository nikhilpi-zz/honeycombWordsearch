
class HNode:
  uID = None
  neighbors = None
  val = ''

  def __init__(self):
    self.neighbors = dict()

  def addNeighbor(self, val, node):
    if val in self.neighbors:
      self.neighbors[val].add(node)
    else:
      self.neighbors[val] = set([node])

  def getValNeighbors(self, keys):
    out = []
    for key in keys:
      if key in self.neighbors:
        nodes = self.neighbors[key]
        for n in nodes:
          out.append(n)
    return out


class HoneyGraph:
  comb = {}

  def setup(self, n,data): 
    # Load nodes
    graph = []
    uIDC = 0

    for row in range(0,n):
      currentRow = data[row]
      hRow = []
      for i in currentRow:
        node = HNode()
        node.uID = uIDC
        uIDC += 1
        node.val = i
        hRow.append(node)
      graph.append(hRow)

    for row in range(0,n):
      currentRow = graph[row]
      nextRow = None
      if row < n-1:
        nextRow = graph[row+1]

      self.loadRowNeighbors(currentRow)
      if row < n-1:
        self.loadNextRowNeighborsVerts(currentRow, row, nextRow)
        if row > 1:
          self.loadNextRowNeighborsSide(currentRow, row, nextRow)

    nodes = [item for sublist in graph for item in sublist]
    for n in nodes:
      if n.val in self.comb:
        self.comb[n.val].add(n)
      else:
        self.comb[n.val] = set([n])

  def loadRowNeighbors(self, row):
    n = len(row)
    for i,node in enumerate(row):
      if n > 1:
        if i < n-1:
          next = row[i + 1]
        else:
          next = row[0]
        node.addNeighbor(next.val, next)
        next.addNeighbor(node.val, node)

  def loadNextRowNeighborsVerts(self, currentRow, rN, nextRow):
    vertR = self.getVerts(rN)
    vertNR = self.getVerts(rN+1)

    if not vertR:
      atNode = currentRow[0]
      nodes = [nextRow[i] for i in vertNR]
      for n in nodes:
        atNode.addNeighbor(n.val, n)
        n.addNeighbor(atNode.val, atNode)

    for i, rVertI in enumerate(vertR):
      nRVertI = vertNR[i]
      atNode = currentRow[rVertI]
      (nextI,prevI) = self.getLoopNeighbors(nRVertI,len(nextRow))
      nodes = [nextRow[prevI], nextRow[nRVertI], nextRow[nextI]]
      for n in nodes:
        atNode.addNeighbor(n.val, n)
        n.addNeighbor(atNode.val, atNode)

  def loadNextRowNeighborsSide(self, currentRow, rN, nextRow):
    cRI = list(set(range(0,len(currentRow))) - set(self.getVerts(rN)))
    nRI = list(set(range(0,len(nextRow))) - set(self.getVerts(rN+1)))
    chunksCR =[cRI[x:x+rN-1] for x in range(0, len(cRI), rN-1)]
    chunksNR =[nRI[x:x+rN] for x in range(0, len(nRI), rN)]

    for i, side in enumerate(chunksCR):
      nRSide = chunksNR[i]
      for j, nI in enumerate(side):
        atNode = currentRow[nI]
        nodes = [nextRow[nRSide[j]], nextRow[nRSide[j+1]]]
        for n in nodes:
          atNode.addNeighbor(n.val, n)
          n.addNeighbor(atNode.val, atNode)

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

