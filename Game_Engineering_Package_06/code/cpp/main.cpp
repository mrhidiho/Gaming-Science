#include "renderer.hpp"
#include <chrono>
#include <iostream>
int main(int argc,char** argv) {
    try {
        std::string output="reference.ppm",mesh_path;
        int width=320,height=180;bool affine=false;
        for(int i=1;i<argc;++i) {
            const std::string a=argv[i];
            if(a=="--affine")affine=true;
            else if((a=="--output"||a=="--mesh"||a=="--width"||a=="--height")&&i+1<argc){
                const std::string value=argv[++i];
                if(a=="--output")output=value;else if(a=="--mesh")mesh_path=value;
                else {std::size_t used=0;int n=std::stoi(value,&used);if(used!=value.size())throw std::invalid_argument("invalid integer");if(a=="--width")width=n;else height=n;}
            } else throw std::invalid_argument("Usage: cpu_renderer [--output image.ppm] [--mesh asset.gem] [--width 320] [--height 180] [--affine]");
        }
        auto mesh=mesh_path.empty()?ge::demo_mesh():ge::load_gem(mesh_path);
        ge::Image image(width,height);
        const auto begin=std::chrono::steady_clock::now();ge::render(image,mesh,affine);
        const double ms=std::chrono::duration<double,std::milli>(std::chrono::steady_clock::now()-begin).count();
        ge::write_ppm(image,output);
        std::cout<<"{\"width\":"<<width<<",\"height\":"<<height<<",\"triangles\":"<<mesh.size()<<",\"cpu_render_ms\":"<<ms<<",\"gpu_tested\":false}\n";
        return 0;
    } catch(const std::exception& e){std::cerr<<"error: "<<e.what()<<'\n';return 1;}
}
