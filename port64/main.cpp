#include "assets.hpp"
#include "view.hpp"
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

int main(int argc, char** argv) {
    try {
        std::string hdi, archive, screenshot, extract, output, packed, inputs;
        std::string scene="title", picture="TL02.PI",font_bitmap,characters="1,3";
        unsigned stage=0;
        bool headless=false, list=false, main_assets=false;
        unsigned frames=0;
        for (int i=1;i<argc;++i) {
            const std::string arg=argv[i];
            if (arg=="--headless") { headless=true; continue; }
            if (arg=="--main-assets") {main_assets=true;continue;}
            if (arg=="--list") { list=true; continue; }
            if (arg=="--help") {
                std::cout<<"th03-port64 (--hdi FILE | --archive FILE) [--headless] [--scene title|menu|options|story-select|versus-select|two-select|stage-intro|battle-ready]\n"
                         <<"  [--font-bmp FILE] [--characters P1,P2] [--stage N]\n"
                         <<"  [--screenshot FILE.ppm] [--frames N] [--inputs SP[:P1:P2],...]\n"
                         <<"  [--main-assets] [--list] [--extract NAME --output FILE] [--pi NAME --packed FILE]\n";
                return 0;
            }
            if (++i>=argc) throw std::runtime_error("missing option value");
            const std::string value=argv[i];
            if (arg=="--hdi") hdi=value;
            else if (arg=="--archive") archive=value;
            else if (arg=="--font-bmp") font_bitmap=value;
            else if (arg=="--characters") characters=value;
            else if (arg=="--stage") stage=unsigned(std::stoul(value));
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
        PfArchive assets(hdi.empty() ? read_file(archive) : hdi_file(disk,main_assets ? main_archive_name : op_archive_name));
        if (list) {
            for (const auto& e:assets.entries()) std::cout<<e.name<<' '<<e.size<<'\n';
            return 0;
        }
        if (!extract.empty()) {
            if (output.empty()) throw std::runtime_error("--extract requires --output");
            write_file(output,assets.read(extract));
            return 0;
        }
        if (!packed.empty()) {
            const auto background=decode_pi(assets.read(picture));
            write_file(packed,background.pixels);
            std::cout<<background.width<<'x'<<background.height<<' '<<background.pixels.size()<<'\n';
            return 0;
        }
        th03::Options options;
        Bytes nem;
        if (!disk.empty()) {
            const auto cfg=hdi_file(disk,"YUME    CFG");
            if (cfg.size()!=8 || cfg[0]>2 || cfg[1]>2 || cfg[2]>3) throw std::runtime_error("unsupported YUME.CFG");
            options={cfg[0],cfg[1],cfg[2]};
            nem=hdi_file(disk,"YUME    NEM");
        }
        std::optional<PfArchive> main_archive;
        if(!disk.empty())main_archive.emplace(hdi_file(disk,main_archive_name));
        th03::Application app(assets,options,nem,picture,font_bitmap.empty() ? Bytes{} : read_file(font_bitmap),
                              main_archive ? &*main_archive : nullptr);
        auto& menu=app.menu;
        if (scene=="menu" || scene=="options") { menu.tick(th03::left); menu.tick(0); }
        if (scene=="options") {
            for (int i=0;i<4;++i) { menu.tick(th03::down); menu.tick(0); }
            menu.tick(th03::shot); menu.tick(0);
        } else if(scene=="story-select") {
            app.resident.begin_story();app.start_selection(th03::SelectKind::story);
        } else if(scene=="versus-select"||scene=="two-select") {
            app.resident.begin_versus(scene=="two-select" ? 1 : 0);
            app.start_selection(scene=="two-select" ? th03::SelectKind::two_player : th03::SelectKind::versus_cpu);
        } else if((scene=="stage-intro"||scene=="battle-ready")) {
            std::istringstream chars(characters);std::string value;unsigned at=0;
            app.resident.begin_story();
            while(std::getline(chars,value,',')) {
                const auto paletted=std::stoul(value);
                if(at>=2||paletted<1||paletted>18)throw std::runtime_error("characters require two palette IDs from 1 to 18");
                app.resident.paletted[at++]=std::uint8_t(paletted);
            }
            if(at!=2||stage>8)throw std::runtime_error("stage introduction needs two characters and stage 0 to 8");
            app.resident.stage=std::uint8_t(stage);app.resident.opponents[stage]=app.resident.paletted[1];
            if(scene=="battle-ready")app.start_main();else app.start_stage_intro();
        } else if (scene!="menu" && scene!="title") throw std::runtime_error("unknown scene");
        if (!inputs.empty()) {
            std::istringstream stream(inputs); std::string word;
            while (std::getline(stream,word,',')) {
                th03::InputFrame input;
                std::istringstream values(word);std::string value;
                unsigned at=0;
                while(std::getline(values,value,':')) {
                    const auto mask=std::stoul(value,nullptr,0);
                    if(mask>65535||at>2)throw std::runtime_error("input exceeds original WORD tuple");
                    if(at==0)input.single=std::uint16_t(mask);
                    else input.players[at-1]=std::uint16_t(mask);
                    ++at;
                }
                app.tick(input);
            }
        }
        const auto render=[&] { return app.render(); };
        if (!headless) run_view(app,render,frames);
        else for(unsigned i=0;i<frames&&!app.finished();++i)app.tick({});
        if (!screenshot.empty()) write_file(screenshot,th03::ppm(render()));
        std::cout<<"screen="<<int(menu.screen)<<" selected="<<int(menu.selected)
                 <<" rank="<<int(menu.options.rank)<<" music="<<int(menu.options.music)
                 <<" keys="<<int(menu.options.keys)<<" handoff="<<int(menu.request)
                 <<" phase="<<int(app.phase)<<" characters="<<int(app.resident.paletted[0])<<','<<int(app.resident.paletted[1])
                 <<" selection="<<int(app.selection.selected[0])<<','<<int(app.selection.selected[1])<<'\n';
        if(app.round) {
            const auto& round=*app.round;
            std::cout<<"round="<<unsigned(round.id)<<" speed="<<unsigned(round.speed)
                     <<" boss="<<unsigned(round.boss_level)<<" safety="<<round.players[1].cpu_safety
                     <<" formations="<<round.formations.size()<<" main_seed="<<round.random.seed<<'\n';
        }
        return 0;
    } catch (const std::exception& e) {
        std::cerr<<"TH03 port64: "<<e.what()<<'\n';
        return 1;
    }
}
