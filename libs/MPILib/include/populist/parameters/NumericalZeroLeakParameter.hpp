// Copyright (c) 2005 - 2012 Marc de Kamps
//						2012 David-Matthias Sichau
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
//
//    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
//    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation
//      and/or other materials provided with the distribution.
//    * Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software
//      without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
// USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
// NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
#ifndef MPILIB_POPULIST_PARAMETERS_NUMERICALZEROLEAKPARAMETER_HPP_
#define MPILIB_POPULIST_PARAMETERS_NUMERICALZEROLEAKPARAMETER_HPP_

#include <MPILib/include/TypeDefinitions.hpp>
#include <MPILib/include/populist/ProbabilityQueue.hpp>

namespace MPILib {
namespace populist {
namespace parameters{

/**
 * @brief To be used internally by NumericalZeroLeakEquations
 *
 * @todo add documentation for members
 */
struct NumericalZeroLeakParameter {
	Number _nr_current_bins = 0;
	Number _nr_max_bins = 0;
	Index _i_reversal = 0;
	Index _i_reset = 0;
	Index _i_reset_orig = 0;
	Index _H = 0;
	Rate _eff_rate_exc = 0.0;
	Rate _eff_rate_inh = 0.0;
	double _alpha_e = 0.0;
	double _alpha_i = 0.0;
	Time _t_ref = 0.0;
	Time _t_abs = 0.0;

	ProbabilityQueue* _p_queue = nullptr;
	/**
	 * default constructor
	 */
	NumericalZeroLeakParameter()= default;
};
} /* namespace parameters */

} /* namespace populist */
} /* namespace MPILib */
#endif //include guard MPILIB_POPULIST_PARAMETERS_NUMERICALZEROLEAKPARAMETER_HPP_