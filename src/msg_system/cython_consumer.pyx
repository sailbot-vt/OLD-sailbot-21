# distutils: sources = consumer.c relay.c
import pdb
from abc import ABC, abstractmethod

cdef extern register_to_consume_data(int channelName, void *callback)

cdef void *data_callback(void *dataPtr) {

    """
   //Called by relay when a publisher publishes data
    //***Currently not working -- issue with consumer data structure not actually being accessed in relay***
    //  Definitely just me being stupid -- need to look into that
    """

    int *newdataPtr = (int *)dataPtr;

    printf("data callback called: %p\n", &consumer_data);

    memcpy(&consumer_data, newdataPtr, DATASIZE);

    printf("First 4 ints = %i %i %i %i\n", consumer_data[0], consumer_data[1], consumer_data[2], consumer_data[3]);

    

    pthread_exit(0);
}

"""
    cdef int cythonCallback(void *dataPtr, int dataSize):
        
        cdef int *newdataPtr = <int *>dataPtr

        cdef int data [dataSize]

        memcpy(&data, dataPtr, dataSize)

        data_callback(data) 

"""

class consumer(ABC):
    """
    An abstract class to hide the interface with Cython from consumers.
    """

    @abstractmethod
    def py_register_to_consume_data(self, channel_name):
        """
        Register with relay to receive a callback upon data being received on <channel_name>. 

        Calls cython which calls the C... Relay keeps track of who to signal upon receiving new data

        Keyword arguments:
        channel_name -- The name of the channel to subscribe to (need to coordinate with producer to have matching values)
        data_callback -- Method to execute upon receiving signal from relay... This method will be passed the dereferenced data from shared memory
        """

        pdb.set_trace()

#        register_to_consume_data(channelName, self.cythonCallback)

    @abstractmethod
    def data_callback(self, data):
        """
        This method is instantiated upon receiving a signal from the relay

        Called by cython method that dereferences data in shared memory and passes it to this function

        Keyword arguments:
        data -- Data that is passed to the callback... Will likely be in a structured numpy array
        """

        pass

    

class example_consumer_class(consumer):
    """
    Inherits from consumer base class
    """
    def py_register_to_consume_data(self, channel_name):
        """
        Nothing additional needed here... Just remember to run this method in order to receive any data!
        """

        pass

    def data_callback(self, data):
        """
        Do any processing needed on the data... Remember to keep the system real-time
        """
        pass

