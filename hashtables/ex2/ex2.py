#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_retrieve)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * length

    for ticket in tickets:
        hash_table_insert(hashtable, ticket.source, ticket.destination)
    
    # Inserts starting point of trip
    route[0] = hash_table_retrieve(hashtable, "NONE")

    for i in range(length - 1):
        new_ticket = hash_table_retrieve(hashtable, route[i])
        route[i + 1] = new_ticket
    
    # Removes ["None"] from the end of the route
    return route[:-1]