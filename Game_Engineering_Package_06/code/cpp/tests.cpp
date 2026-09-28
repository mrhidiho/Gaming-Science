#include "renderer.hpp"
#include <functional>
#include <iostream>
#include <filesystem>
#include <iterator>
#include <sstream>
using namespace ge;
int checks=0;
void require(bool ok,const std::string& message){++checks;if(!ok)throw std::runtime_error(message);}
void close(double a,double b,const std::string& m){require(std::abs(a-b)<1e-9,m);}
template<class F> void rejects(F f,const std::string& m){bool threw=false;try{f();}catch(const std::exception&){threw=true;}require(threw,m);}
Vertex v(double x,double y,double z=.5,double w=1){return {{x,y,z,w},{0,0},{1,0,0}};}
int main(){
    try{
        close(srgb_encode(0),0,"black");close(srgb_encode(1),1,"white");close(srgb_decode(srgb_encode(.18)),.18,"sRGB roundtrip");
        rejects([]{srgb_encode(std::numeric_limits<double>::quiet_NaN());},"reject nan color");
        rejects([]{Image i(0,10);},"zero image");rejects([]{Image i(4097,1);},"extent policy");
        auto pn=project({0,0,-.1},1),pf=project({0,0,-20},1);close(pn.z/pn.w,0,"near maps0");close(pf.z/pf.w,1,"far maps1");
        rejects([]{project({0,0,-1},0);},"zero aspect");rejects([]{to_screen(v(0,0,0,0),8,8);},"zero w divide");
        require(clip_polygon({v(-.5,-.5),v(.5,-.5),v(0,.5)}).size()==3,"inside unchanged");
        require(clip_polygon({v(2,0),v(3,0),v(2,.5)}).empty(),"outside removed");
        auto p=clip_polygon({v(-.5,-.5,-.5),v(.5,-.5,.5),v(0,.5,.5)});require(p.size()==4,"near crossing quad");
        for(auto a:p)for(int i=0;i<6;++i)require(plane_distance(a.p,i)>=-1e-12,"all clip inequalities");
        const std::array<Vertex,6> outside={v(-2,0),v(2,0),v(0,-2),v(0,2),v(0,0,-1),v(0,0,2)};
        for(auto a:outside){auto q=clip_polygon({a,v(-.1,-.1),v(.1,.1)});require(!q.empty(),"cross plane nonempty");for(auto b:q)for(int k=0;k<6;++k)require(plane_distance(b.p,k)>=-1e-12,"six plane clipping");}
        rejects([]{clip_polygon({v(std::numeric_limits<double>::infinity(),0)});},"nonfinite clip");
        Image rect(8,8);draw(rect,{v(-1,1),v(1,1),v(1,-1)},false,false);draw(rect,{v(-1,1),v(1,-1),v(-1,-1)},false,false);
        require(std::all_of(rect.coverage.begin(),rect.coverage.end(),[](unsigned c){return c==1;}),"shared diagonal exactly once, all64 samples");
        Image reverse(8,8);draw(reverse,{v(1,-1),v(1,1),v(-1,1)},false,false);draw(reverse,{v(-1,-1),v(1,-1),v(-1,1)},false,false);
        require(rect.coverage==reverse.coverage,"winding invariant coverage");
        Image empty(8,8);draw(empty,{v(0,0),v(0,0),v(0,0)},false,false);require(std::all_of(empty.coverage.begin(),empty.coverage.end(),[](unsigned c){return c==0;}),"degenerate skipped");
        auto neartri=Triangle{v(-1,1,.2),v(1,1,.2),v(0,-1,.2)};auto fartri=Triangle{v(-1,1,.8),v(1,1,.8),v(0,-1,.8)};
        for(auto& a:fartri){a.color={0,1,0};}
        Image first(8,8),second(8,8);
        draw(first,neartri,false,false);draw(first,fartri,false,false);draw(second,fartri,false,false);draw(second,neartri,false,false);
        require(first.depth==second.depth,"depth draw-order independent");require(first.color[3*8+3].x==1,"nearest red wins");
        close(perspective({.2,.3,.5},{0,1,1},{1,2,4}),11.0/19,"perspective fixture");
        rejects([]{perspective({1,0,0},{0,1,2},{0,1,1});},"bad perspective w");
        Image far(8,8);draw(far,{v(-1,1,1),v(1,1,1),v(0,-1,1)},false,false);require(far.color[27].x==.018,"strict less far-plane policy");
        const auto temp=std::filesystem::temp_directory_path()/"ge_package06_test.ppm";write_ppm(rect,temp.string());
        std::ifstream in(temp,std::ios::binary);std::string all((std::istreambuf_iterator<char>(in)),{});
        require(all.rfind("P6\n",0)==0,"ppm magic");auto offset=all.find("\n255\n");require(offset!=std::string::npos&&all.size()-offset-5==8*8*3,"ppm exact payload");std::filesystem::remove(temp);
        const auto bad=std::filesystem::temp_directory_path()/"ge_package06_bad.gem";{std::ofstream o(bad,std::ios::binary);o<<"GEM1";}
        rejects([&]{load_gem(bad.string());},"truncated cooked file");std::filesystem::remove(bad);
        Image scene(160,90);render(scene,demo_mesh());require(std::count_if(scene.depth.begin(),scene.depth.end(),[](double d){return d<1;})>1000,"scene covers pixels");
        std::cout<<checks<<" assertions passed\n";return 0;
    }catch(const std::exception& e){std::cerr<<"Failed after "<<checks<<" assertions: "<<e.what()<<'\n';return 1;}
}
