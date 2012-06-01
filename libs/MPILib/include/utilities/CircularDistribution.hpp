/*
 * CircularDistribution.hpp
 *
 *  Created on: 01.06.2012
 *      Author: david
 */

#ifndef MPILIB_UTILITIES_CIRCULARDISTRIBUTION_HPP_
#define MPILIB_UTILITIES_CIRCULARDISTRIBUTION_HPP_

#include <MPILib/include/utilities/NodeDistributionInterface.hpp>

namespace MPILib {
namespace utilities {

class CircularDistribution: public NodeDistributionInterface {
public:
	CircularDistribution();
	virtual ~CircularDistribution();

	/** check is a node is local to the processor
	 * @param The Id of the Node
	 * @return true if the Node is local
	 */
	virtual bool isLocalNode(NodeId) const;
	/** get the processor number which is responsible for the node
	 * @param The Id of the Node
	 * @return the processor responsible
	 */
	virtual int getResponsibleProcessor(NodeId) const;

	/**
	 * If the processor is master (We assume the processor with _processorId=0 is the master)
	 * @return true if the node is the master.
	 */
	virtual bool isMaster() const;

	/**
	 * Get the rank of the processor
	 * @return the rank of the processor
	 */
	virtual int getRank() const;

	/**
	 * Get the size of the system
	 * @return the size of the system
	 */
	virtual int getSize() const;


private:
	/**
	 * The local processor id
	 */
	int _processorId;

	/**
	 * The total number of processors
	 */
	int _totalProcessors;
};

} /* namespace MPILib */
} /* namespace utilities */
#endif /* MPILIB_UTILITIES_CIRCULARDISTRIBUTION_HPP_ */