
#pragma once

#include <common/helpers.h>
#include <cnf/sample.h>
#include <cnf/generator.h>
#include <cnf/types.h>
#include <cnf/solver.h>

#include <numeric>


namespace sltp::cnf {

//! A map between feature IDs and transition IDs) and
//! the CNF variable IDs that tell us whether features are selected in the solution and transitions are labeled as
//! good in the solution
    struct VariableMapping {
        //! A map from each feature index to the SAT variable ID of Selected(f)
        std::vector<cnfvar_t> selecteds;

        //! A map from transition IDs to SAT variable IDs:
        std::unordered_map<tx_triple , cnfvar_t, boost::hash<tx_triple>> goods; // good(s, a, s')
//        std::unordered_map<sa_pair , cnfvar_t, boost::hash<sa_pair>> goods_s_a; // good(s, a)
//        std::unordered_map<sa_pair , std::set<unsigned>, boost::hash<sa_pair>> goods_s_a_txs; // {(s, a): {s1', sp2', ...}}}
//        std::unordered_map<tx_triple, cnfvar_t, boost::hash<tx_triple>> goods_s_a_txs; // {(s, a): {s1', sp2', ...}}}
        std::unordered_map<state_id_t, cnfvar_t, boost::hash<state_id_t>> bad_s; // bad(s)

        explicit VariableMapping(unsigned nfeatures) : selecteds(nfeatures, std::numeric_limits<uint32_t>::max())
        {}
    };


    class D2LEncoding {
    public:
        enum class transition_type : bool {
            alive_to_solvable,
            alive_to_dead
        };

        static std::unique_ptr<D2LEncoding> create(const StateSpaceSample& sample, const Options& options);

        D2LEncoding(const StateSpaceSample& sample, const Options& options) :
                sample_(sample),
                options(options),
                nf_(sample.matrix().num_features()),
                transition_ids_(),
                transition_ids_inv_(),
                class_representatives_(),
                from_transition_to_eq_class_(),
                necessarily_bad_transitions_(),
                feature_ids()
        {
            if (!options.validate_features.empty()) {
                // Consider only the features we want to validate
                feature_ids = options.validate_features;
            } else { // Else, we will simply consider all feature IDs
                feature_ids.resize(nf_);
                std::iota(feature_ids.begin(), feature_ids.end(), 0);
            }

            compute_equivalence_relations();
        }

        virtual ~D2LEncoding() = default;

        virtual std::pair<cnf::CNFGenerationOutput, VariableMapping> generate(CNFWriter& wr);

        // Transitions (s, a, s')

        inline unsigned get_transition_id(state_id_t s, action_id_t a, state_id_t t) const { return transition_ids_.at(tx_triple(s, a, t)); }

        inline unsigned get_representative_id(unsigned tx) const { return from_transition_to_eq_class_.at(tx); }

        inline unsigned get_class_representative(state_id_t s, action_id_t a, state_id_t t) const {
            return get_representative_id(get_transition_id(s, a, t));
        }

        inline const tx_triple & get_tx_triple(unsigned tx) const { return transition_ids_inv_.at(tx); }

        inline bool is_necessarily_bad(unsigned tx) const {
            return necessarily_bad_transitions_.find(tx) != necessarily_bad_transitions_.end();
        }

        inline int get_vstar(unsigned s) const {
            return sample_.transitions_.vstar(s);
        }

        inline int get_max_v(unsigned s) const {
            int vstar = get_vstar(s);
            return vstar < 0 ? -1 : std::ceil(options.v_slack * vstar);
        }

        inline unsigned compute_D() const {
            // return 20;
            // D will be the maximum over the set of alive states of the upper bounds on V_pi
            unsigned D = 0;
            for (const auto s:sample_.transitions_.all_alive()) {
                auto max_v_s = get_max_v(s);
                if (max_v_s > D) D = max_v_s;
            }
            return D;
        }

        //! Whether the two given transitions are distinguishable through the given features alone
        bool are_transitions_d1d2_distinguishable(
                state_id_t s, state_id_t sp, state_id_t t, state_id_t tp, const std::vector<unsigned>& features) const;

        DNFAPolicy generate_dnf_from_solution(const VariableMapping& variables, const SatSolution& solution) const;
        DNFAPolicy generate_dnf(const std::vector<tx_triple>& goods, const std::vector<state_id_t>& bads, const std::vector<unsigned>& selecteds) const;

//        DNFPolicy generate_dnf_from_solution(const VariableMapping& variables, const SatSolution& solution) const;
//        DNFPolicy generate_dnf(const std::vector<unsigned>& goods, const std::vector<unsigned>& bads, const std::vector<unsigned>& selecteds) const;
//        DNFPolicy generate_dnf(const std::vector<std::pair<unsigned, unsigned>>& goods, const std::vector<unsigned>& bads, const std::vector<unsigned>& selecteds) const;


    protected:
        //! The transition sample data
        const StateSpaceSample& sample_;

        //! The CNF encoding options
        const Options& options;

        //! The number of features in the encoding
        const std::size_t nf_;

        //! A mapping from pairs of state to the assigned transition id
        std::unordered_map<tx_triple, unsigned, boost::hash<tx_triple>> transition_ids_;

        //! The reverse mapping
        std::vector<tx_triple> transition_ids_inv_;

        //! A list of transition IDs that are the representative of their class
        std::vector<unsigned> class_representatives_;

        //! A mapping from the ID of the transition to the ID of its equivalence class
        std::vector<unsigned> from_transition_to_eq_class_;

        std::unordered_set<unsigned> necessarily_bad_transitions_;

        //! The only feature IDs that we will consider for the encoding
        std::vector<unsigned> feature_ids;

        //!
        void compute_equivalence_relations();

        void report_eq_classes() const;

        std::vector<transition_pair> distinguish_all_transitions() const;
    };

} // namespaces
