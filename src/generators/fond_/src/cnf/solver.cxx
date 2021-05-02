
#include "solver.h"
#include "options.h"
#include <common/macros.h>

#include <common/utils.h>
#include <boost/lexical_cast.hpp>

#include <boost/algorithm/string.hpp>
#include <iostream>

namespace sltp::cnf {

int call(const std::string& cmd, bool verbose) {
    if (verbose) {
        std::cout << "Calling: " << cmd << std::endl;
    }
    auto res = system((cmd).c_str());
    if (verbose) {
        std::cout << "Call returned with exit code " << res << std::endl;
    }
    return res;
}

SatSolution solve_cnf(const std::string& cnf_filename, const std::string& output_filename, bool verbose) {
    call("open-wbo_static " + cnf_filename + " > " + output_filename, verbose);
//    call("clasp --quiet=1 --configuration=jumpy  --parse-maxsat " + cnf_filename + " > " + output_filename, verbose);
    auto solutionf = utils::get_ifstream(output_filename);
    std::string line;

    SatSolution solution;

    while (std::getline(solutionf, line)) {
        const char code = line[0];
        std::string content = line.substr(std::min((unsigned) 2, (unsigned) line.size()));
        boost::trim(content);

        if (code == 'o') {
            solution.cost = std::min(solution.cost, boost::lexical_cast<int>(content));
        } else if (code == 's') {
            solution.result = content;
            if (content == "OPTIMUM FOUND" || content == "SATISFIABLE") {
                solution.solved = true;
            }
        } else if (code == 'v') {
            std::vector<std::string> literals;
            boost::split(literals, content, boost::is_any_of(" "));
            for (const auto& lit:literals) {
                int val = boost::lexical_cast<int>(lit);
                if (std::abs(val)+1>solution.assignment.size()) solution.assignment.resize(std::abs(val)+1);
                if (val > 0) {
                    solution.assignment.at(val) = true;
                }
            }
        }
    }
    solutionf.close();
    return solution;
}


} // namespaces