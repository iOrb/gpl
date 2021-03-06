
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
    std::unordered_map<unsigned, cnfvar_t> goods;
    std::unordered_map<tx_triple, cnfvar_t, boost::hash<tx_triple>> goods_s_a_sp;
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

    //static std::unique_ptr<D2LEncoding> create(const StateSpaceSample& sample, const Options& options);

    D2LEncoding(const StateSpaceSample& sample, const Options& options) :
            sample_(sample),
            options(options),
            nf_(sample.matrix().num_features()),
            transition_ids_(),
            transition_ids_inv_(),
            class_representatives_(),
            from_transition_to_eq_class_(),
            necessarily_bad_transitions_(),
            necessarily_bad_sa_(),
            necessarily_good_sa_(),
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

    inline unsigned get_transition_id(state_id_t s, state_id_t t) const { return transition_ids_.at(state_pair(s, t)); }

    inline unsigned get_representative_id(unsigned tx) const { return from_transition_to_eq_class_.at(tx); }

    inline unsigned get_class_representative(state_id_t s, state_id_t t) const {
        return get_representative_id(get_transition_id(s, t));
    }

    inline const state_pair& get_state_pair(unsigned tx) const { return transition_ids_inv_.at(tx); }

    inline const state_id_t& get_s(tx_triple tx) const { return std::get<0>(tx); }
    inline const state_id_t& get_a(tx_triple tx) const { return std::get<1>(tx); }
    inline const state_id_t& get_sp(tx_triple tx) const { return std::get<2>(tx); }

    inline bool is_necessarily_bad(unsigned tx) const {
        return necessarily_bad_transitions_.find(tx) != necessarily_bad_transitions_.end();
    }
    inline bool is_necessarily_bad_tx(tx_triple tx) const {
        return necessarily_bad_sa_.find(tx) != necessarily_bad_sa_.end();
    }
    inline bool is_necessarily_good_tx(tx_triple tx) const {
        return necessarily_good_sa_.find(tx) != necessarily_good_sa_.end();
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
        for (const auto s:sample_.alive_states()) {
            auto max_v_s = get_max_v(s);
            if (max_v_s > D) D = max_v_s;
        }
        return D;
    }

    //! Whether the two given transitions are distinguishable through the given features alone
    bool are_transitions_d1d2_distinguishable(
            state_id_t s, state_id_t sprime, state_id_t t, state_id_t tprime, const std::vector<unsigned>& features) const;

    DNFPolicy generate_dnf_from_solution(const VariableMapping& variables, const SatSolution& solution) const;

//    DNFPolicy generate_dnf(const std::vector<unsigned>& goods, const std::vector<unsigned>& selecteds) const;
    DNFPolicy generate_dnf(const std::vector<std::tuple<unsigned, unsigned, unsigned>>& goods, const std::vector<unsigned>& selecteds) const;

    int get_num_features(){ return feature_ids.size(); }
    int get_num_tx(){ return transition_ids_.size(); }
    int get_num_tx_eq(){ return class_representatives_.size(); }
    int get_feature_weight( unsigned f ){ return sample_.feature_weight(f); }

        protected:
    //! The transition sample data
    const StateSpaceSample& sample_;

    //! The CNF encoding options
    const Options& options;

    //! The number of features in the encoding
    const std::size_t nf_;

    //! A mapping from pairs of state to the assigned transition id
    std::unordered_map<state_pair, unsigned, boost::hash<state_pair>> transition_ids_;

    //! The reverse mapping
    std::vector<state_pair> transition_ids_inv_;

    //! A list of transition IDs that are the representative of their class
    std::vector<unsigned> class_representatives_;

    //! A mapping from the ID of the transition to the ID of its equivalence class
    std::vector<unsigned> from_transition_to_eq_class_;

    std::unordered_set<unsigned> necessarily_bad_transitions_;
    std::set<tx_triple> necessarily_bad_sa_;
    std::set<tx_triple> necessarily_good_sa_;

    //! The only feature IDs that we will consider for the encoding
    std::vector<unsigned> feature_ids;

    //!
    void compute_equivalence_relations();

    void report_eq_classes() const;

    std::vector<transition_pair> distinguish_all_transitions() const;

    void post_variables_selected(const VariableMapping &mapping, const SatSolution &solution) const;
};

} // namespaces

