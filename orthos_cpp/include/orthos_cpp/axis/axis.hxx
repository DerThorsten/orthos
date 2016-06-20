
#include <string>
#include <vector>

#include <vigra/tinyvector.hxx>

namespace orthos{





class  TileRequest{
public:

private:
    std::vector<int> axisBegin_;
    std::vector<int> axisEnd_;
    int tilesXAxis_;
    int tilesYAxis_;
    int tilesZAxis_;
};



class Axis{
public:

    typedef vigra::TinyVector<int16_t, 4> Color;
    typedef std::vector<std::string> StringVector;

    Axis(
        const int64_t shape = -1,
        const std::string & name = std::string(),
        const std::string & shortName = std::string(),
        const Color  color = Color(-1),
        const bool isChannelAxis = false,
        const StringVector channelNames = StringVector()
    )   :
        shape_(shape),
        name_(name),
        shortName_(shortName),
        color_(color),
        isChannelAxis_(isChannelAxis),
        channelNames_(channelNames)
    {

    }

    std::string name()const{
        return name_;
    }
    std::string shortName()const{
        return shortName_;
    }
    bool isSingleton()const{
        return shape_ == 1;
    }
    bool isChannelAxis()const{
        return isChannelAxis_;
    }
    int64_t shape()const{
        return shape_;
    }

    bool hasName()const{
        return !name_.empty();
    }

    bool hasShortName()const{
        return !shortName_.empty();
    }

    bool hasColor()const{
        for(auto c=0; c<3; ++c)
            if(color_[c]<0)
                return false;
        return true;
    }
    bool hasAlpha()const{
        return color_[3] >= 0;
    }
    Color color()const{
        return color_;
    }
private:

    /// shape of the axis (we always start at 0)
    int64_t shape_;

    /// name of the axis as "X-Axis"
    std::string name_;
    /// short name of the axis as "x" or "x0"
    std::string shortName_;

    /// rgb-a color of the axis 
    /// negative values indicate missing color or 
    /// missing alpha channel
    Color color_;

    /// indicates if this axis is a channel axis
    bool isChannelAxis_;
    /// explict names for the channels like ["r","g","b"]
    std::vector<std::string> channelNames_;
};




class AxisVector{
public:
    AxisVector()
    :   axisVector_(){

    }

    int addAxis(const Axis & axis){

        if(nameToIndex_.find(axis.name())!=nameToIndex_.end()){
            throw std::runtime_error("duplicate in names");
        }
        if(shortNameToIndex_.find(axis.name())!=shortNameToIndex_.end()){
            throw std::runtime_error("duplicate in shortNames");
        }
        nameToIndex_[axis.name()] = axisVector_.size();
        shortNameToIndex_[axis.shortName()] = axisVector_.size();
        axisVector_.push_back(axis);
    }

    template<class OUT_ITER>
    void findAxis(const AxisVector other, OUT_ITER  outIter)const{
        for(const auto & a : other.axisVector_){
            auto resIter = nameToIndex_.find(a.name());
            if(resIter == nameToIndex_.end())
                *outIter = -1;
            else
                *outIter = resIter->second;
            ++outIter;
        }
    }

    int nChannelAxis()const{
        auto c = 0;
        for(const auto & a : axisVector_)
            c += a.isChannelAxis() ? 1 : 0;
        return c;
    }
    bool hasChannelAxis()const{
        auto c = 0;
        for(const auto & a : axisVector_){
            if(a.isChannelAxis()){
                return true;
            }
        }
        return false;
    } 

    int nSingletnAxis()const{
        auto c = 0;
        for(const auto & a : axisVector_)
            c += a.isSingleton() ? 1 : 0;
        return c;
    }
    bool hasSingletonAxis()const{
        auto c = 0;
        for(const auto & a : axisVector_)
            if(a.isSingleton())
                return true;
        return false;
    } 

    std::vector<size_t> shape()const{
        std::vector<size_t> ret(axisVector_.size());
        auto i = 0;
        for(const auto a :axisVector_){
            ret[i] = a.shape();
            ++i;
        }
        return std::move(ret);
    }

    size_t size()const{
        return axisVector_.size();
    }
    const Axis & getAxis(const size_t a)const{
        return axisVector_[a];
    }
private:
    std::vector<Axis> axisVector_;
    std::map<std::string, int> nameToIndex_;
    std::map<std::string, int> shortNameToIndex_;
};








}
