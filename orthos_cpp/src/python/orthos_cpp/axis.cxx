#define PY_ARRAY_UNIQUE_SYMBOL vigranumpyorthos_PyArray_API
#define NO_IMPORT_ARRAY


/*orthos*/
#include <orthos_cpp/orthos.hxx>
#include <orthos_cpp/axis/axis.hxx>
/*vigra python */
#include <vigra/numpy_array.hxx>
#include <vigra/numpy_array_converters.hxx>
#include <vigra/python_utility.hxx>
#include <boost/python/stl_iterator.hpp>

namespace python = boost::python;

namespace orthos{


Axis * pyAxisFactory(
    const int64_t shape,
    const std::string & name,
    const std::string & shortName,
    python::object colorObj,
    const bool isChannelAxis,
    const Axis::StringVector channelNames
){
    python::stl_input_iterator<int> begin(colorObj), end;
    Axis::Color color(-1);
    auto c = 0;
    while(begin!=end){
        color[c] = *begin;
        ++begin;
        ++c;
    }
    return new Axis(shape, name, shortName, color, isChannelAxis, channelNames);
}

python::tuple pyColor(const Axis & a){
    const auto  c = a.color();
    return python::make_tuple(c[0], c[1], c[2], c[3]);
}


python::list axisVectorShape(const AxisVector & axisVector){
    auto shape = axisVector.shape();
    python::list ret;
    for(auto s : shape)
        ret.append(s);
    return ret;
}

vigra::NumpyAnyArray pyFindAxis(const AxisVector & self, const AxisVector & other,
                                vigra::NumpyArray<1, int32_t> out){
    out.reshapeIfEmpty(vigra::NumpyArray<1, int32_t>::difference_type(other.size()));
    self.findAxis(other, out.begin());
    return out;
}

void exportAxis(){

    python::class_< std::vector<std::string> >("StringVector",python::init<>())
    ;



    python::class_<Axis>( "Axis",  python::init<>())
        .def("hasShortName",&Axis::hasShortName)
        .def("hasColor",&Axis::hasColor)
        .def("hasAlpha",&Axis::hasAlpha)
        .def("isChannelAxis",&Axis::isChannelAxis)
        .def("isSingleton", &Axis::isSingleton)
        .add_property("color", &pyColor)
        .add_property("shape", &Axis::shape)
        .add_property("name", &Axis::name)
        .add_property("shortName", &Axis::shortName)
        .add_property("shape", &Axis::shape)
    ;

    python::def("_axis",vigra::registerConverters(&pyAxisFactory),
        (
            python::arg("shape"),
            python::arg("name"),
            python::arg("shortName"),
            python::arg("color") = python::make_tuple(-1,-1,-1,-1),
            python::arg("isChannelAxis") = false,
            python::arg("channelNames") = Axis::StringVector()
        ),
        python::return_value_policy<python::manage_new_object>()
    );



    python::class_<AxisVector>("AxisVector", python::init<>())
        .def("addAxis",&AxisVector::addAxis)
        .def("hasChannelAxis",&AxisVector::hasChannelAxis)
        .def("nChannelAxis",&AxisVector::nChannelAxis)
        .def("hasSingletonAxis",&AxisVector::hasSingletonAxis)
        .def("nSingletnAxis",&AxisVector::nSingletnAxis)
        .def("findAxis",vigra::registerConverters(&pyFindAxis),
            (
                python::arg("otherAxis"),
                python::arg("out") = python::object()
            )
        )
        .add_property("shape", &axisVectorShape)

        // special
        .def("__len__",&AxisVector::size)
        .def("__getitem__",&AxisVector::getAxis,python::return_internal_reference<>())
    ;
}

}
