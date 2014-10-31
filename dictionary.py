
class Dictionary:
  tree = None

  def setup(self, words):
    self.tree = self.make_trie(words)

  def make_trie(self, words):
    root = dict()
    for word in words:
      current_dict = root
      for letter in list(word):
        current_dict = current_dict.setdefault(letter, {})
      current_dict = current_dict.setdefault('_end_', '_end_')
    return root
