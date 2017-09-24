# messages_search
A small RESTful api server that keeps and indexes messages written in Python

# Example message structure
{
  "recipient":31612345678,
  "originator":"MessageBird",
  "message":"This is a test message."
}

# Create Message api call
POST /messages
{
  "recipient":31612345678,
  "originator":"MessageBird",
  "message":"This is a test message."
}


# API call to search message properties

The messages are accessed by the api as follows.

GET /messages?recipient=31612345678

The properties you can use are:
  . recipient
  . originator
  . message_contains (Searches for message text with all the words in the search query existing in the body space seperated)
  
# Architecture

This application optimizes for speed and memory effeciency. Since memory is expensive, it keeps all the messages on file text. The file is memory maped and its indexes are saved in a trie tree for searching. Makes the look up on messages of worst case O(N) N being key length. It also facilitates for further advanced search options in text like search of all prefixes, search of exact sentences and closest variation on a search term.

