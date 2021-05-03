#pragma once

#include "d2l.h"

namespace sltp::cnf {
    class EncodingFactory {
    public:
        EncodingFactory();

        //! Factory method
        static std::unique_ptr<D2LEncoding> create(const StateSpaceSample &sample, const Options &options) {
            return std::make_unique<D2LEncoding>(sample, options);
        }
    };
}