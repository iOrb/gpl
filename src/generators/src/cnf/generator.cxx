
#include <common/helpers.h>
#include "generator.h"
#include "types.h"

namespace sltp::cnf {

//! Return a sorted vector with those features that d1-distinguish s from t
std::vector<feature_t> compute_d1_distinguishing_features(const TrainingSet& sample, unsigned s, unsigned t) {
    std::vector<unsigned> features;
    const auto& mat = sample.matrix();
    for (unsigned f = 0; f < mat.num_features(); ++f) {
        auto sf = mat.entry(s, f);
        auto tf = mat.entry(t, f);
        if ((sf == 0) != (tf == 0)) {
            features.push_back(f);
        }
    }
    return features;
}

//! Return a sorted vector with those features that either d1-distinguish or d2-distinguish (s, s') from (t, t')
std::vector<feature_t> compute_d1d2_distinguishing_features(
        const std::vector<unsigned>& feature_ids,
        const TrainingSet& sample,
        unsigned s, unsigned sprime,
        unsigned t, unsigned tprime)
{
    std::vector<unsigned> features;
    const auto& mat = sample.matrix();

    for (unsigned f:feature_ids) {
        if (are_transitions_d1d2_distinguished(
                mat.entry(s, f), mat.entry(sprime, f), mat.entry(t, f), mat.entry(tprime, f))) {
            features.push_back(f);
        }
    }

    return features;
}


} // namespaces
