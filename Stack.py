class Empty(Exception):
    """Error attempting to access an element from an empty container"""
    pass


class ArrayStack:
    """LIFO Stack implementation using a Python list an underlying storage"""
    def __init__(self) -> None:
        """Create ann empty stack"""
        self._data = []

    def __len__(self):
        """Return the number of element in the stack"""
        return len(self._data)

    def is_empty(self):
        """Return true if the stack is empty"""
        return len(self._data) == 0

    def push(self, e):
        """Add element to the top of the stack"""
        self._data.append(e)

    def top(self):
        """Return (but do not remove) the element at the top of the stack.
        Raise Empty exception when stack is empty."""

        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data[-1]

    def pop(self):
        """Remove and return the top element of the stack.
        Raise Empty exception if the stack is empty."""
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data.pop()



def is_matched(expr):
    """Return True if all delimiter are properly matched; False otherwise."""
    lefty = '({['
    righty = ')}]'
    S = ArrayStack()
    for c in expr:
        if c in lefty:
            S.push(c)
        elif c in righty:
            if S.is_empty():
                return False
            if righty.index(c) != lefty.index(S.pop()):
                return False
    return S.is_empty()


class LinkedStacked:
    '''LIFO Stack implementation using a singly linked list for storage.'''
    #-------------------------- nested Node class --------------------------
    class _Node:
        '''Lightweight, nonpublic class for storing a singly linked node.'''
        __slot__ = '_element', '_next'                  # streamline memory usage
        def __init__(self, element, next):              # initialize node’s fields
            self._element = element                     # reference to user’s element
            self._next = next                           # reference to next node

    #------------------------------- stack methods -------------------------------
    def __init__(self):
        '''Create an empty stack'''
        self._head = None                    # reference to the head node
        self._size = 0                       # number of stack elements


    def __len__(self):
        '''Return the number of elements in the stack.'''
        return self._size


    def is_empty(self):
        '''Return True if the stack is empty.'''
        return self._size == 0

    def push(self, e):
        '''Add element e to the top of the stack.'''
        self._head = self._Node(e, self._head)   # create and link a new node
        self._size += 1

    def top(self):
        '''Return (but do not remove) the element at the top of the stack
           Raise Empty exception if the stack is empty.'''
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._head._element                # top of the stack is at the head of the list

    def pop(self):
        '''Remove and return the element from the top of the stack.
           Raise Empty exception if the stack is empty.'''
        if self.is_empty():
            raise Empty('Stack is empty')
        result = self._head._element
        self._head = self._head._element           #  bypass the former top node
        self._size -= 1
        return result