/// http://www.qtcentre.org/archive/index.php/t-29773.html



long int unwrap(QObject* ptr) {
    return reinterpret_cast<long int>(ptr);
}

template <typename T>
T* wrap(long int ptr) {
    return reinterpret_cast<T*>(ptr);
}




class_<QObject, QObject*, boost::noncopyable>("QObject", no_init)
    .def("unwrap", unwrap)
    .def("wrap", make_function( wrap<QObject>, return_value_policy<return_by_value>() ))
    .staticmethod("wrap")
;

class_<QWidget, bases<QObject>, QWidget*, boost::noncopyable>("QWidget")
    .def("wrap", make_function( wrap<QWidget>, return_value_policy<return_by_value>() ))
    .staticmethod("wrap")
;

class_<QFrame, bases<QWidget>, QFrame*, boost::noncopyable>("QFrame")
    .def("wrap", make_function( wrap<QFrame>, return_value_policy<return_by_value>() ))
    .staticmethod("wrap")
;

class_<QLabel, bases<QFrame>, QLabel*, boost::noncopyable>("QLabel")
    .def("wrap", make_function( wrap<QLabel>, return_value_policy<return_by_value>() ))
    .staticmethod("wrap")
;



/*

http://www.qtcentre.org/archive/index.php/t-29773.html


This is an example how to integrate PyQt4 and boost::python

first of all we must define wrap/unwrap function to deal with bare pointers


long int unwrap(QObject* ptr) {
return reinterpret_cast<long int>(ptr);
}

template <typename T>
T* wrap(long int ptr) {
return reinterpret_cast<T*>(ptr);
}


after that we must register all classes we want integrate to


class_<QObject, QObject*, boost::noncopyable>("QObject", no_init)
.def("unwrap", unwrap)
.def("wrap", make_function( wrap<QObject>, return_value_policy<return_by_value>() ))
.staticmethod("wrap");

class_<QWidget, bases<QObject>, QWidget*, boost::noncopyable>("QWidget")
.def("wrap", make_function( wrap<QWidget>, return_value_policy<return_by_value>() ))
.staticmethod("wrap");

class_<QFrame, bases<QWidget>, QFrame*, boost::noncopyable>("QFrame")
.def("wrap", make_function( wrap<QFrame>, return_value_policy<return_by_value>() ))
.staticmethod("wrap");

class_<QLabel, bases<QFrame>, QLabel*, boost::noncopyable>("QLabel")
.def("wrap", make_function( wrap<QLabel>, return_value_policy<return_by_value>() ))
.staticmethod("wrap");


and for example we have class that works with.. QLabel:



class worker: public QObject {
...
void add_label(QLabel*);
};


we must expose this class to python too:


class_<worker, bases<QObject>, worker*, boost::noncopyable>("worker")
.def("add_label", &worker::add_label);

now we a ready to interaction,
on C++-size do something like this



worker* w = new worker;
main_namespace["worker"] = boost::ref(w);


python:


from PyQt4.Qt import *
import sip
import mylib as MyLib

#...

#If you are using QApplication on C++-size you don't need to create another one

lb = QLabel("label from PyQt4!")

lb_ptr = sip.unwrapinstance(f)

my_lb = MyLib.QLabel.wrap(lb_ptr)

worker.add_label(my_lb)



In other case if you wan't send you own Q-object to PyQt4 :



QLabel* lb = new QLabel("C++ label");
main_namespace["lb"] = boost::ref(lb);


python:


from PyQt4.Qt import *
import sip
import mylib as MyLib

#...

my_lb_ptr = lb.unwrap()

qt_lb = sip.wrapinstance(my_lb_ptr, QLabel)




And this is my real little helper:


from PyQt4.Qt import *
import sip

def toQt(object, type):
ptr = object.unwrap()
return sip.wrapinstance(ptr, type)

def fromQt(object, type):
ptr = sip.unwrapinstance(object)
return type.wrap(ptr)
Powered by vBulletin® Version 4.1.9 Copyright © 2015 vBulletin Solutions, Inc. All rights reserved.
*/
