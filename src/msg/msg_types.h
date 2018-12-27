#ifndef msg_types_h
#define msg_types_h


#include <Python.h>
#include <stddef.h>


typedef struct Data {
    size_t size;
    void* data;
} Data;


typedef struct CallbackWithData {
    Data data;
    PyObject* py_callback;
} CallbackWithData;

#endif /* msg_types_h */
