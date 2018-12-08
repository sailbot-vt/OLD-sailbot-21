#ifndef msg_types_h
#define msg_types_h


#include <stddef.h>
#include <Python.h>


typedef struct Data {
    size_t size;
    void* data;
} Data;


typedef struct CallbackWithData {
    Data* data;
    PyObject* callback;
} CallbackWithArgs;

#endif /* msg_types_h */