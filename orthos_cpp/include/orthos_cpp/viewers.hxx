#ifndef ORTHOS_CPP_VIEWERS_HXX
#define ORTHOS_CPP_VIEWERS_HXX


namespace orthos{


    /*
     *
     *
     *  User Declares Canonical axis tags
     *  and then data Sources 
     *
     *
     *  User declare their data-sources with axistags
     *  source('xyzc') means 4d with the last axis beeing channel
     *  
     *  source('txy') means time is first axis, then xy and no channels 
     *
     *
     *  From now on, internal, we can use an integer wrt the canonical ordering
     *  
     * Then they register 'orthogonal plane viewers'
     *   
     *
     */


    struct AxisTag{
        std::string tag_;
        bool        isChannelAxis_;
        int         canonicalPosition_;
    };




    class ViewerData{
    public:

    private:

    };

    class ViewersData{

    };  

}

#endif
