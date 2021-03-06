
configure_file(miind_settings_template ${CMAKE_CURRENT_SOURCE_DIR}/miind_settings)

set( PYTHON_SCRIPTS
algorithms.py
connections.py
lost.py
parametersweep.py
peakdetect.py
bary3.py
demo2D.py
mesh3.py
bary.py
directories3.py
reporting.py
mesh.py
directories.py
simulation.py
cmake_template
meshtest3.py
cmake_template_lib
grid_adex.py
codegen3.py
grid_cond.py
sub.sh
grid_fn.py
miind_lib.py
utilities.py
grid_generate.py
variables.py
codegen_lib3.py
grid_rybak.py
include.py
miindTVBlibs.py
visualize.py
codegen_lib.py
nodes.py
writemesh.py
jobs.py
codegen.py
ode2dsystem.py
launch.py
palette.py
miind_settings
)

set( PYTHON_SCRIPTS_API
miind_api/Density.py
miind_api/miindcli.py
miind_api/Marginal.py
miind_api/MiindSimulation.py
miind_api/__init__.py
miind_api/tools_lost.py
miind_api/MeshTools.py
miind_api/tools.py
miind_api/LifMeshGenerator.py
miind_api/QifMeshGenerator.py
miind_api/Result.py
)

set( PYTHON_SCRIPTS_XML
xml/duffin.xml
xml/miind.xml
xml/response.xml
xml/twopop.xml
xml/wilsoncowan.xml
)

set( PYTHON_SCRIPTS_MIINDIO
miindio.py
miind.py
submit.py
)

install( FILES ${PYTHON_SCRIPTS}
    DESTINATION share/miind/python )
install( FILES ${PYTHON_SCRIPTS_API}
    DESTINATION share/miind/python/miind_api )
install( FILES ${PYTHON_SCRIPTS_XML}
    DESTINATION share/miind/python/xml )
		install( FILES ${PYTHON_SCRIPTS_MIINDIO}
		    DESTINATION share/miind/python/
				PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE )
