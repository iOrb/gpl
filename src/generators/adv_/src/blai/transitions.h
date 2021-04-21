
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
        const std::size_t num_states_s_spp_;
        const std::size_t num_nondet_transitions_;
        const std::size_t num_agent_transitions_;

        //! nondet_transitions_ represents the entire non-deterministic transition function by storing a vector of
        //! possible tuples (s, a, s').
        std::set<std::tuple<unsigned, unsigned, unsigned>> agent_transitions_;
        std::set<std::tuple<unsigned, unsigned, unsigned>> nondet_transitions_;
        //! possible tuples (s, a, s', S'').
        std::set<std::tuple<unsigned, unsigned, unsigned, std::set<unsigned>>> transitions_;

        //! trdata_[s] contains a vector with all state IDs of the states s' that can be reached in the state space
        //! in one single step from s
        std::map<unsigned, std::set<unsigned>> agent_trdata_;
        std::map<unsigned, std::set<unsigned>> nondet_trdata_;


        std::set<unsigned> alive_states_;
        std::set<unsigned> goal_states_;
        std::set<unsigned> unsolvable_states_;
        std::set<unsigned> alive_states_sp_;

        std::map<unsigned, int> vstar_;

    public:
        TransitionSample(std::size_t num_states, std::size_t num_states_s_spp, std::size_t num_nondet_transitions, std::size_t num_agent_transitions)
                : num_states_(num_states),
                  num_states_s_spp_(num_states_s_spp),
                  num_nondet_transitions_(num_nondet_transitions),
                  num_agent_transitions_(num_agent_transitions),
                  alive_states_(), // include states s and spp
                  goal_states_(), // include states s and spp
                  unsolvable_states_(), // include states s and spp
                  alive_states_sp_(), // include states sp
                  vstar_()
        {
            if (num_states_s_spp_ > std::numeric_limits<state_id_t>::max()) {
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
        std::size_t num_states_s_spp() const { return num_states_s_spp_;}
        std::size_t num_nondet_transitions() const { return num_nondet_transitions_; }
        std::size_t num_agent_transitions() const { return num_agent_transitions_; }

        const std::set<std::tuple<unsigned, unsigned, unsigned>>& agent_transitions() const {
            return agent_transitions_;
        }

        const std::set<std::tuple<unsigned, unsigned, unsigned>>& nondet_transitions() const {
            return nondet_transitions_;
        }

        const std::set<std::tuple<unsigned, unsigned, unsigned, std::set<unsigned>>>& transitions() const {
            return transitions_;
        }

        int vstar(unsigned sid) const {
            return vstar_.at(sid);
        }

        const std::set<unsigned>& agent_successors(unsigned s) const {
            return agent_trdata_.at(s);
        }

        const std::set<unsigned>& nondet_successors(unsigned s) const {
            return nondet_trdata_.at(s);
        }

        bool is_alive(unsigned state) const { return alive_states_.find(state) != alive_states_.end(); }
        bool is_goal(unsigned state) const { return goal_states_.find(state) != goal_states_.end(); }
        bool is_unsolvable(unsigned state) const { return unsolvable_states_.find(state) != unsolvable_states_.end(); }
        bool is_alive_sp(unsigned state) const { return alive_states_sp_.find(state) != alive_states_sp_.end(); }

        unsigned num_unsolvable() const {
            return unsolvable_states_.size();
        }

        const std::set<unsigned>& all_alive() const { return alive_states_; }
        const std::set<unsigned>& all_goals() const { return goal_states_; }
        const std::set<unsigned>& all_dead() const { return unsolvable_states_; }
        const std::set<unsigned>& all_alive_sp() const { return alive_states_sp_; }

        //! Print a representation of the object to the given stream.
        friend std::ostream& operator<<(std::ostream &os, const TransitionSample& o) { return o.print(os); }
        std::ostream& print(std::ostream &os) const {
            os << "Transition sample [#states (s, s'')=" << num_states_s_spp_
               << ", #transitions (non-det)=" << num_nondet_transitions_
               << ", #transitions (agent)=" << num_agent_transitions_
               << std::endl;
            return os;
        }

        // readers
        void read(std::istream &is) {

            // read number of states that have been expanded, for which we'll have one state per line next
            unsigned n_read_transitions = 0;

            // read transitions, in format: s_id, vstar, num_sp, num_spp, (op0, sp0, spp0), (op0, sp0, spp1)...
            for (unsigned i = 0; i < num_states_s_spp_; ++i) {
                unsigned s = 0, n_sp = 0, n_spp = 0, op0 = 0, sp = 0, spp = 0;
                int vstar = 0;
                is >> s >> vstar >> n_sp >> n_spp;
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

                if (n_spp > 0) {
//                    std::vector<bool> seen(num_states_s_spp_ + num_states_sp_, false);
                    std::map<std::pair<unsigned,unsigned>,std::set<unsigned>> tmp_a_sp_spps;

                    for (unsigned j = 0; j < n_spp; ++j) {
                        is >> op0 >> sp >> spp;
//                        assert(spp < num_states_);
                        agent_trdata_[s].insert(sp);
                        nondet_trdata_[s].insert(spp);
                        agent_transitions_.insert(std::make_tuple(s, op0, sp));
                        nondet_transitions_.insert(std::make_tuple(s, op0, spp));
                        tmp_a_sp_spps[{op0, sp}].insert(spp);
                        n_read_transitions++;
                    }

                    for (auto const& [pair, spps]:tmp_a_sp_spps) {
                        transitions_.insert(std::make_tuple(s, pair.first, pair.second, spps));
                    }

                    assert(agent_trdata_[s].empty());
                    assert(nondet_trdata_[s].empty());

                }
            }

            // post alive states sp
            for (unsigned s = 0; s < num_states_; ++s) {
                if (!(is_alive(s) || is_goal(s) || is_unsolvable(s))) {
                    alive_states_sp_.insert(s);
                }
            }

            assert(n_read_transitions==num_nondet_transitions);

            std::cout << "Read " << alive_states_.size() << " alive states" << std::endl;
        }

        static TransitionSample read_dump(std::istream &is, bool verbose) {
            unsigned num_states = 0, num_states_s_spp = 0, num_nondet_transitions = 0, num_agent_transitions = 0;
            is >> num_states >> num_states_s_spp >> num_nondet_transitions >> num_agent_transitions;
            TransitionSample transitions(num_states, num_states_s_spp, num_nondet_transitions, num_agent_transitions);
            transitions.read(is);
            if( verbose ) {
                std::cout << "TransitionSample::read_dump:#states=" << transitions.num_states()
                          << ", #states (s, s'')="<< transitions.num_states_s_spp()
                          << ", #transitions (non-det)=" << transitions.num_nondet_transitions()
                          << ", #transitions (agent)=" << transitions.num_agent_transitions()
                          << std::endl;
            }
            return transitions;
        }
    };

} // namespaces
