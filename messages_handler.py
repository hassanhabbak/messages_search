import messages_storage
import messages_index
import message_schema as m_schema
import jsonschema
from jsonschema import validate
import datetime


# This handler class is responsible for the IO of stored and index messages
class MessagesHandler:

    def __init__(self):

        self.m_storage = messages_storage.MessagesStorage()
        self.m_index = messages_index.MessagesIndex()

        # index everything loaded from the file
        i = 0
        for message in self.m_storage.read_messages():
            self.m_index.index_message(message, i)
            i += 1

    # inserts message into system
    # returns false if failed
    def insert(self, message):

        try:
            validate(message, m_schema.MESSAGE_SCHEMA)
            message['timestamp'] = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            m_id = self.m_storage.insert_message(message)
            if m_id is None: # If insert into storage failed
                print("Message Handler Insert Storage Error")
                return False
            self.m_index.index_message(message, m_id)
        except jsonschema.exceptions.ValidationError as ve:
            print("Message Handler Insert Error #{}: ERROR\n".format(message))
            print(str(ve) + "\n")
            return False
        return True

    # get messages with recipient
    # returns an array of messages json
    def search_recipients(self, recipient):

        m_ids = self.m_index.get_message_ids_recipient(str(recipient))
        return {"list":self.m_storage.read_messages(m_ids)}

    # get messages with originator
    # returns an array of messages json
    def search_originators(self, originator):

        m_ids = self.m_index.get_message_ids_originator(str(originator))
        return {"list":self.m_storage.read_messages(m_ids)}

    # get messages with message content containing words
    # returns an array of messages json
    def search_content(self, words):

        m_ids = self.m_index.get_message_ids_message_contains(words)
        return {"list":self.m_storage.read_messages(m_ids)}

    # get messages that fit all non None options
    def search(self, recipient = None, originator = None, content_contains = None):

        rec_set, ori_set, con_set = None, None, None
        intersection_list = []

        if recipient != None:
            rec_set = set(self.m_index.get_message_ids_recipient(str(recipient)))
            intersection_list.append(rec_set)
        if originator != None:
            ori_set = set(self.m_index.get_message_ids_originator(str(originator)))
            intersection_list.append(ori_set)
        if content_contains != None:
            con_set = set(self.m_index.get_message_ids_message_contains(content_contains))
            intersection_list.append(con_set)

        m_ids = list(set.intersection(*intersection_list))
        return {"list":self.m_storage.read_messages(m_ids)}


# Example use
if __name__ == '__main__':

    mh = MessagesHandler()

    message = {
        'recipient':31612345678,
        'originator':'MessageBird',
        'message':'This is a test message.'
    }

    print("Insert Message Status", mh.insert(message))
    print("Recipients search", mh.search_recipients(31612345678))
    print("Originator search", mh.search_originators('MessageBird'))
    print("Content search", mh.search_content(['This', 'is', 'a']))
