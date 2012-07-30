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
#ifndef MPILIB_POPULIST_CIRCULANTSOLVERS_CIRCULANTSOLVER_HPP_
#define MPILIB_POPULIST_CIRCULANTSOLVERS_CIRCULANTSOLVER_HPP_

#include <valarray>
#include <MPILib/include/populist/circulantSolvers/AbstractCirculantSolver.hpp>
#include <MPILib/include/TypeDefinitions.hpp>
#include <MPILib/include/populist/parameters/InputParameterSet.hpp>
#include <MPILib/include/populist/circulantSolvers/VArray.hpp>

namespace MPILib {
namespace populist {
namespace circulantSolvers {

/**
 * This is the literal implementation of the analytic solution from (de Kamps, 2006).
 * It is not efficient and should probably not be used in realistic applications, but
 * is important in the benchmarking of other circulant solvers
 */
class CirculantSolver: public AbstractCirculantSolver {
public:
	/**
	 * default constructor
	 * @param mode the circulant mode
	 */
	CirculantSolver(CirculantMode mode = INTEGER);

	/**
	 * virtual destructor
	 */
	virtual ~CirculantSolver(){};
	/**
	 * Only concrete CirculantSolvers know how to compute their contribution. At this stage it is assumed that
	 * during configure the InputParameterSet is defined. The number of circulant bins, the number of
	 * non_circulant_areas. H_exc and alpha_exc must all be defined.
	 * @param n_bins Current number of bins that needs to be solved, cannot be larger than number of elements in state array
	 * @param tau Time through which evolution needs to be carried out, this may not be related to the absolute time of the simulation
	 * @param t_sim Irrelevant for this solver
	 */
	virtual void Execute(Number n_bins, Time tau, Time t_sim= 0) override;

	/**
	 * Integrate the grid
	 * @param number_circulant until where the integral is made
	 * @return The integral
	 */
	double Integrate(Number number_circulant) const;

	/**
	 * Purpose: Calculates the flux according to equation .. in [1]
	 * Assumptions: FillNonCirculantBins must be called to initialize the initial density properly
	 * this is the USER's responsibility.
	 * This call can be made explicitly, or implicitly via this->Execute(),
	 * i.e. this function will correctly immediately after Execute is called
	 * @param number_non_circulant_areas
	 * @param tau The time
	 * @return the flux
	 */
	double Flux(Number number_non_circulant_areas, Time tau) const;

	/**
	 * Clone operation
	 * @return A clone of the CirculantSolver
	 */
	virtual CirculantSolver* clone() const
	override;

private:
	/**
	 * This is the calculation of the matrix V_jk, which plays a role in the analytic circulant solution
	 * Since the full matrix can be generated by translations a single row, the whole matrix can be stored
	 * in a single array.
	 */
	void CalculateInnerProduct();

	/**
	 * The Array where the state is stored
	 */
	VArray _array_V;
};} /* namespace circulantSolvers*/
} /* namespace populist */
} /* namespace MPILib */

#endif // include guard MPILIB_POPULIST_CIRCULANTSOLVERS_CIRCULANTSOLVER_HPP_
