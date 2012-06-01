/*
 * CircularDistribution.cpp
 *
 *  Created on: 01.06.2012
 *      Author: david
 */

#include <MPILib/include/utilities/CircularDistribution.hpp>
#include <boost/mpi/communicator.hpp>

using namespace MPILib::utilities;
namespace mpi = boost::mpi;

CircularDistribution::CircularDistribution() {
	mpi::communicator world;

	_processorId = world.rank();
	_totalProcessors = world.size();
}

CircularDistribution::~CircularDistribution() {
}

bool CircularDistribution::isLocalNode(NodeId nodeId) const {
	return getResponsibleProcessor(nodeId) == _processorId;

}

int CircularDistribution::getResponsibleProcessor(NodeId nodeId) const {
	return nodeId % _totalProcessors;

}

bool CircularDistribution::isMaster() const {
	return _processorId == 0;
}

int CircularDistribution::getRank() const{
	return _processorId;
}

int CircularDistribution::getSize() const{
	return _totalProcessors;
}

