
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

        for (const auto& [s, a, sps]:sample_.transitions_.nondet_transitions()) {
            bool all_sp_solvable = true;

            for (auto const& sp:sps) {
                if (!sample_.is_solvable(sp)) {
                    all_sp_solvable = false;
                }
            }

            for (auto const& sp:sps) {
                auto tx = std::make_pair((state_id_t) s, (state_id_t) sp);
                auto id = (unsigned) transition_ids_inv_.size(); // Assign a sequential ID to the transition

                transition_ids_inv_.push_back(tx);
                auto it1 = transition_ids_.emplace(tx, id);
                assert(it1.second);

                if (!all_sp_solvable) { // An alive-to-dead transition cannot be Good
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
                }
            }

//            if (!all_sp_solvable) { // An alive-to-dead transition cannot be Good
//                // do something, e.g. register "necessarily bad (s, a)"
//            }
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
        //    unsigned acyclicity_radius = 99999;
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

            // Add clauses (4), (5)
            wr.cl(within_range_clause);
            n_v_function_clauses += 1;

            for (unsigned d = 1; d <= max_d; ++d) {
                for (unsigned dpp = d+1; dpp <= max_d; ++dpp) {
                    wr.cl({Wr::lit(vs.at({s, d}), false), Wr::lit(vs.at({s, dpp}), false)});
                    n_v_function_clauses += 1;
                }
            }
        }

        // Create all variables Good_a(s, a) for any possible pair (s, a) in a non-det transition (s, a, s').
        // We use this loop to index possible non-det transitions in maps s_to_as and s_a_to_s too.
        using sa_pair_t = std::pair<unsigned, unsigned>;
        // Map `good_s_a` from transition IDs to SAT variable IDs:
        std::unordered_map<sa_pair_t, cnfvar_t, boost::hash<sa_pair_t>> good_s_a;
        for (const auto& [s, a, sps]:sample_.transitions_.nondet_transitions()) {
            if (sample_.is_alive(s)) {
                const auto it = good_s_a.find({s, a});
                cnfvar_t good_s_a_var = 0;

                if (it == good_s_a.end()) {
                    good_s_a_var = wr.var("Good_a(" + std::to_string(s) + ", " + std::to_string(a) + ")");
                    varmapstream << good_s_a_var << " " << s << " " << a << std::endl;
                    good_s_a.emplace(std::make_pair(s, a), good_s_a_var);
                }
                else {
                    good_s_a_var = it->second;
                }
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
            std::cout << "\tGood_a(s, a): " << good_s_a.size() << std::endl;
            if (options.allow_bad_states) { std::cout << "\tBad(s): " << bad_s.size() << std::endl; }
            std::cout << "\tV(s, d): " << vs.size() << std::endl;
        }

        // Check our variable count is correct
        assert(wr.nvars() == variables.selecteds.size() + good_s_a.size() + bad_s.size() + vs.size());

        /////// CNF constraints ///////

      // Good(s, s') iff Good_a(s, a)
        std::unordered_map<unsigned, cnfvar_t> tx_s_a;
        for (const auto& [s, a, sps]:sample_.transitions_.nondet_transitions()) {
            for (const auto& sp:sps) {
                auto tx = get_transition_id(s, sp);
//                if (is_necessarily_bad(get_representative_id(tx))) continue;
                tx_s_a[tx] = good_s_a[{s, a}];
                variables.goods_s_a[good_s_a[{s, a}]].insert(get_representative_id(tx));
            }
        }

        if (options.allow_bad_states) {
            // Bad(s) or OR_{a in A} Good(s, a):
            for (const auto& s:sample_.transitions_.all_alive()) {
                cnfclause_t clause;
                clause.push_back(Wr::lit(bad_s.at(s), true));

                for (const auto& a:sample_.transitions_.s_as(s)) {
                    clause.push_back(Wr::lit(good_s_a.at({s, a}), true));
                }

                // Soft clauses Bad(s):
                wr.cl({Wr::lit(bad_s.at(s), false)}, 99999);

                wr.cl(clause);
            }
        }

//    1. Good(s, a) implies V(s') < V(s),                        equiv. to (using binary variables):
//    2. Good(s, a) implies V(s')=d" and V(s)=d, for some d'<d   equiv. to (move things around):
//    3. Good(s, a) and V(s')=d'  implies OR_{d>d'}  V(s)=d      equiv. to (implication to disjunc.):
//    4. not Good(s, a) or not V(s')=d' or OR_{d>d'}  V(s)=d
        for (unsigned s:sample_.transitions_.all_alive()) {
            for (unsigned a:sample_.transitions_.s_as(s)) {
                for (unsigned sp:sample_.transitions_.nondet_successors({s, a})) {
                    if (!sample_.is_solvable(sp)) continue;
//                   if (!sample_.in_sample(spp)) continue;
//                   if (get_vstar(s) > acyclicity_radius) continue;

                    cnfvar_t good_s_a_var = good_s_a.at({s, a});

                    if (options.decreasing_transitions_must_be_good) {
                        // (3') Border condition: if s' is a goal, then (s, s') must be good
                        if (sample_.is_goal(sp)) {
                            wr.cl({Wr::lit(good_s_a_var, true)});
                            ++n_descending_clauses;
                        }
                    }

                    if (!sample_.is_alive(sp)) continue;

                    for (unsigned dp=1; dp < max_d; ++dp) {

                        cnfclause_t clause;
                        // (2) Good(s, a) and V(s", d") -> V(s) > d"
                        clause.push_back(Wr::lit(good_s_a_var, false));
                        clause.push_back(Wr::lit(vs.at({sp, dp}), false));

                        if (options.allow_cycles) {
                            // (2) Good(s, a) and V(s', d') -> V(s) = d'
                            clause.push_back(Wr::lit(vs.at({s, dp}), true));

//                            // (3') Soft clause Good(s, a) and V(s', d') -> V(s) = d'
                            wr.cl({Wr::lit(good_s_a_var , false),
                                   Wr::lit(vs.at({sp, dp}), false),
                                   Wr::lit(vs.at({s, dp}), true)}, 99999);
                            ++n_descending_clauses;
                        }

                        for (unsigned d = dp + 1; d <= max_d; ++d) {
                            clause.push_back(Wr::lit(vs.at({s, d}),true));

                            if (options.decreasing_transitions_must_be_good) {
                                // (3) V(s') < V(s) -> Good(s, a)
                                wr.cl({Wr::lit(vs.at({s, d}), false),
                                       Wr::lit(vs.at({sp, dp}), false),
                                       Wr::lit(good_s_a_var, true)});
                                ++n_descending_clauses;
                            }

                        }
                        wr.cl(clause);
                        ++n_descending_clauses;
                    }

//               (2') Border condition: V(s', D) implies -Good(s, a)
                    wr.cl({Wr::lit(vs.at({sp, max_d}), false),
                           Wr::lit(good_s_a_var, false)});
                    ++n_descending_clauses;
                }
            }
        }

        // Clauses (6), (7):
        auto transitions_to_distinguish = distinguish_all_transitions();
        if (options.verbosity>0) {
            std::cout << "Posting distinguishability constraints for " << transitions_to_distinguish.size()
                      << " pairs of transitions" << std::endl;
        }
        for (const auto& tpair:transitions_to_distinguish) {
            assert (!is_necessarily_bad(tpair.tx1));
            const auto& [s, sp] = get_state_pair(tpair.tx1);
            const auto& [t, tp] = get_state_pair(tpair.tx2);

            cnfclause_t clause{Wr::lit(tx_s_a[tpair.tx1], false)};

            // Compute first the Selected(f) terms
            for (feature_t f:compute_d1d2_distinguishing_features(feature_ids, sample_, s, sp, t, tp)) {
                clause.push_back(Wr::lit(variables.selecteds.at(f), true));
            }

            if (!is_necessarily_bad(tpair.tx2)) {
                auto good_t_a = tx_s_a[tpair.tx2];
                clause.push_back(Wr::lit(good_t_a, true));
            }
            wr.cl(clause);
            n_separation_clauses += 1;
        }

        // (8): Force D1(s1, s2) to be true if exactly one of the two states is a goal state
        if (options.distinguish_goals) {
            if (options.verbosity>0) {
                std::cout << "Posting distinguishability constraints for goal states" << std::endl;
            }
            for (unsigned g:sample_.transitions_.all_goal()) {
                for (unsigned s:sample_.transitions_.all_alive()) {
                    for (unsigned a:sample_.transitions_.s_as(s)) {
                        for (unsigned t:sample_.transitions_.nondet_successors({s, a})) {
                            if (!sample_.is_goal(t)) {
                                const auto d1feats = compute_d1_distinguishing_features(sample_, g, t);
                                if (d1feats.empty()) {
                                    undist_goal_warning(g, t);
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
                }
            }
        }

        if (!options.validate_features.empty()) {
            // If we only want to validate a set of features, we just force the Selected(f) to be true for them,
            // plus we don't really need any soft constraints.
//        std::cout << "Enforcing " << feature_ids.size() << " feature selections and ignoring soft constraints" << std::endl;
            for (unsigned f:feature_ids) {
                wr.cl({Wr::lit(variables.selecteds[f], true)});
            }
        } else {
//        std::cout << "Posting (weighted) soft constraints for " << variables.selecteds.size() << " features" << std::endl;
            for (unsigned f:feature_ids) {
                wr.cl({Wr::lit(variables.selecteds[f], false)}, sample_.feature_weight(f));
            }
        }

        n_selected_clauses += feature_ids.size();

        if (options.verbosity>0) {
            // Print a breakdown of the clauses
            std::cout << "A total of " << wr.nclauses() << " clauses were created" << std::endl;
            std::cout << "\tPolicy completeness [1]: " << n_good_tx_clauses << std::endl;
            std::cout << "\tTransition separation [5,6]: " << n_separation_clauses << std::endl;
            std::cout << "\tV descending along good transitions [X]: " << n_descending_clauses << std::endl;
            std::cout << "\tV is total function within bounds [X]: " << n_v_function_clauses << std::endl;
            std::cout << "\tGoal separation [X]: " << n_goal_clauses << std::endl;
            std::cout << "\t(Weighted) Select(f): " << n_selected_clauses << std::endl;
            assert(wr.nclauses() == n_selected_clauses + n_good_tx_clauses + n_descending_clauses
                                    + n_v_function_clauses + n_separation_clauses
                                    + n_goal_clauses + n_reachability_clauses);
        }
        return {CNFGenerationOutput::Success, variables};
    }


    std::vector<transition_pair> D2LEncoding::distinguish_all_transitions() const {
        std::vector<transition_pair> transitions_to_distinguish;
        transitions_to_distinguish.reserve(class_representatives_.size() * class_representatives_.size());
        for (const auto tx1:class_representatives_) {
            if (is_necessarily_bad(tx1)) continue;
            for (const auto tx2:class_representatives_) {
                if (tx1 != tx2) {
                    transitions_to_distinguish.emplace_back(tx1, tx2);
                }
            }
        }
        return transitions_to_distinguish;
    }

    DNFPolicy D2LEncoding::generate_dnf(const std::vector<std::pair<unsigned, unsigned>>& goods, const std::vector<unsigned>& selecteds) const {
        DNFPolicy dnf(selecteds);
        for (const auto& [s, sp]:goods) {
            DNFPolicy::term_t clause;

            for (const auto& f:selecteds) {
                const auto& fs = sample_.matrix().entry(s, f);
                const auto& fsprime = sample_.matrix().entry(sp, f);

                clause.emplace_back(f, DNFPolicy::compute_state_value(fs));
                clause.emplace_back(f, DNFPolicy::compute_transition_value(fs, fsprime));
            }

            dnf.terms.insert(clause);
        }
        return dnf;
    }

    DNFPolicy D2LEncoding::generate_dnf(const std::vector<unsigned>& goods, const std::vector<unsigned>& selecteds) const {
        std::vector<std::pair<unsigned, unsigned>> pairs;
        pairs.reserve(goods.size());
        for (const auto& tx:goods) {
            pairs.push_back(get_state_pair(tx));
        }
        return generate_dnf(pairs, selecteds);
    }

    DNFPolicy D2LEncoding::generate_dnf_from_solution(const VariableMapping& variables, const SatSolution& solution) const {
        // Let's parse the relevant bits of the CNF solution:
        std::vector<unsigned> selecteds, goods;
        for (unsigned f=0; f < variables.selecteds.size(); ++f) {
            auto varid = variables.selecteds[f];
            if (varid>0 && solution.assignment.at(varid)) selecteds.push_back(f);
        }
        for (auto const& [varid, txids]:variables.goods_s_a) {
            if (varid>0 && solution.assignment.at(varid)) {
                for (unsigned txid:txids) {
                    goods.push_back(txid);
                }
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
