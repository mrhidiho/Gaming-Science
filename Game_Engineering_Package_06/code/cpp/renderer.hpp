#pragma once
// Package 06: CPU reference, not a production renderer or GPU emulator.
// RH view, camera looks -Z, column-vector transform, clip Z in [0,W].
// Screen origin upper-left; 1/256-pixel fixed-point coverage; strict-less depth.
#include <algorithm>
#include <array>
#include <bit>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace ge {
struct V2 { double x{}, y{}; };
struct V3 { double x{}, y{}, z{}; };
struct V4 { double x{}, y{}, z{}, w{}; };
struct Vertex { V4 p; V2 uv; V3 color{1,1,1}; };
using Triangle=std::array<Vertex,3>;
inline bool finite(V4 v) { return std::isfinite(v.x)&&std::isfinite(v.y)&&std::isfinite(v.z)&&std::isfinite(v.w); }
inline double srgb_encode(double x) {
    if(!std::isfinite(x)) throw std::invalid_argument("nonfinite color");
    x=std::clamp(x,0.0,1.0);
    return x<=0.0031308 ? 12.92*x : 1.055*std::pow(x,1.0/2.4)-0.055;
}
inline double srgb_decode(double x) {
    if(!std::isfinite(x)||x<0||x>1) throw std::invalid_argument("invalid sRGB sample");
    return x<=0.04045 ? x/12.92 : std::pow((x+0.055)/1.055,2.4);
}
inline V4 project(V3 p,double aspect,double fovy=1.0471975511965976,double near_z=.1,double far_z=20) {
    if(!std::isfinite(aspect)||aspect<=0||!std::isfinite(fovy)||fovy<=0||fovy>=3.141592653589793||
       !std::isfinite(near_z)||!std::isfinite(far_z)||near_z<=0||far_z<=near_z)
        throw std::invalid_argument("projection domain");
    const double s=1/std::tan(fovy/2), a=far_z/(near_z-far_z), b=far_z*near_z/(near_z-far_z);
    return {s/aspect*p.x,s*p.y,a*p.z+b,-p.z};
}
inline double plane_distance(V4 p,int plane) {
    switch(plane) { case 0:return p.x+p.w;case 1:return p.w-p.x;case 2:return p.y+p.w;
      case 3:return p.w-p.y;case 4:return p.z;case 5:return p.w-p.z;default:throw std::invalid_argument("plane index"); }
}
inline Vertex lerp(Vertex a,Vertex b,double t) {
    auto f=[t](double x,double y){return x+(y-x)*t;};
    return {{f(a.p.x,b.p.x),f(a.p.y,b.p.y),f(a.p.z,b.p.z),f(a.p.w,b.p.w)},
            {f(a.uv.x,b.uv.x),f(a.uv.y,b.uv.y)},
            {f(a.color.x,b.color.x),f(a.color.y,b.color.y),f(a.color.z,b.color.z)}};
}
inline std::vector<Vertex> clip_polygon(std::vector<Vertex> points) {
    for(const auto& v:points)
        if(!finite(v.p)||!std::isfinite(v.uv.x)||!std::isfinite(v.uv.y)||
           !std::isfinite(v.color.x)||!std::isfinite(v.color.y)||!std::isfinite(v.color.z))
            throw std::invalid_argument("nonfinite vertex");
    for(int plane=0;plane<6&&!points.empty();++plane) {
        std::vector<Vertex> out;
        Vertex prev=points.back();double dp=plane_distance(prev.p,plane);
        for(const auto& cur:points) {
            const double dc=plane_distance(cur.p,plane);
            if((dp>=0)!=(dc>=0)) out.push_back(lerp(prev,cur,dp/(dp-dc)));
            if(dc>=0) out.push_back(cur);
            prev=cur;dp=dc;
        }
        points=std::move(out);
    }
    return points;
}
struct ScreenVertex { std::int64_t x{},y{};double inv_w{},z{}; V2 uv;V3 color; };
inline ScreenVertex to_screen(Vertex v,int width,int height) {
    if(!finite(v.p)||v.p.w<=0) throw std::invalid_argument("perspective division requires positive finite w");
    const double q=1/v.p.w;
    const double x=(v.p.x*q*.5+.5)*width, y=(.5-v.p.y*q*.5)*height;
    if(!std::isfinite(x)||!std::isfinite(y)||x < -1 || x>width+1 || y < -1 || y>height+1)
        throw std::invalid_argument("vertex was not clipped");
    return {std::llround(x*256),std::llround(y*256),q,v.p.z*q,v.uv,v.color};
}
inline std::int64_t edge(const ScreenVertex& a,const ScreenVertex& b,std::int64_t x,std::int64_t y) {
    return (b.x-a.x)*(y-a.y)-(b.y-a.y)*(x-a.x);
}
inline bool inclusive_edge(const ScreenVertex& a,const ScreenVertex& b) {
    const auto dx=b.x-a.x,dy=b.y-a.y;
    return dy<0||(dy==0&&dx>0); // y down, normalized positive signed area
}
inline bool inside_edge(std::int64_t value,const ScreenVertex& a,const ScreenVertex& b) {
    return value>0||(value==0&&inclusive_edge(a,b));
}
inline double perspective(const std::array<double,3>& weights,const std::array<double,3>& value,
                          const std::array<double,3>& w) {
    double sum=0,num=0,den=0;
    for(int i=0;i<3;++i) {
        if(!std::isfinite(weights[i])||weights[i]<0||!std::isfinite(value[i])||!std::isfinite(w[i])||w[i]<=0)
            throw std::invalid_argument("invalid interpolant");
        sum+=weights[i];num+=weights[i]*value[i]/w[i];den+=weights[i]/w[i];
    }
    if(std::abs(sum-1)>1e-9||den<=0)throw std::invalid_argument("invalid barycentric sum");
    return num/den;
}
struct Image {
    int width,height;
    std::vector<V3> color;
    std::vector<double> depth;
    std::vector<unsigned> coverage; // diagnostic coverage BEFORE depth test
    explicit Image(int w,int h):width(w),height(h) {
        if(w<=0||h<=0||w>4096||h>4096)throw std::invalid_argument("extent must be 1..4096");
        const auto n=static_cast<std::size_t>(w)*static_cast<std::size_t>(h);
        color.assign(n,{.018,.025,.04});depth.assign(n,1.0);coverage.assign(n,0);
    }
};
inline void raster_triangle(Image& image,Triangle t,bool affine=false,bool checker=true) {
    auto a=to_screen(t[0],image.width,image.height),b=to_screen(t[1],image.width,image.height),c=to_screen(t[2],image.width,image.height);
    auto area=edge(a,b,c.x,c.y);
    if(area==0)return;
    if(area<0){std::swap(b,c);area=-area;}
    const int minx=std::max(0,static_cast<int>(std::min({a.x,b.x,c.x})/256));
    const int miny=std::max(0,static_cast<int>(std::min({a.y,b.y,c.y})/256));
    const int maxx=std::min(image.width-1,static_cast<int>(std::max({a.x,b.x,c.x})/256));
    const int maxy=std::min(image.height-1,static_cast<int>(std::max({a.y,b.y,c.y})/256));
    for(int y=miny;y<=maxy;++y)for(int x=minx;x<=maxx;++x) {
        const auto sx=static_cast<std::int64_t>(x)*256+128,sy=static_cast<std::int64_t>(y)*256+128;
        const auto e0=edge(b,c,sx,sy),e1=edge(c,a,sx,sy),e2=edge(a,b,sx,sy);
        if(!inside_edge(e0,b,c)||!inside_edge(e1,c,a)||!inside_edge(e2,a,b))continue;
        const auto index=static_cast<std::size_t>(y)*static_cast<std::size_t>(image.width)+static_cast<std::size_t>(x);
        ++image.coverage[index];
        const double l0=static_cast<double>(e0)/static_cast<double>(area),l1=static_cast<double>(e1)/static_cast<double>(area),l2=static_cast<double>(e2)/static_cast<double>(area);
        // NDC depth is already projected: interpolate it affinely, not as a varying.
        const double z=l0*a.z+l1*b.z+l2*c.z;
        if(z<0||z>1||!(z<image.depth[index]))continue;
        double q0=l0,q1=l1,q2=l2;
        if(!affine){q0*=a.inv_w;q1*=b.inv_w;q2*=c.inv_w;const double den=q0+q1+q2;q0/=den;q1/=den;q2/=den;}
        const double u=q0*a.uv.x+q1*b.uv.x+q2*c.uv.x,v=q0*a.uv.y+q1*b.uv.y+q2*c.uv.y;
        // Procedural point-sampled checker; intentionally aliases without the learner's filtering lab.
        const auto tile=static_cast<long long>(std::floor(u*8))+static_cast<long long>(std::floor(v*8));
        const double value=checker ? (tile%2==0 ? .9:.08):1;
        image.color[index]={(q0*a.color.x+q1*b.color.x+q2*c.color.x)*value,
                            (q0*a.color.y+q1*b.color.y+q2*c.color.y)*value,
                            (q0*a.color.z+q1*b.color.z+q2*c.color.z)*value};
        image.depth[index]=z;
    }
}
inline void draw(Image& image,const Triangle& triangle,bool affine=false,bool checker=true) {
    auto p=clip_polygon({triangle[0],triangle[1],triangle[2]});
    if(p.size()<3)return;
    for(std::size_t i=1;i+1<p.size();++i) {
        // A clip-space origin can survive the six planes but cannot be divided.
        if(p[0].p.w<=0||p[i].p.w<=0||p[i+1].p.w<=0)continue;
        raster_triangle(image,{p[0],p[i],p[i+1]},affine,checker);
    }
}
inline void write_ppm(const Image& image,const std::string& path) {
    std::ofstream out(path,std::ios::binary); if(!out)throw std::runtime_error("cannot open output "+path);
    out<<"P6\n# sRGB-encoded RGB8 variant; origin upper-left; opaque\n"<<image.width<<' '<<image.height<<"\n255\n";
    for(auto c:image.color)for(double channel:{c.x,c.y,c.z}){
        const unsigned char value=static_cast<unsigned char>(std::lround(srgb_encode(channel)*255));
        out.write(reinterpret_cast<const char*>(&value),1);
    }
    if(!out)throw std::runtime_error("failed writing PPM");
}
inline std::vector<Triangle> demo_mesh() {
    auto v=[](double x,double y,double z,double u,double t,V3 c){return Vertex{{x,y,z,1},{u,t},c};};
    const auto a=v(-1.5,-.7,-1,0,0,{.7,.9,1}),b=v(1.5,-.7,-1,1,0,{.7,.9,1}),
               c=v(1.5,-.7,-7,1,1,{.7,.9,1}),d=v(-1.5,-.7,-7,0,1,{.7,.9,1});
    return {{a,b,c},{a,c,d},
      {v(-.7,-.4,-2.6,0,0,{1,.3,.1}),v(.7,-.4,-2.6,1,0,{1,.3,.1}),v(0,.8,-2.6,.5,1,{1,.8,.2})},
      {v(.02,.01,-.05,0,0,{.2,1,.6}),v(.9,.1,-1.6,1,0,{.2,1,.6}),v(.7,.7,-1.6,.5,1,{.2,1,.6})}};
}
inline std::uint32_t read_u32(std::istream& in) {
    std::array<unsigned char,4> b{};in.read(reinterpret_cast<char*>(b.data()),4);
    if(!in)throw std::runtime_error("truncated cooked mesh");
    return std::uint32_t(b[0])|(std::uint32_t(b[1])<<8)|(std::uint32_t(b[2])<<16)|(std::uint32_t(b[3])<<24);
}
inline std::vector<Triangle> load_gem(const std::string& path) {
    static_assert(sizeof(float)==4&&std::numeric_limits<float>::is_iec559,"GEM1 requires IEEE binary32");
    std::ifstream in(path,std::ios::binary);if(!in)throw std::runtime_error("cannot open mesh "+path);
    char magic[4]{};in.read(magic,4);
    if(!in||std::string(magic,4)!="GEM1")throw std::runtime_error("bad mesh magic");
    const auto count=read_u32(in);
    if(count==0||count>300000||count%3!=0)throw std::runtime_error("invalid triangle vertex count");
    std::vector<Triangle> mesh(count/3);
    for(std::uint32_t i=0;i<count;++i){
        std::array<double,8> f{};
        for(auto& x:f){x=static_cast<double>(std::bit_cast<float>(read_u32(in)));if(!std::isfinite(x)||std::abs(x)>10000)throw std::runtime_error("invalid cooked component");}
        if(f[5]<0||f[5]>1||f[6]<0||f[6]>1||f[7]<0||f[7]>1)throw std::runtime_error("color outside [0,1]");
        mesh[i/3][i%3]={{f[0],f[1],f[2],1},{f[3],f[4]},{f[5],f[6],f[7]}};
    }
    if(in.peek()!=std::char_traits<char>::eof())throw std::runtime_error("unexpected mesh trailing data");
    return mesh;
}
inline void render(Image& image,const std::vector<Triangle>& world,bool affine=false) {
    for(auto tri:world){
        for(auto& v:tri)v.p=project({v.p.x,v.p.y,v.p.z},double(image.width)/image.height);
        draw(image,tri,affine,true);
    }
}
} // namespace ge
