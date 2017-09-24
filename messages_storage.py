import mmap
import jsonschema
from jsonschema import validate
import io, json, os
import message_schema as schema
import array

class MessagesStorage:
    def __init__(self):

        # File storage for messages
        self.STORAGE_PATH = 'messages.txt'
        if not os.path.exists(self.STORAGE_PATH):
            open(self.STORAGE_PATH, 'w').close()

        # Key map storage for messages.txt
        self.MAP_PATH = 'map.txt'
        if not os.path.exists(self.MAP_PATH):
            open(self.MAP_PATH, 'w').close()

        # Holds all the messages inserted as message dictionary
        # ID to hold start and end position on file
        self._messages_pos = {}

        # Holds the number of messages
        self._id_counter = 0

        self.init_from_file()

    # inserts message json
    # returns insert ID uint
    # None if failed
    def insert_message(self, message):

        # Validates message json
        try:
            validate(message, schema.MESSAGE_SCHEMA)
        except jsonschema.exceptions.ValidationError as ve:
            print("Insert ERROR #{}: ERROR\n".format(post_json))
            print(str(ve) + "\n")
            return None

        with io.open(self.STORAGE_PATH, 'a', encoding='utf-8') as f:
            start_index = f.tell()
            f.write(json.dumps(message, ensure_ascii=False))
            end_index = f.tell()
            self._messages_pos[self._id_counter] = {"start":start_index, "end":end_index}
            self._id_counter += 1

        # Save keys in map.tx
        with io.open(self.MAP_PATH, 'a', encoding='utf-8') as f:
            #f.write(str(self._id_counter - 1)+' '+str(start_index)+' '+str(end_index)+';')
            print(str(self._id_counter - 1)+' '+str(start_index)+' '+str(end_index), file=f)

        return self._id_counter - 1

    # Reads message with id
    # returns array of json messages, all ids if no ids passed to function
    # returns empty array if nothing found
    def read_messages(self, message_ids=None):

        try:
            with open(self.STORAGE_PATH, "r+b") as f:
                mm = mmap.mmap(f.fileno(), 0)

                if message_ids != None:
                    return self.extract_messages(message_ids, mm)
                else:
                    all_ids = array.array('i',(0 for i in range(0,self._id_counter)))
                    return self.extract_messages(all_ids, mm)
        except ValueError:
            print ("No messages on storage")
            return []

    def extract_messages(self, message_ids, mm):

        result = []
        for message_id in message_ids:
            if message_id <= self._id_counter:
                result.append(json.loads(mm[self._messages_pos[message_id]["start"]:
                         self._messages_pos[message_id]["end"]]))
        return result


    # Initializes the object from file storage
    def init_from_file(self):

        try:
            with open(self.MAP_PATH,"r") as f:
                for line in f:
                    try:
                        keys = line.split()
                        self._messages_pos[int(keys[0])] = {"start":int(keys[1]), "end":int(keys[2])}
                        self._id_counter += 1
                    except:
                        print("Failed to inialize line", line)
        except:
            print("Failed to open keymap file")
            return



# Example usage
if __name__ == '__main__':

    ms = MessagesStorage()

    message = {
        'recipient':31612345678,
        'originator':'MessageBird',
        'message':'This is a test message.'
    }

    ms.insert_message(message)

    print("Read message ", ms.read_messages([0]))
