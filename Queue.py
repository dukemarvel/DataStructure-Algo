from queue import Empty


class ArrayQueue:
    """First in First Out(FIFO) queue implementation using a Python list as an underlying storage."""
    DEFAULT_CAPACITY = 10   #moderate capacity for all new queues

    def __init__(self):
        """Create an empty queue."""
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0


    def __len__(self):
        """Return the number of element in the queue."""
        return self._size
    
    def is_empty(self):
        """Return True if the queue is empty."""
        return self._size == 0

    def first(self):
        """Return (but do not remove) the element at the front of the queue.
           Raise Empty exception if the queue is empty."""
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._data[self._front]

    def dequeue(self):
        """Remove and return the first element of the queue(i.e FIFO)
           Raise Empty exception if the queue is empty."""
        if self.is_empty():
            raise Empty('Queue is empty')
        answer = self._data[self._front]
        self._data[self._front] = None                          # help with gabage collection
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return answer

    def enqueue(self, e):
        """Add an element to the back of queue."""
        if self._size == len(self._data):
            self._resize(2 * len(self._data)) # double the array
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1

    def _resize(self, cap):                                     # we assume cap >= len(self)
        """Resize to a new list of capacity >= len(self)."""
        old = self._data                                        # keep track of the old data
        self._data = [None] * cap                               # allocate list with new capacity
        walk = self._front
        for k in range(self._size):                             # only consider an existing elements
            self._data[k] = old[walk]                           # intentionally shift indices
            walk = (1 + walk) % len(old)                        # use old size as modulus
        self._front = 0                                         # front has been realigned




class ArrayDeque(ArrayQueue):
    def last(self):
        """Return (but do not remove) the last element (back of the queue) of the queue.
            Raise Empty exception if deque is empty"""
        if self.is_empty():
            raise Empty('Deque is empty')
        back = (self._front + self._size - 1) % len(self._data)
        return self._data[back]

    
    def add_first(self, e):
        """Add an element to the front of the deque."""
        self._front = (self._front - 1) % len(self._data)          # cycli shift
        self._data[self._front] = e
        self._size += 1


    def add_last(self, e):
        self.enqueue(e)
    
    def delete_first(self):
        self.dequeue()
    
    def delete_last(self):
        '''Return the last element of the deque.
           Raise E,pty exception if deque is empty.'''
        back = (self._front + self._size - 1) % len(self._data)
        result = self._data[back]
        self._data[back] = None                                         # help with gabage collection
        self._size -= 1
        return result

    def show_deque(self):
        back = (self._front + self._size - 1) % len(self._data)
        return self._data[self._front:back]





class LinkedQueue:
    '''FIFO queue implementation using a singly linked list for storage.'''
    #-------------------------- nested Node class --------------------------
    class _Node:
        '''Lightweight, nonpublic class for storing a singly linked node.'''
        __slot__ = '_element', '_next'                  # streamline memory usage
        def __init__(self, element, next):              # initialize node’s fields
            self._element = element                     # reference to user’s element
            self._next = next
    
    #------------------------------- queue methods -------------------------------
    def __init__(self):
        '''Create an empty queue'''
        self._head = None
        self._tail = None
        self._size = 0                          # number of elements in the queue


    def __len__(self):
        '''Return the number of elements in the queue.'''
        return self._size
    
    def is_empty(self):
        '''Return True if the queue is empty.'''
        return self._size == 0

    def first(self):
        '''Return (but do not remove) the element at the fronts (head) of the queue.'''
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._head._element               # front alignment with the head of the list

    def dequeue(self):
        '''Remove and return the first element of the queue(FIFO).
           Raise Empty exception if queue is empty'''
        if self.is_empty():
            raise Empty('Queue is empty')
        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        if self.is_empty():                        # special case as queue is empty
            self._tail = None                      # removed head had been the tail
        return answer
    

    def enqueue(self, e):
        '''Add an element to the back of queue.'''
        newest = self._Node(e, None)               # node will be new tail node          
        if self.is_empty():
            self._head = newest                    # special case: previously empty
        else:
            self._tail._next = newest              
        self._tail = newest                        # update reference to tail node
        self._size += 1




class CircularQueue:
    '''FIFO queue implementation using a circularly linked list for storage.'''
    #-------------------------- nested Node class --------------------------
    class _Node:
        '''Lightweight, nonpublic class for storing a singly linked node.'''
        __slot__ = '_element', '_next'                  # streamline memory usage
        def __init__(self, element, next):              # initialize node’s fields
            self._element = element                     # reference to user’s element
            self._next = next
    
    #------------------------------- queue methods -------------------------------
    def __init__(self):
        '''Create an empty queue.'''
        self._tail = None                   # will represent tail of queue
        self._size = 0                      # number of elements in the queue

    def __len__(self):
        '''Return the number of elements in the queue.'''
        return self._size
    
    def is_empty(self):
        '''Return True if the queue is empty.'''
        return self._size == 0

    def first(self):
        '''Return (but do not remove) the element at the front of the queue.'''
        if self.is_empty():
            raise Empty('Queue is empty')
        head = self._tail._next 
        return head._element

    def dequeue(self):
        '''Remove and return the first element of the queue(i.e FIFO).'''
        if self.is_empty():
            raise Empty('Queue is empty')
        oldhead = self._tail._next 
        if self._size == 1:                     # removing only element
            self._tail = None                   # queue becomes empty
        else:
            self._tail._next = oldhead._next    # bypass the old head
        self._size -= 1
        return oldhead._element

    def enqueue(self, e):
        '''Add an element to the back of queue.'''
        newest = self._Node(e, None)            # node will be new tail
        if self.is_empty():
            newest._next = newest               # initialize circularly
        else:
            newest._next = self._tail._next     # new node points to head
            self._tail._next = newest           # old tail points to new node
        self._tail = newest                     # new node becomes the tail
        self._size += 1
    
    def rotate(self):
        '''Rotate front element to the back of the queue.'''
        if self._size > 0:
            self._tail = self._tail._next       # old head becomes new tail





class _DoublyLinkedBase:
    '''A base class providing a doubly linked list representation.'''
    class _Node:
        '''Lightweight, nonpublic class for storing a doubly linked node.'''
        __slot__ = '_element', '_prev', '_next'   # streamline memory
        def __init__(self, element, prev, next):  # initialize node's fields
            self._element = element               # user's element
            self._prev = prev                     # previous node reference
            self._next = next                     # next node reference

    def __init__(self):
        '''Create an empty list'''
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)
        self._header._next = self._trailer        # trailer is after header
        self._trailer._prev = self._header        # header is before trailer
        self._size = 0                            # number of elements


    def is_empty(self):
        '''Return True if list is empty.'''
        return self._size == 0

    def __len__(self):
        '''Return the number of elements in the list.'''
        return self._size
    
    def _insert_between(self, e, predecessor, successor):
        '''Add element e between two existing node and return new node.'''
        newest = self._Node(e, predecessor, successor) # linked to neighbors
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest

    def _delete_node(self, node):
        '''Delete nonsentinel node from the list and return its element.'''
        predecessor = node._prev
        successor = node._next 
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element                         # record deleted element
        node._prev = node._next = node._element = None  # deprecate node
        return element



class LinkedDeque(_DoublyLinkedBase):
    '''Doubl-ended queue implementation based on a doubly linked list.'''

    def first(self):
        '''Return (but do not remove) the element at the front of the deque.'''
        if self.is_empty():
            raise Empty('Deque is empty')
        return self._header._next._element                # real item just after the header
    
    def last(self):
        '''Return (but do not remove) the element at the back of the deque.'''
        if self.is_empty():
            raise Empty('Deque is empty')
        return self._trailer._prev._element               # real item just before trailer

    def insert_first(self, e):
        '''Add an element to the front of the deque'''
        self._insert_between(e, self._header, self._header._next)     # after header

    def insert_last(self, e):
        '''Add an element to the back of the deque.'''
        self._insert_between(e, self._trailer._prev, self._trailer)   # before the trailer



    def delete_firsty(self):
        '''Remove and return the element from the front of the deque.
           Raise Empty exception if the deque is empty.'''
        if self.is_empty():
            raise Empty('Deque is empty')
        return self._delete_node(self._header._next)

    
    def delete_last(self):
        '''Remove and return the element from the back of the deque.
           Raise Empty exception if the deque is empty.'''
        if self.is_empty():
            raise Empty('Deque is empty')
        return self._delete_node(self._trailer._prev)




class PositionalList(_DoublyLinkedBase):
    '''A sequential container of elements allowing positional access.'''

    #-------------------------- nested Position class --------------------------
    class Position:
        '''An abstraction representing the location of a single element.'''
        def __init__(self, container, node):
            '''Constructor should not be invoked by user.'''
            self._container = container
            self._node = node

        def element(self):
            '''Return the element stored at this Position.'''
            return self._node._element
        
        def __eq__(self, other):
            '''Return True if other is a Position representing the same location.'''
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other) -> bool:
            '''Return True if other does not represent the same location.'''
            return not (self == other)        # opposit of __eq__

    #------------------------------- utility method -------------------------------
    def _validate(self, p):
        '''Return position s node, or raise appropriate error if invalid.'''
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._next is None:             # convention for deprecated nodes
            raise ValueError('p is no longer valid')

        return p._node

    def _make_position(self, node):
        '''Return Position instance for given node (or None if sentinel).'''
        if node is self._header or node is self._trailer:
            return None                        # boundary conditions
        else:
            return self.Position(self, node)   # legitimate position

    #------------------------------- accessors -------------------------------
    def first(self):
        '''Return the first Position in the list (or None if list is empty).'''
        return self._make_position(self._header._next)

    def last(self):
        '''Return the last Position in the list (or None if list is empty).'''
        return self._make_position(self._trailer._prev)

    def before(self, p):
        '''Return the Position just before Position p (or None if p is first).'''
        node = self._validate(p)
        return self._make_position(node._prev)

    def after(self, p):
        '''Return the Position just after Position p (or None if p is last).'''
        node = self._validate(p)
        return self._make_position(node._next)

    def __iter__(self):
        '''Generate a forward iteration of the elements of the list.'''
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)


    #------------------------------- mutators -------------------------------
    # override inherited version to return Position, rather than Node
    def _insert_between(self, e, predecessor, successor):
        '''Add element between existing nodes and return new Position.'''
        node = super()._insert_between(e, predecessor, successor)
        return self._make_position(node)


    def add_first(self, e):
        '''Insert element e at the front of the list and return new Position.'''
        return self._insert_between(e, self._header, self._header._next)

    def add_last(self, e):
        '''Insert element e at the back of the list and return new Position.'''
        return self._insert_between(e, self._trailer._prev, self._trailer)

    def add_before(self, p, e):
        '''Insert element e into list before Position p and return new Position.'''
        original = self._validate(p)
        return self._insert_between(e, original._prev, original)

    def add_after(self, p, e):
        '''Insert element e into list after Position p and return new Position.'''
        original = self._validate(p)
        return self._insert_between(e, original, original._next)

    def delete(self, p):
        '''Remove and return the element at Position p.'''
        original = self._validate(p)
        return self._delete_node(original)         # inherited method returns element


    def replace(self, p, e):
        '''Replace the element at Position p with e.
           Return the element formerly at Position p.'''
        original = self._validate(p)
        old_value = original._elemeny              # temporarily store old element
        original._element = e                      # replace with new element
        return old_value                           # return the old element value






class FavoriteList:
    '''List of elements ordered from most frequently accessed to least'''
    #.........................nested _item class ......................
    class _item:
        __slot__= '_value', '_count'            # streamline memory usage
        def __init__(self, e):
            self._value = e                     # the user's element
            self._count = 0                     # access count initially zero



    #...................... nonpublic utilities .......................
    def _find_positon(self, e):
        '''Search for element e and return its Positon (or None if not found).'''
        walk = self._data.first()
        while walk is not None and walk.element()._value != e:
            walk = self._data.after(walk)
        return walk

    def _move_up(self, p):
        '''Move item at Position p earlier in the list based on access count.'''
        if p != self._data.first():            # consider moving up
            cnt = p.element()._count
            walk = self._data.before(p)
            if cnt > walk.element()._count:    # must shift forward
                while (walk != self._data.first() and 
                        cnt > self._data.before(walk).element()._count):
                        walk = self._data.before(walk)
                self._data.add_before(walk, self._data.delete(p))   # delete/reinsert

    #.......................... public methods ..........................
    def __init__(self):
        '''Create an empty list of favorites.'''
        self._data = PositionalList()          # will be list of _item instances

    def __len__(self):
        '''Return number of entries on favorites list.'''
        return len(self._data)

    def is_empty(self):
        '''Return True if list is empty.'''
        return len(self._data) == 0

    def access(self, e):
        '''Access element e, thereby increasing its access count.'''
        p = self._find_positon(e)                       # try to locate existing element
        if p is None:
            p = self._data.add_last(self._item(e))      # if new, place at end
        p.element()._count += 1                         # always increment count
        self._move_up(p)

    def remove(self, e):
        '''Remove element e from the list of favorites.'''
        p = self._find_positon(e)                       # try to locate existing element
        if p is not None:
            self._data.delete(p)                        # delete if found

    def top(self, k):
        '''Generate sequence of top k elements in terms of access count.'''
        if not 1 <= k <= len(self):
            raise ValueError('Illegal value for k')
        walk = self._data.first()
        for j in range(k):
            item = walk.element()                      # element of list is _item
            yield item._value                          # report user's element
            walk = self._data.after(walk)