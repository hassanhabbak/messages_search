import trie_tree


# This class is responsible for indexing
# and retriving from the index
# the indexed message properties
class MessagesIndex:
    def __init__(self):

        self.recipients_trie = trie_tree.Trie()
        self.originators_trie = trie_tree.Trie()
        self.messages_trie = trie_tree.Trie()

    # Indexes the message and all its components
    # Message assumed to be validated
    def index_message(self, message, message_id):

        self.index_recipient(message["recipient"], message_id)
        self.index_originator(message["originator"], message_id)
        self.index_content(message["message"], message_id)


    def index_recipient(self, recipient, message_id):

        self.recipients_trie.add(str(recipient), {"w":str(recipient),
                                            "id":message_id,
                                            "order":0})

    def index_originator(self, originator, message_id):

        self.originators_trie.add(originator, {"w":originator,
                                            "id":message_id,
                                            "order":0})

    def index_content(self, content, message_id):

        i = 0 # order of the word in message
        for word in content.split():
            self.messages_trie.add(word, {"w":word,
                                        "id":message_id,
                                        "order":i})
            i += 1

    # returns all message IDs by recipient
    # returns empty array if nothing found
    def get_message_ids_recipient(self, recipient):

        message_ids = []
        search_r = self.recipients_trie.search(str(recipient))
        if search_r != None:
            for data in search_r:
                message_ids.append(data["id"])
        return message_ids

    # returns all message IDs by originator
    # returns empty array if nothing found
    def get_message_ids_originator(self, originator):

        message_ids = []
        search_r = self.originators_trie.search(str(originator))
        if search_r != None:
            for data in search_r:
                message_ids.append(data["id"])
        return message_ids

    # returns all message IDs by text in message
    # returns empty array if nothing found
    def get_message_ids_message_contains(self, words):

        common_ids_set = set()
        i = 0 # words counted since first word is special
        for word in words:
            search_r = self.messages_trie.search(str(word))
            ids_set = set()
            if search_r != None:
                for data in search_r:
                    ids_set.add(data["id"])
            else: # one word does not exist in the tree
                return []
            if i != 0:
                common_ids_set = common_ids_set.intersection(ids_set)
                # set is empty so it will remain empty. Exit with empty results
                if len(common_ids_set) == 0:
                    return []
            else: # First time just populate the set
                common_ids_set = ids_set
            i += 1
        return list(common_ids_set)

# Example use
if __name__ == '__main__':

    message = {
        'recipient':31612345678,
        'originator':'MessageBird',
        'message':'This is a test message.'
    }
    ms = MessagesIndex()
    ms.index_message(message, 0)

    print ("'31612345678' in recipients: ", ms.recipients_trie.contains('31612345678'))
    print ("'MessageBird' in originator: ", ms.originators_trie.contains('MessageBird'))
    print ("'This' in content: ", ms.messages_trie.contains('This'))
    print ("'is' in content: ", ms.messages_trie.contains('is'))

    print ("Search '31612345678' in recipients: ", ms.get_message_ids_recipient('31612345678'))
    print ("Search '316123452678232' in recipients: ", ms.get_message_ids_recipient('316123452678232'))
    print ("Search 'This is a' in message content: ", ms.get_message_ids_message_contains(['This', 'is', 'a']))
    print ("Search 'This is not a' in message content: ", ms.get_message_ids_message_contains(['This', 'is', 'a', 'not']))
