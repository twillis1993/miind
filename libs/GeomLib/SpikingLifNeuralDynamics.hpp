// Copyright (c) 2005 - 2014 Marc de Kamps
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
//      If you use this software in work leading to a scientific publication, you should include a reference there to
//      the 'currently valid reference', which can be found at http://miind.sourceforge.net
#ifndef _CODE_LIBS_GEOMLIB_SPIKINGLIFNEURALDYNAMICS_H_
#define _CODE_LIBS_GEOMLIB_SPIKINGLIFNEURALDYNAMICS_H_

#include <MPILib/include/BasicDefinitions.hpp>
#include "SpikingNeuralDynamics.hpp"
#include "LifParameter.hpp"

using MPILib::Time;

namespace GeomLib {


	class SpikingLifNeuralDynamics : public SpikingNeuralDynamics {
	public:

		SpikingLifNeuralDynamics
		(
			const OdeParameter&,
			const LIFParameter&
		);

		SpikingLifNeuralDynamics
		(
			const SpikingLifNeuralDynamics&
		);

		virtual ~SpikingLifNeuralDynamics();

		//! calculate time to reach threshold for the given potential
		virtual Time TimeToInf(Potential) const;

		virtual Time TStep() const;

		virtual Time TPeriod() const;

		virtual Potential
			EvolvePotential
			(
				Potential,
				Time
			) const;

		virtual SpikingLifNeuralDynamics* Clone() const;


		const LIFParameter& ParLif() const {return _par_lif; }

	protected:

		const LIFParameter _par_lif;

	private:

	};

}




#endif /* SPIKINGLIFNEURALDYNAMICS_H_ */