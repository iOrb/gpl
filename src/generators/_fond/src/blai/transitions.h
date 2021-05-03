
#pragma once

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
        const std::size_t num_transitions_;

        //! nondet_transitions_ represents the entire non-deterministic transition function by storing a vector of
        //! possible tuples (s, a, S').
//        std::set<std::tuple<unsigned, unsigned, unsigned>> nondet_transitions_;

        // Operations
        std::map<unsigned, std::unordered_set<unsigned>> s_as_; // {s: {a1, a2, ...}}
        std::set<action_id_t> action_ids_;

        //! trdata_[s] contains the IDs of all neighbors of s in the state space
        std::vector<std::vector<unsigned>> trdata_;
        std::map<std::pair<unsigned, unsigned>, std::set<unsigned>> trdata_s_a_;

        std::set<unsigned> alive_states_;
        std::set<unsigned> goal_states_;
        std::set<unsigned> unsolvable_states_;
        std::set<unsigned> unknown_states_;

        std::vector<int> vstar_;

    public:
        TransitionSample(std::size_t num_states, std::size_t num_transitions)
                : num_states_(num_states),
                  num_transitions_(num_transitions),
                  trdata_(num_states),
                  alive_states_(),
                  goal_states_(),
                  vstar_(num_states)
        {
            if (num_states_ > std::numeric_limits<state_id_t>::max()) {
                throw std::runtime_error("Number of states too high - revise source code and change state_id_t datatype");
            }

            if (num_transitions_ > std::numeric_limits<transition_id_t>::max()) {
                throw std::runtime_error("Number of states too high - revise source code and change transition_id_t datatype");
            }
        }

        ~TransitionSample() = default;
        TransitionSample(const TransitionSample&) = default;
        TransitionSample(TransitionSample&&) = default;

        std::size_t num_states() const { return num_states_; }
        std::size_t num_transitions() const { return num_transitions_; }

        int vstar(unsigned sid) const {
            auto vstar = vstar_.at(sid);
            return vstar;
//        return vstar < 0 ? -1 : vstar;
        }

        const std::vector<unsigned>& successors(unsigned s) const {
            return trdata_.at(s);
        }

        const std::set<unsigned>& successors(std::pair<unsigned, unsigned> sa) const {
            return trdata_s_a_.at(sa);
        }

        const std::unordered_set<unsigned>& s_as(unsigned s) const {
            return s_as_.at(s);
        }

        bool is_alive(unsigned state) const { return alive_states_.find(state) != alive_states_.end(); }
        bool is_goal(unsigned state) const { return goal_states_.find(state) != goal_states_.end(); }
        bool is_unsolvable(unsigned state) const { return unsolvable_states_.find(state) != unsolvable_states_.end(); }
        bool is_unknown(unsigned state) const { return unknown_states_.find(state) != unknown_states_.end() ; }

        unsigned num_unsolvable() const {
            unsigned c = 0;
            for (unsigned s=0; s < num_states_; ++s) {
                if (is_unsolvable(s)) c += 1;
            }
            return c;
        }

        const std::vector<unsigned>& all_alive() const {
            std::vector<unsigned> v;
            v.reserve(alive_states_.size());
            for (auto const& s:alive_states_) {
                v.push_back(s);
            }
            return v;
        }

        const std::vector<unsigned>& all_goals() const {
            std::vector<unsigned> v;
            v.reserve(goal_states_.size());
            for (auto const& s:goal_states_) {
                v.push_back(s);
            }
            return v;
        }

        //! Print a representation of the object to the given stream.
        friend std::ostream& operator<<(std::ostream &os, const TransitionSample& o) { return o.print(os); }
        std::ostream& print(std::ostream &os) const {
            os << "Transition sample [states: " << num_states_
               << ", transitions: " << num_transitions_ << std::endl;
            return os;
        }

        // readers
        void read(std::istream &is) {
            for (unsigned i = 0; i < num_states_; ++i) {
                unsigned s = 0, n_a = 0, n_sp = 0, a = 0, sp = 0;
                int vstar = 0;
                is >> s >> vstar >> n_a >> n_sp;

                // Store the value of V^*(s) for each state s
                if (vstar > 0) {
                    alive_states_.insert(s);
                } else if (vstar == 0) {
                    goal_states_.insert(s);
                } else if (vstar == -1) {
                    unsolvable_states_.insert(s);
                } else if (vstar == -2) {
                    unknown_states_.insert(s);
                } else {
                    assert (vstar < -1);
                    // No need to do anything, we don't know whether the state is unsolvable or not
                }
                vstar_[s] = vstar;

                if (n_sp > 0) {
                    std::set<unsigned> tmp_sps;
                    for (unsigned j = 0; j < n_sp; ++j) {
                        is >> a >> sp;
                        s_as_[s].insert(a);
                        action_ids_.insert(a);
                        trdata_s_a_[{s, a}].insert(sp);
                        tmp_sps.insert(sp);
                    }
                    std::vector<unsigned> all_sps{tmp_sps.begin(), tmp_sps.end()};
                    trdata_[s] = all_sps;

                    assert(trdata_[s].empty());
                }
            }
        }


        static TransitionSample read_dump(std::istream &is, bool verbose) {
            unsigned num_states = 0, num_transitions = 0;
            is >> num_states >> num_transitions;
            TransitionSample transitions(num_states, num_transitions);
            transitions.read(is);
            if( verbose ) {
                std::cout << "TransitionSample::read_dump: #states=" << transitions.num_states()
                          << ", #transitions=" << transitions.num_transitions()
                          << std::endl;
            }
            return transitions;
        }
    };

} // namespaces