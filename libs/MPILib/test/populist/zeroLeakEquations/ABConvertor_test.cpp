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

#include <vector>
#include <MPILib/include/TypeDefinitions.hpp>
#define private public
#define protected public
#include <MPILib/include/populist/zeroLeakEquations/ABConvertor.hpp>
#undef protected
#undef private
#include <MPILib/include/populist/zeroLeakEquations/SpecialBins.hpp>
#include <MPILib/include/populist/parameters/PopulistSpecificParameter.hpp>
#include <MPILib/include/populist/parameters/PopulistParameter.hpp>

#include <boost/test/minimal.hpp>
using namespace boost::unit_test;
using namespace MPILib::populist;
using namespace MPILib::populist::zeroLeakEquations;
using namespace MPILib;

void test_Constructor() {
	parameters::PopulistSpecificParameter popSpecParam;
	parameters::OrnsteinUhlenbeckParameter popParam;

	SpecialBins specBins { 4, 5, 6 };
	Potential pot = 2.0;
	Number num = 3;

	ABConvertor converter(specBins, popParam, popSpecParam, pot, num);

	BOOST_CHECK(converter._p_pop==&popParam);
	BOOST_CHECK(converter._p_specific==&popSpecParam);
	BOOST_CHECK((*converter._p_delta_v)==2.0);
	BOOST_CHECK(converter._p_delta_v==&pot);

	BOOST_CHECK((*converter._p_n_bins)==3.0);
	BOOST_CHECK(converter._p_n_bins==&num);


}

void test_SortConnectionvector(){
	parameters::PopulistSpecificParameter popSpecParam;
	parameters::OrnsteinUhlenbeckParameter popParam;
	SpecialBins specBins { 4, 5, 6 };
	Potential pot = 2.0;
	Number num = 3;
	ABConvertor converter(specBins, popParam, popSpecParam, pot, num);

	std::vector<Rate> rates;
	std::vector<OrnsteinUhlenbeckConnection> weights;
	std::vector<NodeType> types;

	rates.push_back(6.0);
	weights.push_back(OrnsteinUhlenbeckConnection(2.0,3.0));
	types.push_back(EXCITATORY_DIRECT);
	rates.push_back(2.0);
	weights.push_back(OrnsteinUhlenbeckConnection(4.0,5.0));
	types.push_back(INHIBITORY_DIRECT);
	rates.push_back(3.0);
	weights.push_back(OrnsteinUhlenbeckConnection(6.0,7.0));
	types.push_back(INHIBITORY_GAUSSIAN);

	converter.SortConnectionvector(rates, weights, types);
	BOOST_CHECK(converter._param_input._par_input._a==6.91423056);
	BOOST_CHECK(converter._param_input._par_input._b==0.13299526);
	BOOST_CHECK(converter._param_input._par_input._q==0.0);

}

void test_RecalculateSolverParameters(){
	///@todo implement this test
}

int test_main(int argc, char* argv[]) // note the name!
		{

	test_Constructor();
	test_SortConnectionvector();
	test_RecalculateSolverParameters();
	return 0;
//    // six ways to detect and report the same error:
//    BOOST_CHECK( add( 2,2 ) == 4 );        // #1 continues on error
//    BOOST_CHECK( add( 2,2 ) == 4 );      // #2 throws on error
//    if( add( 2,2 ) != 4 )
//        BOOST_ERROR( "Ouch..." );          // #3 continues on error
//    if( add( 2,2 ) != 4 )
//        BOOST_FAIL( "Ouch..." );           // #4 throws on error
//    if( add( 2,2 ) != 4 ) throw "Oops..."; // #5 throws on error
//
//    return add( 2, 2 ) == 4 ? 0 : 1;       // #6 returns error code
}
