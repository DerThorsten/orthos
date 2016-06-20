#ifndef  ORHTOS_CPP_PLANE_HXX
#define ORHTOS_CPP_PLANE_HXX


#include <string>
#include <vector>
#include <vigra/tinyvector.hxx>

namespace orthos{






    class Plane{

    public:
        Plane(const std::string & name,
              const int xAxis,
              const int yAxis,
              const int zAxis=-1,
              const int planeIndex = -1)
        :   name_(name),
            xAxis_(xAxis),
            yAxis_(yAxis),
            zAxis_(zAxis),
            planeIndex_(planeIndex){
        }
        std::string  name() const{
            return name_;
        }
        int xAxis()const{
            return xAxis_;
        }
        int yAxis()const{
            return yAxis_;
        }
        int zAxis()const{
            return zAxis_;
        }
        int planeIndex()const{
            return planeIndex_;
        }

        void setPlaneIndex(const int i){
            planeIndex_ = i;
        }

    private:
        // the name of the plane
        std::string name_;

        // the axis of the viewer 
        int xAxis_;
        int yAxis_;
        int zAxis_;

        // the index of the plaine
        int planeIndex_;
    };



    class PlaneVector{
    public:
        void addPlane(const Plane & plane ){
            const auto & name  = plane.name();
            auto fres = nameToIndex_.find(name);
            if(fres == nameToIndex_.end()){
                nameToIndex_[name] = planes_.size();
            }
            else{
                throw std::runtime_error("duplicate in planne names");
            }
            planes_.push_back(plane);
        }
        size_t size()const{
            return planes_.size();
        }
        const Plane & getPlane(const size_t i)const{
            return planes_[i];
        }
    private:
        std::vector<Plane> planes_;
        std::map<std::string, int> nameToIndex_;
        std::vector<int> planePosition_;
    };

}

#endif /* ORTHOS_CPP_PLANE_HXX */
