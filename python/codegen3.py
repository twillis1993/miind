import os
import sys
import include
import algorithms
import nodes
import connections
import reporting
import simulation
import variables
import xml.etree.ElementTree as ET
import argparse
import directories3

XML_EXTENSION = '.xml'

# Nothing too fancy for the weight type

WEIGHTTYPES = ['double', 'DelayedConnection']

def generate_preamble(outfile):
    outfile.write('//Machine-generated by miind.py. Edit at your own risk.\n\n')
    for inc in include.includes:
        outfile.write(inc +'\n')

    return

def define_network_type(outfile, type):
    if type ==  "DelayedConnection":
        s = "MPILib::" + type
    else:
        s = "double"
    return 'typedef MPILib::MPINetwork<' + s + ', MPILib::utilities::CircularDistribution> Network;\n'

def generate_closing(outfile, steps, t_step, weighttype):
    outfile.write('\tnetwork.configureSimulation(par_run);\n')

    if weighttype.text ==  "DelayedConnection":
        type = "MPILib::" + weighttype.text
    else:
        type = "double"

    outfile.write('\tTwoDLib::Display::getInstance()->animate(true, display_nodes,' + t_step + ');\n')
    outfile.write('\tnetwork.startSimulation();\n')
    outfile.write('\tMPILib::utilities::ProgressBar *pb = new MPILib::utilities::ProgressBar(' + steps + ');\n')
    outfile.write('\tlong count = 0;\n')
    outfile.write('\twhile(count < ' + steps + ') {\n')
    outfile.write('\t\tnetwork.evolveSingleStep(std::vector<MPILib::ActivityType>());\n')
    outfile.write('\t\tnetwork.reportNodeActivities(rate_nodes);\n')
    outfile.write('\t\tTwoDLib::Display::getInstance()->updateDisplay(count);\n')
    outfile.write('\t\tTwoDLib::GridReport<'+type+'>::getInstance()->reportDensity(density_nodes,density_node_start_times,density_node_end_times,density_node_intervals,(count * ' + t_step + '));\n')
    outfile.write('\t\t(*pb)++;\n')
    outfile.write('\t\tcount++;\n')
    outfile.write('\t}\n')
    outfile.write('\tnetwork.endSimulation();\n')

    outfile.write('\t} catch(std::exception& exc){\n')
    outfile.write('\t\tstd::cout << exc.what() << std::endl;\n')

    outfile.write('#ifdef ENABLE_MPI\n')
    outfile.write('\t//Abort the MPI environment in the correct way :\n')
    outfile.write('\tenv.abort(1);\n')
    outfile.write('#endif\n')
    outfile.write('\t}\n\n')

    outfile.write('\tMPILib::utilities::MPIProxy().barrier();\n')
    outfile.write('\tt.stop();\n')
    outfile.write('\tif (MPILib::utilities::MPIProxy().getRank() == 0) {\n')
    outfile.write('\n\t\tstd::cout << \"Overall time spend\\n\";\n')
    outfile.write('\t\tt.report();\n')
    outfile.write('\t}\n')

    outfile.write('\treturn 0;\n}\n')

    for t in  algorithms.RATEFUNCTIONS:
        outfile.write(t)

    return

def parse_xml(infile, outfile):
    tree=ET.fromstring(infile.read())
    m=tree.find('WeightType')
    s = m.text
    return define_network_type(outfile,s), tree

def generate_opening(outfile):
    outfile.write('int main(int argc, char *argv[]){\n\tNetwork network;\n')
    outfile.write('\tboost::timer::auto_cpu_timer t;\n\n')
    outfile.write('#ifdef ENABLE_MPI\n')
    outfile.write('\t// initialise the mpi environment this cannot be forwarded to a class\n')
    outfile.write('\tboost::mpi::environment env(argc, argv);\n')
    outfile.write('#endif\n\n')
    outfile.write('\ttry {')

def matrix_transform_name(fn):
    '''Identifies matrix transform files mentioned in an XML file. For example used in placing the right model file in
    the same directory as an XML file.'''
    infile = open(fn)
    tree=ET.fromstring(infile.read())
    ma = tree.findall('Algorithms/Algorithm')

    tmatnames = []
    for a in ma:
        if a.attrib['type'] in ['GridAlgorithm','GridAlgorithmGroup']:
            tmatnames.append(a.attrib['transformfile'])
    return tmatnames

def model_name(fn):
    '''Identifies model files mentioned in an XML file. For example used in placing the right model file in
    the same directory as an XML file.'''
    infile = open(fn)
    tree=ET.fromstring(infile.read())
    ma = tree.findall('Algorithms/Algorithm')

    modelnames = []
    for a in ma:
        if a.attrib['type'] in ['GridAlgorithm','GridAlgorithmGroup','MeshAlgorithm','MeshAlgorithmGroup']:
            modelnames.append(a.attrib['modelfile'])
    return modelnames

def matrix_names(fn):
    '''Find the file names of all MatrixFiles, mentioned in an XML file.'''
    infile = open(fn)
    tree=ET.fromstring(infile.read())
    ma = tree.findall('Algorithms/Algorithm/MatrixFile')
    matrixnames = []
    for a in ma:
        matrixnames.append(a.text)
    return matrixnames

def node_name_to_node_id(nodes):
     '''Create a map from name to NodeId from node elements. Return this map.'''
     d ={}
     for i,node in enumerate(nodes):
          d[node.attrib['name']] = i
     return d

def generate_outputfile(infile, outfile, enable_root):
    generate_preamble(outfile)
    nettype, tree = parse_xml(infile,outfile)
    outfile.write(nettype)
    outfile.write('\t// defining variables\n') # whatever variables are use are global
    variable_list = tree.findall('Variable')
    variables.parse_variables(variable_list,outfile)
    algies = tree.findall('Algorithms')
    if len(algies) != 1:
        raise ValueError

    alg_list = algies[0].findall('Algorithm')
    weighttype = tree.find('WeightType')
    generate_opening(outfile)
    outfile.write('\t// generating algorithms\n')
    algorithms.parse_algorithms(alg_list,weighttype,outfile)
    node_list = tree.findall('Nodes/Node')
    outfile.write('\t// generating nodes\n')
    nodes.parse_nodes(node_list,weighttype,outfile)
    outfile.write('\t// generating connections\n')
    connection_list = tree.findall('Connections/Connection')
    connections.parse_connections(connection_list,weighttype,outfile)
    outfile.write('\t// generation simulation parameter\n')
    simhand = tree.find('SimulationIO')
    simulation.parse_simulation(simhand,outfile,enable_root)
    simpar = tree.find('SimulationRunParameter')
    simulation.parse_parameter(simpar,outfile)

    nodemap = node_name_to_node_id(node_list)
    outfile.write(reporting.define_display_nodes(tree,nodemap))
    outfile.write(reporting.define_rate_nodes(tree,nodemap))
    outfile.write(reporting.define_density_nodes(tree,nodemap))

    t_begin = tree.find('SimulationRunParameter/t_begin')
    t_end   = tree.find('SimulationRunParameter/t_end')
    t_step = tree.find('SimulationRunParameter/t_step')

    generate_closing(outfile, '(' + t_end.text + ' - ' + t_begin.text + ') / ' + t_step.text , t_step.text, weighttype)

    algorithms.reset_algorithms()
    nodes.reset_nodes()
