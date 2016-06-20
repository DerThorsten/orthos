#define PY_ARRAY_UNIQUE_SYMBOL vigranumpyorthos_PyArray_API
#define NO_IMPORT_ARRAY


/*orthos*/
#include <orthos_cpp/orthos.hxx>
#include <orthos_cpp/axis/axis.hxx>
#include <orthos_cpp/axis/plane.hxx>

/*vigra python */
#include <vigra/numpy_array.hxx>
#include <vigra/numpy_array_converters.hxx>
#include <vigra/python_utility.hxx>
#include <boost/python/stl_iterator.hpp>

namespace python = boost::python;

namespace orthos{


    void exportPlane(){
        python::class_<Plane>(
            "Plane",
            python::init<
                const std::string &,
                const int,
                const int,
                const int,
                const int
            >(
                (
                    python::arg("name"),
                    python::arg("xAxis"),
                    python::arg("yAxis"),
                    python::arg("zAxis") = -1,
                    python::arg("planeIndex") = -1
                )
            )
        )
            .add_property("name", &Plane::name)
            .add_property("xAxis", &Plane::xAxis)
            .add_property("yAxis", &Plane::yAxis)
            .add_property("zAxis", &Plane::zAxis)
            .add_property("name",  &Plane::name)
            .add_property("planeIndex",  &Plane::planeIndex, &Plane::setPlaneIndex)
        ;


        python::class_<PlaneVector>("PlaneVector",python::init<>())
            .def("addPlane",&PlaneVector::addPlane)
            .def("__len__",&PlaneVector::size)
            .def("__getitem__",&PlaneVector::getPlane, python::return_internal_reference<>())
        ;

    }

}
