
#include "d2l.h"
#include "types.h"

#include <iostream>
#include <vector>
#include <unordered_map>

#include <boost/functional/hash.hpp>
#include <common/helpers.h>


namespace sltp::cnf {


    transition_denotation
    compute_transition_denotation(FeatureMatrix::feature_value_t s_f, FeatureMatrix::feature_value_t sprime_f) {
        int type_s = (int) sprime_f - (int) s_f; // <0 if DEC, =0 if unaffected, >0 if INC
        int sign = (type_s > 0) ? 1 : ((type_s < 0) ? -1 : 0); // Get the sign
        return transition_denotation(bool(s_f > 0), sign);
    }


    void D2LEncoding::compute_equivalence_relations() {
        // A mapping from a full transition trace to the ID of the corresponding equivalence class
        std::unordered_map<transition_trace, unsigned> from_trace_to_class_repr;

        for (const auto &s:sample_.expanded_states()) {
            for (const auto&[a, sp]:sample_.successors_a_sp(s)) {
                auto tx = std::make_pair((state_id_t) s, (state_id_t) sp);
                auto id = (unsigned) transition_ids_inv_.size();

                transition_ids_inv_.push_back(tx);
                auto it1 = transition_ids_.emplace(tx, id);
                assert(it1.second);

                bool all_possible_adv_states_are_solvable = true;
                bool all_possible_adv_states_are_goal = true;
                for (const auto &spp:sample_.adv(sp)) {
//                    if (!sample_.is_unknown(spp)) continue;
                    if (!sample_.is_solvable(spp)) { // An alive-to-dead transition cannot be Good
                        all_possible_adv_states_are_solvable = false;
                    }
                    if (!sample_.is_goal(spp)) { // An alive-to-dead transition cannot be Good
                        all_possible_adv_states_are_goal = false;
                    }
                }

                if (!sample_.is_solvable(sp)) { // An alive-to-dead transition cannot be Good
                    necessarily_bad_transitions_.insert(id);
                }

                if (!all_possible_adv_states_are_solvable)
                    necessarily_bad_sa_.insert({s, a, sp});
                if (all_possible_adv_states_are_goal)
                    necessarily_good_sa_.insert({s, a, sp});

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
        }


        // All transitions that belong to some class where at least one transition must be bad, must be bad
        std::unordered_set<unsigned> necessarily_bad_classes;
        for (const auto id:necessarily_bad_transitions_) {
            necessarily_bad_classes.insert(get_representative_id(id));
        }

        for (unsigned id = 0; id < transition_ids_.size(); ++id) {
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
        for (unsigned tx = 0; tx < transition_ids_.size(); ++tx) {
            auto repr = get_representative_id(tx);
            classes[repr].push_back(get_state_pair(tx));
        }

        unsigned i = 0;
        for (const auto &elem:classes) {
            std::cout << "Class " << ++i << ": " << std::endl;
            const auto &elements = elem.second;
            for (unsigned j = 0; j < elements.size(); ++j) {
                const auto &tx = elements[j];
                std::cout << "(" << tx.first << ", " << tx.second << ")";
                if (j < elements.size() - 1) std::cout << "; ";
            }
            std::cout << std::endl << std::endl;
        }
    }


    std::pair<cnf::CNFGenerationOutput, VariableMapping> D2LEncoding::generate(CNFWriter &wr) {
        using Wr = CNFWriter;
        const auto &mat = sample_.matrix();
        const auto num_transitions = transition_ids_.size();

        VariableMapping variables(nf_);

        auto varmapstream = utils::get_ofstream(options.workspace + "/varmap.wsat");

        // Keep a map from pairs (s, d) to SAT variable ID of the variable V(s, d)
        std::unordered_map<std::pair<unsigned, unsigned>, cnfvar_t, boost::hash<state_pair>> vs;

        // Map from state and card. const. var pairs (s,y) to SAT variable ID of the variable CardConstraint(s,y)
        std::unordered_map<std::pair<unsigned, unsigned>, cnfvar_t, boost::hash<state_pair> > card_constraint_vars;

        unsigned n_descending_clauses = 0;
        unsigned n_v_function_clauses = 0;
        unsigned n_good_tx_clauses = 0;
        unsigned n_selected_clauses = 0;
        unsigned n_separation_clauses = 0;
        unsigned n_goal_clauses = 0;

        if (options.verbosity > 0) {
            std::cout << "Generating CNF encoding for " << sample_.alive_states().size() << " alive states, "
                      << transition_ids_.size() << " alive-to-solvable and alive-to-dead transitions and "
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
        for (const auto s:sample_.alive_states()) {
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
                for (unsigned dprime = d + 1; dprime <= max_d; ++dprime) {
                    wr.cl({Wr::lit(vs.at({s, d}), false), Wr::lit(vs.at({s, dprime}), false)});
                    n_v_function_clauses += 1;
                }
            }
        }

        // Create all variables Good(s, a, s') for any possible pair (s, a, s') in a non-det transition (s, a, s').
        // We use this loop to index possible non-det transitions in maps s_to_as and s_a_to_s too.
        // Map `good_s_a` from transition IDs to SAT variable IDs:
        for (const auto &s:sample_.expanded_states()) {
            for (const auto&[a, sp]:sample_.successors_a_sp(s)) {
                const auto it = variables.goods_s_a_sp.find({s, a, sp});
                cnfvar_t good_s_a_sp_var = 0;
                if (it == variables.goods_s_a_sp.end()) {
                    good_s_a_sp_var = wr.var(
                            "Good(" + std::to_string(s) + ", " + std::to_string(a) + ", " + std::to_string(sp) + ")");
                    varmapstream << good_s_a_sp_var << " " << s << " " << a << " " << sp << std::endl;
                    variables.goods_s_a_sp.emplace((tx_triple) {s, a, sp}, good_s_a_sp_var);
                } else {
                    good_s_a_sp_var = it->second;
                }
            }
        }

        // Create a variable "Bad(s)" for each alive state
        if (options.allow_bad_states) {
            for (unsigned s:sample_.expanded_states()) {
                cnfvar_t bad_s_var = 0;
                bad_s_var = wr.var("Bad(" + std::to_string(s) + ")");
                variables.bad_s.emplace(s, bad_s_var);
                varmapstream << bad_s_var << " " << s << std::endl;
            }
        }

        // From this point on, no more variables will be created. Print total count.
        if (options.verbosity > 0) {
            std::cout << "A total of " << wr.nvars() << " variables were created" << std::endl;
            std::cout << "\tSelect(f): " << variables.selecteds.size() << std::endl;
            std::cout << "\tGood(s, a, s'): " << variables.goods_s_a_sp.size() << std::endl;
            std::cout << "\tBad(s): " << variables.bad_s.size() << std::endl;
            std::cout << "\tV(s, d): " << vs.size() << std::endl;
        }

        /////// CNF constraints ///////

        // C1. For each alive state s, at least one Good(s, a, s') must be true,
        // or (optionally) the state must be marked as bad
        for (const auto &s:sample_.expanded_states()) {
            cnfclause_t clause;

            if (options.allow_bad_states) {
                // Bad(s) or OR_{a in A} Good(s, a, s'):
                clause.push_back(Wr::lit(variables.bad_s.at(s), true));
                // Soft clauses Bad(s). Minimize the number of Bad(s) atoms that are true.
                wr.cl({Wr::lit(variables.bad_s.at(s), false)}, 1);
            }

            for (const auto&[a, sp]:sample_.successors_a_sp(s)) {
                tx_triple tx = std::make_tuple(s, a, sp);
                cnfvar_t good_s_a_sp_var = variables.goods_s_a_sp.at(tx);
                if (is_necessarily_bad(get_class_representative(s, sp))) {
                    wr.cl({Wr::lit(good_s_a_sp_var, false)});
                    continue;
                }
                // TODO: take adv resposes into account, special cases like: all_goals or some_dead
                if (is_necessarily_bad_tx(tx)) {
                    wr.cl({Wr::lit(good_s_a_sp_var, false)});
                    continue;
                }
//                if (is_necessarily_good_tx(tx))
//                    wr.cl({Wr::lit(good_s_a_sp_var, true)});
                clause.push_back(Wr::lit(good_s_a_sp_var, true));
//                wr.cl({Wr::lit(good_s_a_sp_var, true)}, 1);
            }

            wr.cl(clause);
        }

        // C2. Good(s, a, s') implies V(s') < V(s), for s' in res(s, a)  \equiv
        // Good(s, a, s') and V(s)=k implies OR_{0<=k'<k}  V(s')=k'      \equiv
        // -Good(s, a, s') or -V(s, k) or OR_{0<=k'<k} V(s', k')
        for (const auto &s:sample_.expanded_states()) {
            for (const auto &[a, sp]:sample_.successors_a_sp(s)) {
                tx_triple tx = std::make_tuple(s, a, sp);
                cnfvar_t good_var = variables.goods_s_a_sp.at(tx);
                if (!sample_.in_sample(sp)) continue; // maybe we do not car about this?
                if (options.use_weighted_tx and sample_.is_goal(sp))
                    wr.cl({Wr::lit(good_var, true)}, 1);
                if (!sample_.is_alive(sp)) continue;
                if (is_necessarily_bad(get_class_representative(s, sp))) continue;
                if (is_necessarily_bad_tx(tx)) continue;
//                    if (sample_.is_unknown(sp)) continue; // (?)
                for (const auto &spp:sample_.adv(sp)) {
                    if (!sample_.in_sample(spp)) continue; // maybe we do not car about this?
                    if (!sample_.is_alive(spp)) continue;
                    // TODO: take adv resposes into account, special cases like: all_goals or some_dead.
                    //  if possibly usolvable skip?
                    // TODO: check if this formula is doing what we want, that is Good(s, a, s') -> V(s'') < V(s)
                    for (unsigned k = 1; k < max_d; ++k) {
                        // Minimize Good(s, a, s') and V(s', d') -> V(s) < d'
                        cnfclause_t clause_s_a{Wr::lit(good_var, false),
                                               Wr::lit(vs.at({s, k}), false)};
                        for (unsigned kpp = 1; kpp <= k; ++kpp) {
                            if (!options.allow_cycles and k == kpp) continue;
                            clause_s_a.push_back(Wr::lit(vs.at({spp, kpp}), true));
                        }
                        wr.cl(clause_s_a);
                        ++n_descending_clauses;
                    }
                }
            }
        }

        if (options.validate_features.empty()) {
            // Clauses (6), (7):
            if (options.verbosity > 0) {
                std::cout << "Posting distinguishability constraints" << std::endl;
            }
            for (const auto &s:sample_.expanded_states()) {
                for (const auto &[a, sp]:sample_.successors_a_sp(s)) {
                    tx_triple tx = std::make_tuple(s, a, sp);
                    if (is_necessarily_bad(get_class_representative(s, sp))) continue;
                    if (is_necessarily_bad_tx(tx)) continue;
                    cnfvar_t good_var = variables.goods_s_a_sp.at(tx);
                    for (const auto &t:sample_.expanded_states()) {
                        for (const auto &[b, tp]:sample_.successors_a_sp(t)) {
                            if (options.use_action_ids and a != b)
                                continue; // TODO: continue or just don't add txp to the clause?
                            tx_triple txp = std::make_tuple(t, b, tp);
                            cnfvar_t good_var_p = variables.goods_s_a_sp.at(txp);
                            cnfclause_t clause{Wr::lit(good_var, false)};
                            // Compute first the Selected(f) terms
                            for (feature_t f:compute_d1d2_distinguishing_features(feature_ids, sample_, s, sp, t, tp)) {
                                clause.push_back(Wr::lit(variables.selecteds.at(f), true));
                            }
                            if (!is_necessarily_bad(get_class_representative(t, tp))) {
//                        if (!is_necessarily_bad_tx(txp)) {
                                clause.push_back(Wr::lit(good_var_p, true));
                            }
                            wr.cl(clause);
                            n_separation_clauses += 1;
                        }
                    }
                }
            }
        }

        // good(s, a, s') -> -bad(s')
        if (options.allow_bad_states and options.use_weighted_tx) {
            for (const auto &s:sample_.expanded_states()) {
                for (const auto &[a, sp]:sample_.successors_a_sp(s)) {
                    tx_triple tx = std::make_tuple(s, a, sp);
                    if (is_necessarily_bad(get_class_representative(s, sp))) continue;
                    if (is_necessarily_bad_tx(tx)) continue;
                    auto it = variables.bad_s.find(sp);
                    if (it == variables.bad_s.end()) continue;

                    cnfclause_t clause{Wr::lit(variables.bad_s.at(sp), true),
                                       Wr::lit(variables.goods_s_a_sp.at(tx), false)};

                    wr.cl(clause);
                    n_separation_clauses += 1;
                }
            }
        }

        // Distinguish Bad(s) from -Bad(s)
        // Clauses C5-6: Good actions must be distinguishable from bad actions.
//        if (options.allow_bad_states) {
//            if (options.verbosity > 0) {
//                std::cout << "Posting distinguishability constraints" << std::endl;
//            }
//            for (unsigned s:sample_.expanded_states()) {
//                cnfvar_t bad_s_var = variables.bad_s.at(s);
//                for (unsigned t:sample_.expanded_states()) {
//                    cnfvar_t bad_t_var = variables.bad_s.at(t);
//                    cnfclause_t clause{Wr::lit(bad_s_var, false),
//                                       Wr::lit(bad_t_var, true)};
//
//                    for (feature_t f:compute_d1_distinguishing_features(sample_, s, t)) {
//                        clause.push_back(Wr::lit(variables.selecteds.at(f), true));
//                    }
//
//                    wr.cl(clause);
//                    n_separation_clauses += 1;
//                }
//            }
//        }

        // (8): Force D1(s1, s2) to be true if exactly one of the two states is a goal state
        if (options.distinguish_goals) {
            for (const auto &s:sample_.full_training_set().all_alive()) {
                for (const auto &t: sample_.full_training_set().all_goals()) {
                    const auto d1feats = compute_d1_distinguishing_features(sample_, s, t);
                    if (d1feats.empty())
                        undist_goal_warning(s, t);
                    cnfclause_t clause;
                    for (unsigned f:d1feats) {
                        clause.push_back(Wr::lit(variables.selecteds.at(f), true));
                    }
                    wr.cl(clause);
                    n_goal_clauses += 1;
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

        if (options.verbosity > 0) {
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


    DNFPolicy
    D2LEncoding::generate_dnf(const std::vector<tx_triple> &goods, const std::vector<unsigned> &selecteds) const {
        DNFPolicy dnf(selecteds);
        for (const auto &tx:goods) {
            DNFPolicy::term_t clause;

            for (const auto &f:selecteds) {
                const auto &fs = sample_.matrix().entry(get_s(tx), f);
                const auto &fsprime = sample_.matrix().entry(get_sp(tx), f);

                clause.emplace_back(f, DNFPolicy::compute_state_value(fs));
                clause.emplace_back(f, DNFPolicy::compute_transition_value(fs, fsprime));
            }

            dnf.terms.insert({clause, get_a(tx)});
        }
        return dnf;
    }


    DNFPolicy
    D2LEncoding::generate_dnf_from_solution(const VariableMapping &variables, const SatSolution &solution) const {
        // Let's parse the relevant bits of the CNF solution:
        std::vector<unsigned> selecteds;
        std::vector<std::tuple<unsigned, unsigned, unsigned>> goods;
        for (unsigned f = 0; f < variables.selecteds.size(); ++f) {
            auto varid = variables.selecteds[f];
            if (varid > 0 && solution.assignment.at(varid)) selecteds.push_back(f);
        }
        unsigned n_good_s_a_sp = 0;
        for (const auto&[s_a_sp, varid]:variables.goods_s_a_sp) {
            if (varid > 0 && solution.assignment.at(varid)) {
                if (options.verbosity > 1) {
                    if (n_good_s_a_sp % 10 == 0) {
                        std::cout << std::endl;
                    }
                    std::cout << "Good(" << get_s(s_a_sp) << ", " << get_a(s_a_sp) << ", " << get_sp(s_a_sp) << ") ";
                }
                goods.push_back(s_a_sp);
                ++n_good_s_a_sp;
            }
        }
        if (options.verbosity) {
            post_variables_selected(variables, solution);
        }
        return generate_dnf(goods, selecteds);
    }

    void D2LEncoding::post_variables_selected(const VariableMapping &variables, const SatSolution &solution) const {
        std::vector<unsigned> selecteds;
        unsigned n_selecteds = 0;
        std::vector<std::tuple<unsigned, unsigned, unsigned>> goods;
        for (unsigned f = 0; f < variables.selecteds.size(); ++f) {
            auto varid = variables.selecteds[f];
            if (varid > 0 && solution.assignment.at(varid)) ++n_selecteds;
        }
        unsigned n_good_s_a_sp = 0;
        for (const auto&[s_a_sp, varid]:variables.goods_s_a_sp) {
            if (varid > 0 && solution.assignment.at(varid)) {
                if (options.verbosity > 1) {
                    if (n_good_s_a_sp % 10 == 0) {
                        std::cout << std::endl;
                    }
                    std::cout << "Good(" << get_s(s_a_sp) << ", " << get_a(s_a_sp) << ", " << get_sp(s_a_sp) << ") ";
                }
                ++n_good_s_a_sp;
            }
        }
        unsigned n_bad_s = 0;
        for (const auto&[s, varid]:variables.bad_s) {
            if (varid > 0 && solution.assignment.at(varid)) {
                if (options.verbosity > 1) {
                    if (n_good_s_a_sp % 10 == 0) {
                        std::cout << std::endl;
                    }
                    std::cout << "Bad(" << s << ") ";
                }
                ++n_bad_s;
            }
        }
        double psasp, pbs, psel;

        psasp = (variables.goods_s_a_sp.size() == 0) ? 0 : ((double) n_good_s_a_sp /
                                                            (double) variables.goods_s_a_sp.size() * 100);
        pbs = (variables.bad_s.size() == 0) ? 0 : ((double) n_bad_s / (double) variables.bad_s.size() * 100);
        psel = (variables.selecteds.size() == 0) ? 0 : ((double) n_selecteds / (double) variables.selecteds.size() *
                                                        100);
        std::cout << std::endl << "Num Good(s, a, s') selected: " << n_good_s_a_sp << " (" << psasp << "%)"
                  << std::endl;
        std::cout << "Num Bad(s) selected: " << n_bad_s << " (" << pbs << "%)" << std::endl;
        std::cout << "Num selected features: " << n_selecteds << " (" << psel << "%)" << std::endl;
    }

    bool D2LEncoding::are_transitions_d1d2_distinguishable(
            state_id_t s, state_id_t sprime, state_id_t t, state_id_t tprime,
            const std::vector<unsigned> &features) const {
        const auto &mat = sample_.matrix();
        for (unsigned f:features) {
            if (are_transitions_d1d2_distinguished(mat.entry(s, f), mat.entry(sprime, f),
                                                   mat.entry(t, f), mat.entry(tprime, f))) {
                return true;
            }
        }
        return false;
    }

} // namespaces