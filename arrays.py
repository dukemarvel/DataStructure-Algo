from array import array
import sys, ctypes
primes = array('i', [2,3,5,7,11,13,17,19])
c = sys.getsizeof(primes)
print(c)

"""An experiment to explore the relationship
between a list’s length and its underlying
size in Python.
"""
def array_size(n):
    data = []
    for k in range(n):
        a = len(data)
        b = sys.getsizeof(data)
        print('Length: {0:3d}; Size in bytes:{0:4d}'.format(a,b))
        data.append(None)


class DynamicArray:
    """A dynamic array class akin to simplified python list"""
    
    def __init__(self) -> None:
        """Create an empty array"""
        self.__n = 0                                 # count actual elements, for internal use only
        self._capacity = 1                           # default array capacity, for internal use only
        self._A = self._make_array(self._capacity)   # low-level array, for internal use only

    def __len__(self):
        """Return the number elements stored in the array"""
        return self.__n

    def __getitem__(self, k):
        """Return element at index k"""
        if not 0 <= k < self.__n:
            raise IndexError('invalid index')
        return self._A[k]                           # retrieve from array

    def append(self, obj):
        """Add object to end of the array"""
        if self.__n == self._capacity:                # not enough room
            self._resize(2 * self._capacity)         # so double capacity
        self._A[self.__n] = obj
        self.__n += 1

    def _resize(self, c):                            # nonpublic utility methods
        """Resize internal array"""
        B = self._make_array(c)                      # new (Bigger) array
        for k in range(self.__n):                     # for each existing value
            B[k] = self._A[k]
        self._A = B                                  # use the bigger array
        self._capacity = c

    def _make_array(self, c):                        # nonpublic utility method
        """Return a new array with capacity c"""
        return (c * ctypes.py_object)()

    def insert(self, k, value):
        """Insert value at index k, shifting subsequent value rightward"""
        # (for simplicity, we assume 0 <= k <= n in this verion)
        if self.__n == self._capacity:                # not enough room
            self._resize(2 * self._capacity)         # so double capacity
        for j in range(self.__n, k, -1):              # shift rightmost first
            self._A[j] = self._A[j-1]
        self._A[k] = value                           # store newest element
        self.__n += 1

    def remove(self, value):
        """Remove first occurrence of value (or raise ValueError)."""
        # note: we do not consider shrinking the dynamic array in this version
        for k in range(self.__n):
            if self._A[k] == value:                  # found a match!
                for j in range(k, self.__n - 1):      # shift others to fill gap
                    self._A[j] == self._A[j+1]
                self._A[self.__n - 1] = None          # help garbage collection
                self.__n -= 1                         # we have one less item
                return                               # exit immediately
        raise ValueError('Value not found')          # only reached if no match
