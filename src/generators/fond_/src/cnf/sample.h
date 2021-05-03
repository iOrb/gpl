
#pragma once

#include <utility>
#include <vector>
#include <cstdint>
#include <string>

#include <blai/matrix.h>
#include <blai/transitions.h>
#include <blai/sample.h>
#include <common/utils.h>
#include <unordered_set>
#include <random>


enum class FeatureValue {
    Eq0 = 0,
    Gt0 = 1,
    Dec = 2,
    Nil = 3,
    Inc = 4
};

inline std::string print_feature_value(const FeatureValue& fval) {
    if (fval == FeatureValue::Eq0) return "=0";
    else if (fval == FeatureValue::Gt0) return ">0";
    else if (fval == FeatureValue::Dec) return "DEC";
    else if (fval == FeatureValue::Nil) return "NIL";
    else if (fval == FeatureValue::Inc) return "INC";
    throw std::runtime_error("Unexpected Feature Value");
}

//class DNFPolicy {
//public:
//    using literal_t = std::pair<uint32_t, FeatureValue>;
//    using term_t = std::vector<literal_t>;
//
//    static FeatureValue compute_state_value(unsigned x) { return x>0 ? FeatureValue::Gt0 : FeatureValue::Eq0; }
//    static FeatureValue compute_transition_value(unsigned xs, unsigned xsprime) {
//        if (xs == xsprime) return FeatureValue::Nil;
//        return xs > xsprime ? FeatureValue::Dec : FeatureValue::Inc;
//    }
//
//    DNFPolicy() = default;
//    explicit DNFPolicy(std::vector<unsigned> features_) :
//            features(std::move(features_)), terms()
//    {}
//
//    std::vector<unsigned> features;
//    std::unordered_set<term_t, sltp::utils::container_hash<term_t>> terms;
//
//};

class DNFAPolicy {
public:
    using literal_t = std::pair<uint32_t, FeatureValue>;
    using term_t = std::vector<literal_t>;

    static FeatureValue compute_state_value(unsigned x) { return x>0 ? FeatureValue::Gt0 : FeatureValue::Eq0; }
    static FeatureValue compute_transition_value(unsigned xs, unsigned xsprime) {
        if (xs == xsprime) return FeatureValue::Nil;
        return xs > xsprime ? FeatureValue::Dec : FeatureValue::Inc;
    }

    DNFAPolicy() = default;
    explicit DNFAPolicy(std::vector<unsigned> features_) :
            features(std::move(features_)), terms()
    {}

    std::vector<unsigned> features;
    std::unordered_set<term_t, sltp::utils::container_hash<term_t>> terms; // {tx1, tx2, ...}, where tx=(s, a, s')

};

//class FixedActionPolicy {
//public:
//    using literal_t = std::pair<uint32_t, FeatureValue>;
//    using term_t = std::vector<literal_t>;
//
//    static FeatureValue compute_state_value(unsigned x) {
//        return x>0 ? FeatureValue::Gt0 : FeatureValue::Eq0;
//    }
//
//    FixedActionPolicy() = default;
//    explicit FixedActionPolicy(std::vector<unsigned> features_) :
//            features(std::move(features_)), terms()
//    {}
//
//    std::vector<unsigned> features;
//    std::unordered_set<std::pair<term_t, unsigned>, boost::hash<std::pair<term_t, unsigned>>> terms;
//};


namespace sltp::cnf {

    class StateSpaceSample {
    public:
        const FeatureMatrix& matrix_;
        const TransitionSample& transitions_;

        //! The states that belong to this sample
        std::unordered_set<unsigned> states_;

        std::set<unsigned> alive_states_;
        std::set<unsigned> goal_states_;
        std::set<unsigned> nongoal_states_;

        StateSpaceSample(const FeatureMatrix& matrix, const TransitionSample& transitions, std::set<unsigned> states) :
                matrix_(matrix), transitions_(transitions), states_(states.begin(), states.end())
        {
            // Let's classify the states for easier access
            for (unsigned s:states_) {
                if (is_alive(s)) alive_states_.insert(s);
                if (is_goal(s)) goal_states_.insert(s);
                if (is_unsolvable(s)) nongoal_states_.insert(s);
            }
        }

        virtual ~StateSpaceSample() = default;
        StateSpaceSample(const StateSpaceSample&) = default;

//    const std::vector<unsigned>& states() const {
//        return states_;
//    }

        inline bool in_sample(unsigned s) const {
            return states_.find(s) != states_.end();
        }

        const FeatureMatrix& matrix() const { return matrix_; }

        //! Return all alive states in this sample
        const std::set<unsigned>& alive_states() const { return transitions_.all_alive(); }
        const std::set<unsigned>& goal_states() const { return transitions_.all_goal(); }
        const std::set<unsigned>& nongoal_states() const { return transitions_.all_dead(); }

        bool is_goal(unsigned s) const { return transitions_.is_goal(s); }
        bool is_alive(unsigned s) const { return transitions_.is_alive(s); }
        bool is_solvable(unsigned s) const { return is_alive(s) || is_goal(s); }
        bool is_unsolvable(unsigned s) const { return transitions_.is_unsolvable(s); }

        inline FeatureMatrix::feature_value_t value(unsigned s, unsigned f) const {
            return matrix_.entry(s, f);
        }

        unsigned feature_weight(unsigned f) const {
            return matrix_.feature_cost(f);
        }

        const std::unordered_set<unsigned>& nondet_successors(unsigned s) const {
            return transitions_.nondet_successors(s);
        }

        const TransitionSample& full_training_set() const {
            return transitions_;
        }

        StateSpaceSample* add_states(const std::vector<unsigned>& states) const {
            std::set<unsigned> tmp(states_.begin(), states_.end());
            tmp.insert(states.begin(), states.end());
            return new StateSpaceSample(matrix_, transitions_, {tmp.begin(), tmp.end()});
        }

        friend std::ostream& operator<<(std::ostream &os, const StateSpaceSample& o) { return o.print(os); }
        std::ostream& print(std::ostream &os) const {
            os << "Sample [sz=" << states_.size() << "]: ";
            for (const auto& s:states_) os << s << ", ";
            os << std::endl;
            return os;
        }
    };

    void print_classifier(const sltp::FeatureMatrix& matrix, const FixedActionPolicy& dnf, const std::string& filename);

    class StateSampler {
    protected:
        std::mt19937& rng;
        const TrainingSet& trset;
        unsigned verbosity;


    public:
        StateSampler(std::mt19937& rng, const TrainingSet& trset, unsigned verbosity)
                : rng(rng), trset(trset), verbosity(verbosity)
        {}

        virtual StateSpaceSample* sample_initial_states(unsigned n) = 0;

        virtual std::vector<unsigned> sample_flaws(const FixedActionPolicy& dnf, unsigned batch_size) = 0;


    protected:
        std::set<unsigned> randomize_all_alive_states(unsigned n = std::numeric_limits<unsigned>::max());
        std::vector<unsigned> sample_flaws(const FixedActionPolicy& dnf, unsigned batch_size, const std::set<unsigned>& states_to_check);

    };

    class RandomSampler : public StateSampler {
    public:
        RandomSampler(std::mt19937& rng, const TrainingSet& trset, unsigned verbosity)
                : StateSampler(rng, trset, verbosity)
        {}

        StateSpaceSample* sample_initial_states(unsigned n) override;
        std::vector<unsigned> sample_flaws(const FixedActionPolicy& dnf, unsigned batch_size) override;

    protected:
        using StateSampler::sample_flaws;
    };

    class GoalDistanceSampler : public StateSampler {
    public:
        GoalDistanceSampler(std::mt19937& rng, const TrainingSet& trset, unsigned verbosity)
                : StateSampler(rng, trset, verbosity)
        {}

        StateSpaceSample* sample_initial_states(unsigned n) override;
        std::vector<unsigned> sample_flaws(const FixedActionPolicy& dnf, unsigned batch_size) override;

        std::set<unsigned> randomize_and_sort_alive_states(unsigned n = std::numeric_limits<unsigned>::max());

        std::unordered_map<unsigned, unsigned> compute_goal_distance_histogram(const std::vector<unsigned> states);


    protected:
        using StateSampler::sample_flaws;
    };

    inline std::unique_ptr<StateSampler> select_sampler(const std::string& strategy, std::mt19937& rng, const TrainingSet& trset, unsigned verbosity) {
        if (strategy == "random") return std::make_unique<RandomSampler>(rng, trset, verbosity);
        else if (strategy == "goal") return std::make_unique<GoalDistanceSampler>(rng, trset, verbosity);
        else throw std::runtime_error("Unknown state sampling strategy " + strategy);
    }


}