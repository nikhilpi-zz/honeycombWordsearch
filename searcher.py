from honeyGraph import HoneyGraph 
from dictionary import Dictionary 
import copy, sys

def main():
  graph = sys.argv[1]
  wordsList = sys.argv[2]

  with open(graph, 'r') as f:
    n = int(f.readline().strip())
    data = []
    for i in range(0,n):
      l = list(f.readline().strip())
      data.append(l)

  g = HoneyGraph()
  g.setup(n, data)

  words = []
  with open(wordsList, 'r') as f:
    words = [line.strip() for line in f.readlines()]

  d = Dictionary()
  d.setup(words)
  bound = max(words, key=len)

  out = set()
  for key in d.tree.keys():
    for n in g.comb[key]:
      recurseSearch(n, d.tree, '', [], out)
  out = sorted(out)

  with open('output.txt', 'w') as f:
    for i in out:
      f.write(i + "\n")

def recurseSearch(gN, dN, wordSoFar, path, words):
  for val, rest in dN.items():
    wordSoFar = copy.deepcopy(wordSoFar)
    path = copy.deepcopy(path)
    if val == "_end_":
      words.add(wordSoFar)
    else:
      if val == gN.val and gN.uID not in path:
        wordSoFar += val
        path.append(gN.uID)
        if "_end_" in rest:
          words.add(wordSoFar)
        for n in gN.getValNeighbors(rest.keys()):
          recurseSearch(n, rest, wordSoFar, path, words)

      

main()