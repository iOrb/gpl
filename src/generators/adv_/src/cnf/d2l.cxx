
#include "d2l.h"
#include "types.h"

#include <iostream>
#include <vector>
#include <unordered_map>

#include <boost/functional/hash.hpp>
#include <common/helpers.h>


namespace sltp::cnf {


    transition_denotation compute_transition_denotation(FeatureMatrix::feature_value_t s_f, FeatureMatrix::feature_value_t sprime_f) {
        int type_s = (int) sprime_f - (int) s_f; // <0 if DEC, =0 if unaffected, >0 if INC
        int sign = (type_s > 0) ? 1 : ((type_s < 0) ? -1 : 0); // Get the sign
        return transition_denotation(bool(s_f > 0), sign);
    }


    void D2LEncoding::compute_equivalence_relations() {
        // A mapping from a full transition trace to the ID of the corresponding equivalence class
        std::unordered_map<transition_trace, unsigned> from_trace_to_class_repr;

        for (const auto& [s, a, sp, spps]:sample_.transitions_.transitions()) {
            auto tx = std::make_pair((state_id_t) s, (state_id_t) sp);
            auto id = (unsigned) transition_ids_inv_.size(); // Assign a sequential ID to the transition

            transition_ids_inv_.push_back(tx);
            auto it1 = transition_ids_.emplace(tx, id);
            assert(it1.second);

            bool all_spp_solvable = true;
            for (auto const& spp:spps) {
                if (!sample_.is_solvable(spp)) {
                    all_spp_solvable = false;
                }
            }

            if (!all_spp_solvable) { // An alive-to-dead transition cannot be Good
                necessarily_bad_transitions_.emplace(id);
            }

            if (!options.use_equivalence_classes) {
                // If we don't want to use equivalence classes, we simply create one fictitious equivalence class
                // for each transition, and proceed as usual
                from_transition_to_eq_class_.push_back(id);
                class_representatives_.push_back(id);
                continue;
            }

            // Compute the trace of the transition for all features
            transition_trace trace;
            for (auto f:feature_ids) {
                trace.denotations.emplace_back(
                        compute_transition_denotation(sample_.value(s, f), sample_.value(sp, f)));
            }

            // Check whether some previous transition has the same transition trace
            auto it = from_trace_to_class_repr.find(trace);
            if (it == from_trace_to_class_repr.end()) {
                // We have a new equivalence class, to which we assign the ID of the representative transition
                from_transition_to_eq_class_.push_back(id);
                from_trace_to_class_repr.emplace(trace, id);
                class_representatives_.push_back(id);
            } else {
                // We already have other transitions undistinguishable from this one
                assert(it->second < id);
                from_transition_to_eq_class_.push_back(it->second);

//                if (types_[it->second] != types_[id]) {
//                    // We have to non-distinguishable transitions, one from alive to solvable, and one from alive
//                    // to dead; hence, both will need to be labeled as not Good
//                    throw std::runtime_error("Found two non-distinguishable transitions with different types");
//                }
            }
        }

        // All transitions that belong to some class where at least one transition must be bad, must be bad
        std::unordered_set<unsigned> necessarily_bad_classes;
        for (const auto id:necessarily_bad_transitions_) {
            necessarily_bad_classes.insert(get_representative_id(id));
        }

        for (unsigned id=0; id < transition_ids_.size(); ++id) {
            auto repr = get_representative_id(id);
            if (necessarily_bad_classes.find(repr) != necessarily_bad_classes.end()) {
                necessarily_bad_transitions_.insert(id);
            }
        }

        // Print some stats
        if (options.verbosity > 0) {
            std::cout << "Number of transitions/equivalence classes: " << transition_ids_.size()
                      << "/" << class_representatives_.size() << std::endl;
            std::cout << "Number of necessarily bad transitions/classes: " << necessarily_bad_transitions_.size()
                      << "/" << necessarily_bad_classes.size() << std::endl;
        }

//    report_eq_classes();
    }

    void D2LEncoding::report_eq_classes() const {
        std::unordered_map<unsigned, std::vector<state_pair>> classes;
        for (unsigned tx=0; tx < transition_ids_.size(); ++tx) {
            auto repr = get_representative_id(tx);
            classes[repr].push_back(get_state_pair(tx));
        }

        unsigned i = 0;
        for (const auto& elem:classes) {
            std::cout << "Class " << ++i << ": " << std::endl;
            const auto& elements = elem.second;
            for (unsigned j = 0; j < elements.size(); ++j) {
                const auto& txpair = elements[j];
                std::cout << "(" << txpair.first << ", " << txpair.second << ")";
                if (j < elements.size()-1) std::cout << "; ";
            }
            std::cout << std::endl << std::endl;
        }
    }


    std::pair<cnf::CNFGenerationOutput, VariableMapping> D2LEncoding::generate(CNFWriter& wr)
    {
        using Wr = CNFWriter;
        const auto& mat = sample_.matrix();
        const auto num_transitions = transition_ids_.size();

        VariableMapping variables(nf_);

        auto varmapstream = utils::get_ofstream(options.workspace + "/varmap.wsat");

        // Keep a map from pairs (s, d) to SAT variable ID of the variable V(s, d)
        std::unordered_map<std::pair<unsigned, unsigned>, cnfvar_t, boost::hash<state_pair>> vs;

        unsigned n_descending_clauses = 0;
        unsigned n_v_function_clauses = 0;
        unsigned n_good_tx_clauses = 0;
        unsigned n_selected_clauses = 0;
        unsigned n_separation_clauses = 0;
        unsigned n_goal_clauses = 0;
        unsigned n_bad_states_clauses = 0;

        if (options.verbosity>0) {
            std::cout << "Generating CNF encoding for " << sample_.transitions_.all_alive().size() << " alive states, "
                      <<  transition_ids_.size() << " alive-to-solvable and alive-to-dead transitions and "
                      << class_representatives_.size() << " transition equivalence classes" << std::endl;
        }

        const unsigned max_d = compute_D();

        /////// CNF variables ///////
        // Create one "Select(f)" variable for each feature f in the pool
        for (unsigned f:feature_ids) {
            auto v = wr.var("Select(" + mat.feature_name(f) + ")");
            variables.selecteds[f] = v;
        }

        // Create variables V(s, d) variables for all alive state s and d in 1..D
        for (const auto s:sample_.transitions_.all_alive()) {
            const auto min_vs = get_vstar(s);
            const auto max_vs = get_max_v(s);
            assert(max_vs > 0 && max_vs <= max_d && min_vs <= max_vs);

            cnfclause_t within_range_clause;

            // TODO Note that we could be more efficient here and create only variables V(s,d) for those values of d that
            //  are within the bounds below. I'm leaving that as a future optimization, as it slightly complicates the
            //  formulation of constraints C2
            for (unsigned d = 1; d <= max_d; ++d) {
                const auto v_s_d = wr.var("V(" + std::to_string(s) + ", " + std::to_string(d) + ")");
                vs.emplace(std::make_pair(s, d), v_s_d);
//                std::cout << s << ", " << d << std::endl;

                if (d >= min_vs && d <= max_vs) {
                    within_range_clause.push_back(Wr::lit(v_s_d, true));
                }
            }

            // Add clauses C3-4
            wr.cl(within_range_clause);
            n_v_function_clauses += 1;

            for (unsigned d = 1; d <= max_d; ++d) {
                for (unsigned dpp = d+1; dpp <= max_d; ++dpp) {
                    wr.cl({Wr::lit(vs.at({s, d}), false), Wr::lit(vs.at({s, dpp}), false)});
                    n_v_function_clauses += 1;
                }
            }
        }

        // Create all variables Good(s, a) for any possible pair (s, a) in a non-det transition (s, a, s').
        // We use this loop to index possible non-det transitions in maps s_to_as and s_a_to_s too.
        using sa_pair_t = std::pair<unsigned, unsigned>;
        std::unordered_map<unsigned, std::unordered_set<unsigned>> s_to_as;
        std::unordered_map<sa_pair_t, std::unordered_set<unsigned>, boost::hash<sa_pair_t>> s_a_to_spp;

        for (const auto& [s, a, sp, spps]:sample_.transitions_.transitions()) {
            if (sample_.is_alive(s)) {
                if (variables.goods_s_a.find({s, a}) == variables.goods_s_a.end()) {
                    auto good_s_a_var = wr.var("Good(" + std::to_string(s) + ", " + std::to_string(a) + ")");
                    varmapstream << good_s_a_var << " " << s << " " << a << std::endl;
                    variables.goods_s_a.emplace(std::make_pair(s, a), good_s_a_var);
                    s_to_as[s].insert(a);
                }
                s_a_to_spp[{s, a}].insert(spps.begin(), spps.end());
            }
        }

        // Create a variable "Bad(s)" for each alive state
        std::unordered_map<unsigned, cnfvar_t, boost::hash<unsigned>> bad_s;
        if (options.allow_bad_states) {
            for (unsigned s:sample_.transitions_.all_alive()) {
                cnfvar_t bad_s_var = 0;
                bad_s_var = wr.var("Bad(" + std::to_string(s) + ")");
                bad_s.emplace(s, bad_s_var);
                varmapstream << bad_s_var << " " << s << std::endl;
            }
        }

        // From this point on, no more variables will be created. Print total count.
        if (options.verbosity>0) {
            std::cout << "A total of " << wr.nvars() << " variables were created" << std::endl;
            std::cout << "\tSelect(f): " << variables.selecteds.size() << std::endl;
            std::cout << "\tGood(s, a): " << variables.goods_s_a.size() << std::endl;
            std::cout << "\tBad(s): " << bad_s.size() << std::endl;
            std::cout << "\tV(s, d): " << vs.size() << std::endl;
        }

        // Check our variable count is correct
        assert(wr.nvars() == variables.selecteds.size() + variables.goods_s_a.size() + bad_s.size() + vs.size());

        /////// CNF constraints ///////

        // C1. For each alive state s, at least one Good(s, a) must be true,
        // or (optionally) the state must be marked as bad
        for (const auto s:sample_.transitions_.all_alive()) {
            cnfclause_t clause;

            if (options.allow_bad_states) {
                clause.push_back(Wr::lit(bad_s.at(s), true));
            }

            for (const auto a:s_to_as[s]) {
                // TODO: If (s,a) leads to unsolvable state, skip it
                // if (is_necessarily_bad(get_transition_id(s, s_a_to_sp[{s, a}]))) continue;
                clause.push_back(Wr::lit(variables.goods_s_a.at({s, a}), true));
            }
            wr.cl(clause);
            n_good_tx_clauses += 1;
        }


        // Minimize the number of Bad(s) atoms that are true
        if (options.allow_bad_states) {
            for (const auto s:sample_.transitions_.all_alive()) {
                wr.cl({Wr::lit(bad_s.at(s), false)}, 1);
                n_bad_states_clauses += 1;
            }
        }

        // C2. Good(s, a) implies V(s') < V(s), for s' in res(s, a)  \equiv
        // Good(s, a) and V(s)=k implies OR_{0<=k'<k}  V(s')=k'      \equiv
        // -Good(s, a) or -V(s, k) or OR_{0<=k'<k} V(s', k')
        for (unsigned s:sample_.transitions_.all_alive()) {
            for (unsigned a:s_to_as[s]) {
                // TODO Check if (s, a) can lead to unsolvable state. If it can, then post -Good(s, a)
                cnfvar_t good_s_a_var = variables.goods_s_a.at({s, a});

                for (unsigned spp:s_a_to_spp[{s, a}]) {
                    if (!sample_.is_solvable(spp)) continue;
//                   if (!sample_.in_sample(spp)) continue;
                    if (!sample_.is_alive(spp)) continue;

                    for (unsigned k=1; k <= max_d; ++k) {
                        cnfclause_t clause{Wr::lit(good_s_a_var, false),
                                           Wr::lit(vs.at({s, k}), false)};

                        for (unsigned kp = 1; kp<k; ++kp) {
                            clause.push_back(Wr::lit(vs.at({spp, kp}), true));
                        }
                        wr.cl(clause);
                        ++n_descending_clauses;
                    }
                }
            }
        }

        // Clauses C5-6: Good actions must be distinguishable from bad actions.
        if (options.verbosity>0) {
            std::cout << "Posting distinguishability constraints" << std::endl;
        }

        for (unsigned s:sample_.transitions_.all_alive()) {
            // TODO: Take unsolvability into account
            for (auto a:sample_.transitions_.action_ids()) {
                auto it = variables.goods_s_a.find({s, a});
                if (it == variables.goods_s_a.end()) {
                    // The action is not applicable in s, hence cannot be good.
                    continue;
                }

                cnfvar_t good_s_a_var = it->second;
                for (unsigned sp:sample_.transitions_.all_alive()) {
                    cnfclause_t clause{Wr::lit(good_s_a_var, false)};

                    auto it = variables.goods_s_a.find({sp, a});
                    if (it != variables.goods_s_a.end()) {
                        clause.push_back(Wr::lit(it->second, true));
                    }

                    for (feature_t f:compute_d1_distinguishing_features(sample_, s, sp)) {
                        clause.push_back(Wr::lit(variables.selecteds.at(f), true));
                    }

                    wr.cl(clause);
                    n_separation_clauses += 1;
                }
            }
        }

        if (options.verbosity>0) {
            std::cout << "Posting distinguishability constraints for goal states" << std::endl;
        }

        // C7: Force D1(s1, s2) to be true if exactly one of the two states is a goal state
        if (options.distinguish_goals) {
            for ( const auto s : sample_.transitions_.all_alive()) {
                for( const auto t : sample_.transitions_.all_goals()) {
                    const auto d1feats = compute_d1_distinguishing_features(sample_, s, t);
                    if (d1feats.empty()) {
                        undist_goal_warning(s, t);
                    }

                    cnfclause_t clause;
                    for (unsigned f:d1feats) {
                        clause.push_back(Wr::lit(variables.selecteds.at(f), true));
                    }

                    wr.cl(clause);
                    n_goal_clauses += 1;
                }
            }
        }

        for (unsigned f:feature_ids) {
            wr.cl({Wr::lit(variables.selecteds[f], false)}, sample_.feature_weight(f));
        }
        n_selected_clauses += feature_ids.size();

        if (options.verbosity>0) {
            // Print a breakdown of the clauses
            std::cout << "A total of " << wr.nclauses() << " clauses were created" << std::endl;
            std::cout << "\tPolicy completeness: " << n_good_tx_clauses << std::endl;
            std::cout << "\tTransition separation: " << n_separation_clauses << std::endl;
            std::cout << "\tV descending along good transitions: " << n_descending_clauses << std::endl;
            std::cout << "\tV is total function within bounds: " << n_v_function_clauses << std::endl;
            std::cout << "\tGoal separation: " << n_goal_clauses << std::endl;
            std::cout << "\t(Weighted) Bad(s): " << n_bad_states_clauses << std::endl;
            std::cout << "\t(Weighted) Select(f): " << n_selected_clauses << std::endl;
            assert(wr.nclauses() == n_selected_clauses + n_good_tx_clauses + n_descending_clauses
                                    + n_v_function_clauses + n_separation_clauses + n_bad_states_clauses
                                    + n_goal_clauses);
        }
        return {CNFGenerationOutput::Success, variables};
    }


    FixedActionPolicy D2LEncoding::generate_dnf(const std::vector<std::pair<unsigned, unsigned>>& goods, const std::vector<unsigned>& selecteds) const {
        FixedActionPolicy dnf(selecteds);
        for (const auto& [s, a]:goods) {
            FixedActionPolicy::term_t clause;

            for (const auto& f:selecteds) {
                const auto& fs = sample_.matrix().entry(s, f);
                clause.emplace_back(f, FixedActionPolicy::compute_state_value(fs));
            }

            dnf.terms.emplace(clause, a);
        }
        return dnf;
    }

    FixedActionPolicy D2LEncoding::generate_dnf_from_solution(const VariableMapping& variables, const SatSolution& solution) const {
        // Let's parse the relevant bits of the CNF solution:
        std::vector<unsigned> selecteds;
        std::vector<std::pair<unsigned, unsigned>> goods;
        for (unsigned f=0; f < variables.selecteds.size(); ++f) {
            auto varid = variables.selecteds[f];
            if (varid>0 && solution.assignment.at(varid)) selecteds.push_back(f);
        }
        for (auto const& [sa_pair, varid]:variables.goods_s_a) {
            if (varid>0 && solution.assignment.at(varid)) {
                std::cout << "Good(" << sa_pair.first << ", " << sa_pair.second << ")" << std::endl;
                goods.push_back(sa_pair);
            }
        }
        return generate_dnf(goods, selecteds);
    }

    bool D2LEncoding::are_transitions_d1d2_distinguishable(
            state_id_t s, state_id_t sp, state_id_t t, state_id_t tp, const std::vector<unsigned>& features) const {
        const auto& mat = sample_.matrix();
        for (unsigned f:features) {
            if (are_transitions_d1d2_distinguished(mat.entry(s, f), mat.entry(sp, f),
                                                   mat.entry(t, f), mat.entry(tp, f))) {
                return true;
            }
        }
        return false;
    }

} // namespaces
