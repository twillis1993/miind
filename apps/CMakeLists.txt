ADD_SUBDIRECTORY( BasicDemos )
ADD_SUBDIRECTORY( largeNetwork )
ADD_SUBDIRECTORY( UnitMPILib )
ADD_SUBDIRECTORY( UnitGeomLib )
ADD_SUBDIRECTORY( UnitTwoDLib )
ADD_SUBDIRECTORY( IntegrationTwoDLib )
ADD_SUBDIRECTORY( PerformanceGeom )
ADD_SUBDIRECTORY( Projection )
ADD_SUBDIRECTORY( MatrixGenerator )
#ADD_SUBDIRECTORY( TvbModels )
if(ENABLE_CUDA)
if(APPLE)
message("Cuda support is not defined on Mac Os")
else(APPLE)
ADD_SUBDIRECTORY(UnitCudaLib)
endif(APPLE)
endif(ENABLE_CUDA)
