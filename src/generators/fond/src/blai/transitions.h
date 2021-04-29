
#pragma once

#include "map"
#include <cassert>
#include <iostream>
#include <fstream>
#include <random>
#include <string>
#include <unordered_set>
#include <vector>

#include <common/base.h>


namespace sltp {

    class TransitionSample {
    protected:
        const std::size_t num_states_;
        const std::size_t num_nondet_transitions_;

        //! nondet_transitions_ represents the entire non-deterministic transition function by storing a vector of
        //! possible tuples (s, a, S').
        std::set<std::tuple<unsigned, unsigned, std::set<unsigned>>> nondet_transitions_;

        // Operations
        std::map<unsigned, std::unordered_set<unsigned>> s_as_; // {s: {a1, a2, ...}}

        //! trdata_[s] contains a vector with all state IDs of the states s' that can be reached in the state space
        //! in one single step from s
        std::map<unsigned, std::unordered_set<unsigned>> trdata_s; // {s: {s1', s2', ...}}
        std::map<sa_pair, std::unordered_set<unsigned>> trdata_s_a; // {(s, a): {s1', s2', ...}}

        std::set<action_id_t> action_ids_;

        std::set<unsigned> alive_states_;
        std::set<unsigned> goal_states_;
        std::set<unsigned> unsolvable_states_;

        std::unordered_map<unsigned, int> vstar_;

    public:
        TransitionSample(std::size_t num_states, std::size_t num_nondet_transitions)
                : num_states_(num_states),
                  num_nondet_transitions_(num_nondet_transitions)
        {
            if (num_states_ > std::numeric_limits<state_id_t>::max()) {
                throw std::runtime_error("Number of states too high - revise source code and change state_id_t datatype");
            }

            if (num_nondet_transitions_ > std::numeric_limits<transition_id_t>::max()) {
                throw std::runtime_error("Number of states too high - revise source code and change transition_id_t datatype");
            }
        }

        ~TransitionSample() = default;
        TransitionSample(const TransitionSample&) = default;
        TransitionSample(TransitionSample&&) = default;

        std::size_t num_states() const { return num_states_;}
        std::size_t num_nondet_transitions() const { return num_nondet_transitions_; }

        const std::set<std::tuple<unsigned, unsigned, std::set<unsigned>>>& nondet_transitions() const {
            return nondet_transitions_;
        }

        int vstar(unsigned sid) const {
            return vstar_.at(sid);
        }

        const std::unordered_set<unsigned>& nondet_successors(unsigned s) const {
            return trdata_s.at(s);
        }

        const std::unordered_set<unsigned>& nondet_successors(sa_pair sa) const {
            return trdata_s_a.at(sa);
        }

        const std::unordered_set<unsigned>& s_as(unsigned s) const {
            return s_as_.at(s);
        }

        bool is_alive(unsigned state) const { return alive_states_.find(state) != alive_states_.end(); }
        bool is_goal(unsigned state) const { return goal_states_.find(state) != goal_states_.end(); }
        bool is_unsolvable(unsigned state) const { return unsolvable_states_.find(state) != unsolvable_states_.end(); }

        const std::set<action_id_t>& action_ids() const { return action_ids_; };

        unsigned num_unsolvable() const {
            return unsolvable_states_.size();
        }

        const std::set<unsigned>& all_alive() const { return alive_states_; }
        const std::set<unsigned>& all_goal() const { return goal_states_; }
        const std::set<unsigned>& all_dead() const { return unsolvable_states_; }

        //! Print a representation of the object to the given stream.
        friend std::ostream& operator<<(std::ostream &os, const TransitionSample& o) { return o.print(os); }
        std::ostream& print(std::ostream &os) const {
            os << "Transition sample [#states=" << num_states_
               << ", #transitions=" << num_nondet_transitions_
               << std::endl;
            return os;
        }

        // readers
        void read(std::istream &is) {

            // read number of states that have been expanded, for which we'll have one state per line next
            unsigned n_read_transitions = 0;

            // read transitions, in format: s_id, vstar, num_ops, num_spp, (op0, sp0), (op0, sp1)...
            for (unsigned i = 0; i < num_states_; ++i) {
                unsigned s = 0, n_a = 0, n_sp = 0, op = 0, sp = 0;
                int vstar = 0;
                is >> s >> vstar >> n_a >> n_sp;
//                assert(i==src);
//                assert(src < num_states_ && 0 <= count);

                // Store the value of V^*(s) for each state s
                if (vstar>0) {
                    alive_states_.insert(s);
                } else if (vstar == 0) {
                    goal_states_.insert(s);
                } else if (vstar < 0) {
                    unsolvable_states_.insert(s);
                }
                vstar_[s] = vstar;

                if (n_sp > 0) {
//                    std::vector<bool> seen(num_states_s_spp_ + num_states_sp_, false);
                    std::map<unsigned,std::set<unsigned>> tmp_a_sps;

                    for (unsigned j = 0; j < n_sp; ++j) {
                        is >> op >> sp;
//                        assert(spp < num_states_);
                        trdata_s[s].insert(sp);
                        trdata_s_a[{s, op}].insert(sp);
                        s_as_[s].insert(op);
                        action_ids_.insert(op);
                        tmp_a_sps[op].insert(sp);
                        n_read_transitions++;
                    }

                    for (auto const& [op, sps]:tmp_a_sps) {
                        nondet_transitions_.insert(std::make_tuple(s, op, sps));
                    }

                    assert(trdata_[s].empty());

                }
            }

            assert(n_read_transitions==num_nondet_transitions);

            std::cout << "Read " << alive_states_.size() << " alive states" << std::endl;

        }

        static TransitionSample read_dump(std::istream &is, bool verbose) {
            unsigned num_states = 0, num_nondet_transitions = 0;
            is >> num_states >> num_nondet_transitions;
            TransitionSample transitions(num_states, num_nondet_transitions);
            transitions.read(is);
            if( verbose ) {
                std::cout << "TransitionSample::read_dump:#states=" << transitions.num_states()
                          << ", #states="<< transitions.num_states()
                          << ", #transitions=" << transitions.num_nondet_transitions()
                          << std::endl;
            }
            return transitions;
        }
    };

} // namespaces
