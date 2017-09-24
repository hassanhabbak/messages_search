class Node:
    def __init__(self, label=None, data=None, is_word = False):

        # Contains the indexed data object
        self.data = []

        # Contains all the children indexed one level below
        self.children = dict()

        # Signals this node to mark an end of a word
        self.is_word = False

    def add_child(self, key, data=None):
        if not isinstance(key, Node):
            self.children[key] = Node(key, data)

    def __getitem__(self, key):
        return self.children[key]

class Trie:
    def __init__(self):
        self.head = Node()

    def __getitem__(self, key):
        return self.head.children[key]

    def add(self, word, data=None):
        current_node = self.head
        word_finished = True

        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
            else:
                word_finished = False
                break

        # For ever new letter, create a new child node
        if not word_finished:
            while i < len(word):
                current_node.add_child(word[i])
                current_node = current_node.children[word[i]]
                i += 1

        # Index the referenced object
        current_node.data.append(data)
        current_node.is_word = True

    def contains(self, word):
        if word == '':
            return False
        if word == None:
            raise ValueError('Trie.contains requires a not-Null string')

        # Start at the top
        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break

        # Check if it is the end of a word
        if exists:
            exists = current_node.is_word

        return exists

    # Returns all the Data that its key starts with a prefix
    def start_with_prefix(self, prefix):

        words = list()
        if prefix == None:
            raise ValueError('Requires not-Null prefix')

        # Determine end-of-prefix node
        top_node = self.head
        for letter in prefix:
            if letter in top_node.children:
                top_node = top_node.children[letter]
            else:
                # Prefix not in tree, go no further
                return words

        # Get words under prefix
        if top_node == self.head:
            queue = [node for key, node in top_node.children.iteritems()]
        else:
            queue = [top_node]

        # Perform a breadth first search under the prefix
        # A cool effect of using BFS as opposed to DFS is that BFS will return
        # a list of words ordered by increasing length
        while queue:
            current_node = queue.pop()
            if current_node.is_word:
                # Isn't it nice to not have to go back up the tree?
                words.append(current_node.data)

            queue = [node for key,node in current_node.children.items()] + queue

        return words

    # Searches for the index and returns the indexed data
    def search(self, word):

        # Not found in Trie
        if not self.contains(word):
            return None

        # Race to the bottom, get data
        current_node = self.head
        for letter in word:
            current_node = current_node[letter]

        return current_node.data

# Example use
if __name__ == '__main__':

    trie = Trie()
    words = 'hello goodbye help gerald gold tea ted team to too tom stan standard money'
    for word in words.split():
        trie.add(word, {"w":word, "id":1})
    trie.add("123", {"w":"123", "id":2})
    trie.add("123", {"w":"123", "id":3})

    print ("'goodbye' in trie: ", trie.contains('goodbye'))
    print ("'123' in trie: ", trie.contains('123'))
    print ("'Notthere' in trie: ", trie.contains('Notthere'))
    print (trie.start_with_prefix('g'))
    print (trie.start_with_prefix('to'))
    print (trie.search("123"))
