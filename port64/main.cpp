#include "assets.hpp"
#include "view.hpp"
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

int main(int argc, char** argv) {
    try {
        std::string hdi, archive, screenshot, extract, output, packed, inputs;
        std::string scene="title", picture="TL02.PI";
        bool headless=false, list=false;
        unsigned frames=0;
        for (int i=1;i<argc;++i) {
            const std::string arg=argv[i];
            if (arg=="--headless") { headless=true; continue; }
            if (arg=="--list") { list=true; continue; }
            if (arg=="--help") {
                std::cout<<"th03-port64 (--hdi FILE | --archive FILE) [--headless] [--scene title|menu|options]\n"
                         <<"  [--screenshot FILE.ppm] [--frames N] [--inputs WORD,WORD,...]\n"
                         <<"  [--list] [--extract NAME --output FILE] [--pi NAME --packed FILE]\n";
                return 0;
            }
            if (++i>=argc) throw std::runtime_error("missing option value");
            const std::string value=argv[i];
            if (arg=="--hdi") hdi=value;
            else if (arg=="--archive") archive=value;
            else if (arg=="--scene") scene=value;
            else if (arg=="--screenshot") screenshot=value;
            else if (arg=="--extract") extract=value;
            else if (arg=="--output") output=value;
            else if (arg=="--pi") picture=value;
            else if (arg=="--packed") packed=value;
            else if (arg=="--inputs") inputs=value;
            else if (arg=="--frames") frames=unsigned(std::stoul(value));
            else throw std::runtime_error("unknown option: "+arg);
        }
        if (hdi.empty()==archive.empty()) throw std::runtime_error("supply one original HDI or PF archive");
        Bytes disk;
        if (!hdi.empty()) disk=read_file(hdi);
        PfArchive assets(hdi.empty() ? read_file(archive) : hdi_file(disk,op_archive_name));
        if (list) {
            for (const auto& e:assets.entries()) std::cout<<e.name<<' '<<e.size<<'\n';
            return 0;
        }
        if (!extract.empty()) {
            if (output.empty()) throw std::runtime_error("--extract requires --output");
            write_file(output,assets.read(extract));
            return 0;
        }
        const auto background=decode_pi(assets.read(picture));
        if (!packed.empty()) {
            write_file(packed,background.pixels);
            std::cout<<background.width<<'x'<<background.height<<' '<<background.pixels.size()<<'\n';
            return 0;
        }
        const auto gaiji=assets.read("MIKOFT.BFT"), window=assets.read("OPWIN.BFT");
        th03::Menu menu;
        if (!disk.empty()) {
            const auto cfg=hdi_file(disk,"YUME    CFG");
            if (cfg.size()!=8 || cfg[0]>2 || cfg[1]>2 || cfg[2]>3) throw std::runtime_error("unsupported YUME.CFG");
            menu.options={cfg[0],cfg[1],cfg[2]};
        }
        if (scene=="menu" || scene=="options") { menu.tick(th03::left); menu.tick(0); }
        if (scene=="options") {
            for (int i=0;i<4;++i) { menu.tick(th03::down); menu.tick(0); }
            menu.tick(th03::shot); menu.tick(0);
        } else if (scene!="menu" && scene!="title") throw std::runtime_error("unknown scene");
        if (!inputs.empty()) {
            std::istringstream stream(inputs); std::string word;
            while (std::getline(stream,word,',')) {
                const auto value=std::stoul(word,nullptr,0);
                if (value>65535) throw std::runtime_error("input exceeds original WORD");
                menu.tick(std::uint16_t(value));
            }
        }
        const auto render=[&] { return th03::menu_frame(background,gaiji,window,menu); };
        if (!headless) run_view(menu,render,frames);
        if (!screenshot.empty()) write_file(screenshot,th03::ppm(render()));
        std::cout<<"screen="<<int(menu.screen)<<" selected="<<int(menu.selected)
                 <<" rank="<<int(menu.options.rank)<<" music="<<int(menu.options.music)
                 <<" keys="<<int(menu.options.keys)<<" handoff="<<int(menu.request)<<'\n';
        return 0;
    } catch (const std::exception& e) {
        std::cerr<<"TH03 port64: "<<e.what()<<'\n';
        return 1;
    }
}
