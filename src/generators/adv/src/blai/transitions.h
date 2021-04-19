
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
        const std::size_t num_states_s_spp_;
        const std::size_t num_nondet_transitions_;
        const std::size_t num_agent_transitions_;

        //! nondet_transitions_ represents the entire non-deterministic transition function by storing a vector of
        //! possible tuples (s, a, s').
        std::vector<std::tuple<unsigned, unsigned, unsigned>> agent_transitions_;
        std::vector<std::tuple<unsigned, unsigned, unsigned>> nondet_transitions_;

        //! trdata_[s] contains a vector with all state IDs of the states s' that can be reached in the state space
        //! in one single step from s
        std::vector<std::vector<unsigned>> agent_trdata_;
        std::vector<std::vector<unsigned>> nondet_trdata_;

        std::vector<bool> is_state_alive_;
        std::vector<bool> is_state_goal_;
        std::vector<bool> is_state_unsolvable_;
        std::vector<bool> is_state_alive_sp_;

        std::vector<unsigned> alive_states_;
        std::vector<unsigned> goal_states_;
        std::vector<unsigned> unsolvable_states_;

        std::vector<int> vstar_;

    public:
        TransitionSample(std::size_t num_states, std::size_t num_states_s_spp, std::size_t num_nondet_transitions, std::size_t num_agent_transitions)
                : num_states_(num_states),
                  num_states_s_spp_(num_states_s_spp),
                  num_nondet_transitions_(num_nondet_transitions),
                  num_agent_transitions_(num_agent_transitions),
                  agent_trdata_(num_agent_transitions),
                  nondet_trdata_(num_nondet_transitions),
                  is_state_alive_(num_states_s_spp, false), // include states s and spp
                  is_state_goal_(num_states_s_spp, false), // include states s and spp
                  is_state_unsolvable_(num_states_s_spp, false), // include states s and spp
                  is_state_alive_sp_(num_states, false), // include states sp
                  alive_states_(),
                  goal_states_(),
                  unsolvable_states_()
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

        const std::vector<std::tuple<unsigned, unsigned, unsigned>>& agent_transitions() const {
            return agent_transitions_;
        }

        const std::vector<std::tuple<unsigned, unsigned, unsigned>>& nondet_transitions() const {
            return nondet_transitions_;
        }

        int vstar(unsigned sid) const {
            auto vstar = vstar_.at(sid);
            return vstar < 0 ? -1 : vstar;
        }

        const std::vector<unsigned>& agent_successors(unsigned s) const {
            return agent_trdata_.at(s);
        }

        const std::vector<unsigned>& nondet_successors(unsigned s) const {
            return nondet_trdata_.at(s);
        }

        bool is_alive(unsigned state) const { return is_state_alive_.at(state); }
        bool is_goal(unsigned state) const { return is_state_goal_.at(state); }
        bool is_unsolvable(unsigned state) const { return is_state_unsolvable_.at(state); }
        bool is_alive_sp(unsigned state) const { return is_state_alive_sp_.at(state); }

        unsigned num_unsolvable() const {
            unsigned c = 0;
            for (auto const& [s, o, spp]:nondet_transitions_) {
                if (is_unsolvable(s)) c += 1;
            }
            return c;
        }

        const std::vector<unsigned>& all_alive() const { return alive_states_; }
        const std::vector<unsigned>& all_goals() const { return goal_states_; }
        const std::vector<unsigned>& all_dead() const { return unsolvable_states_; }

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
            vstar_.reserve(num_states_s_spp_);

            // read transitions, in format: s_id, vstar, num_sp, num_spp, (op0, sp0, spp0), (op0, sp0, spp1)...
            for (unsigned i = 0; i < num_states_s_spp_; ++i) {
                unsigned s = 0, vstar=0, n_sp = 0, n_spp = 0, op0 = 0, sp = 0, spp = 0;
                is >> s >> vstar >> n_sp >> n_spp;
//                assert(i==src);
//                assert(src < num_states_ && 0 <= count);
                if (n_spp > 0) {
//                    std::vector<bool> seen(num_states_s_spp_ + num_states_sp_, false);
                    agent_trdata_[s].reserve(n_sp);
                    nondet_trdata_[s].reserve(n_spp);
                    std::unordered_set<unsigned> all_sp_successors;
                    std::unordered_set<unsigned> all_spp_successors;
                    for (unsigned j = 0; j < n_spp; ++j) {
                        is >> op0 >> sp >> spp;
//                        assert(spp < num_states_);
                        all_sp_successors.insert(sp);
                        all_spp_successors.insert(spp);
                        agent_transitions_.emplace_back(s, op0, sp);
                        nondet_transitions_.emplace_back(s, op0, spp);
                        n_read_transitions++;
                    }

                    assert(agent_trdata_[s].empty());
                    assert(nondet_trdata_[s].empty());
                    agent_trdata_[s].insert(agent_trdata_[s].end(), all_sp_successors.begin(), all_sp_successors.end());
                    nondet_trdata_[s].insert(nondet_trdata_[s].end(), all_spp_successors.begin(), all_spp_successors.end());

                    // Store the value of V^*(s) for each state s
                    vstar_.push_back(vstar);
                    if (vstar>0) {
                        is_state_alive_[s] = true;
                        alive_states_.push_back(s);
                    } else if (vstar<0) {
                        is_state_unsolvable_[s] = true;
                        unsolvable_states_.push_back(s);
                    } else {
                        is_state_goal_[s] = true;
                        goal_states_.push_back(s);
                    }
                }
            }

            // post alive states sp
            for (unsigned s = 0; s < num_states_; ++s) {
                if (!(is_alive(s) || is_goal(s) || is_unsolvable(s))) {
                    is_state_alive_sp_[s] = true;
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
