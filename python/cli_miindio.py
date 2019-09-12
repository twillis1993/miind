#!/usr/bin/env python3

import argparse
import codegen3
import sys
import os
import os.path as op
import miind_api as api
import matplotlib.pyplot as plt
import directories3

def configureArgumentParser():
    """
    """
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()
    defTimestep = 0.0001
    defRevPotential = -65.0
    defThrPotential = -50.0
    defMinPotential = -80.0
    defTau = 0.01
    defNGrid = 300
    defVEfficacy = 0.1
    defNoOfPoints = 100
    defWEfficacy = 0.0
    defWResetShift = 0.0
    defIsAreaCalc = False

    generateLifMeshSP = subparsers.add_parser("generate-lif-mesh", help="Generates lif mesh using the LifMeshGenerator.py script")
    generateLifMeshSP.add_argument('name', type=str)
    generateLifMeshSP.add_argument('--timestep', type=float, default=defTimestep)
    generateLifMeshSP.add_argument('--reversalPotential', type=float, default=defRevPotential)
    generateLifMeshSP.add_argument('--thresholdPotential', type=float, default=defThrPotential)
    generateLifMeshSP.add_argument('--minPotential', type=float, default=defMinPotential)
    generateLifMeshSP.add_argument('--tau', type=float, default=defTau)
    generateLifMeshSP.add_argument('--nGrid', type=int, default=defNGrid)
    generateLifMeshSP.set_defaults(func=cli_generateLifMesh)

    generateEmptyFidSP = subparsers.add_parser("generate-empty-fid", help="Generates empty fid file")
    generateEmptyFidSP.add_argument('name', type=str)
    generateEmptyFidSP.set_defaults(func=cli_generateEmptyFid)

    generateModelSP = subparsers.add_parser("generate-model", help="Generates model file")
    generateModelSP.add_argument('name', type=str)
    generateModelSP.add_argument('reversalPotential', type=float)
    generateModelSP.add_argument('thresholdPotential', type=float)
    generateModelSP.set_defaults(func=cli_generateModel)

    generateMatrixSP = subparsers.add_parser("generate-matrix", help="Generates mat file")
    generateMatrixSP.add_argument('name', type=str)
    generateMatrixSP.add_argument('--jumpFile', type=str)
    generateMatrixSP.add_argument('--vEfficacy', type=float, default=defVEfficacy)
    generateMatrixSP.add_argument('--noOfPoints', type=int, default=defNoOfPoints)
    generateMatrixSP.add_argument('--wEfficacy', type=float, default=defWEfficacy)
    generateMatrixSP.add_argument('--wResetShift', type=float, default=defWResetShift)
    generateMatrixSP.add_argument('--isAreaCalc', type=bool, default=defIsAreaCalc)
    generateMatrixSP.set_defaults(func=cli_generateMatrix)	

    generateAllFilesSP = subparsers.add_parser("generate-all-files", help="Generates all files")
    generateAllFilesSP.add_argument('name', type=str)
    generateAllFilesSP.add_argument('--timestep', type=float, default=defTimestep)
    generateAllFilesSP.add_argument('--reversalPotential', type=float, default=defRevPotential)
    generateAllFilesSP.add_argument('--thresholdPotential', type=float, default=defThrPotential)
    generateAllFilesSP.add_argument('--minPotential', type=float, default=defMinPotential)
    generateAllFilesSP.add_argument('--tau', type=float, default=defTau)
    generateAllFilesSP.add_argument('--nGrid', type=int, default=defNGrid)
    generateAllFilesSP.add_argument('--vEfficacy', type=float, default=defVEfficacy)
    generateAllFilesSP.add_argument('--noOfPoints', type=int, default=defNoOfPoints)
    generateAllFilesSP.add_argument('--wEfficacy', type=float, default=defWEfficacy)
    generateAllFilesSP.add_argument('--wResetShift', type=float, default=defWResetShift)
    generateAllFilesSP.add_argument('--isAreaCalc', type=bool, default=defIsAreaCalc)
    generateAllFilesSP.set_defaults(func=cli_generateAllFiles)

    generateDrawMeshSP = subparsers.add_parser("draw-mesh", help="Draws mesh")
    generateDrawMeshSP.add_argument('filename', type=str)
    generateDrawMeshSP.set_defaults(func=cli_drawMesh)

    #simSP = subparsers.add_parser("sim", help="Sets specified XML file as current simulation")
    #simSP.add_argument("filename", type=str)			
    #simSP.set_defaults(func=cli_sim)

    simSubmitRunSP = subparsers.add_parser("sim-submit-run", help="Submits and runs simulation")
    simSubmitRunSP.add_argument("filename", type=str)			
    simSubmitRunSP.add_argument('submitName',type=str,default=None)
    simSubmitRunSP.set_defaults(func=cli_simSubmitRun)

    return parser

def cli_generateLifMesh(args):	 
    gen = api.LifMeshGenerator(args.name, V_rest=args.reversalPotential, V_threshold=args.thresholdPotential, V_min=args.minPotential, dt=args.timestep, N_grid=args.nGrid, tau=args.tau)

    gen.generateLifMesh()

    gen.generateLifStationary()

    gen.generateLifReversal()

def cli_generateEmptyFid(args):
    api.MeshTools.generateStubFidFile(args.name)

def cli_generateModel(args):
    api.MeshTools.buildModelFileFromMesh(args.name, args.reversalPotential, args.thresholdPotential)

def cli_generateMatrix(args):
    try:
        api.MeshTools.buildMatrixFileFromModel(args.name, args.vEfficacy, fidfile=".".join([args.name, "fid"]), num_mc_points=args.noOfPoints, jump_file=args.jumpFile)
    except AttributeError:
        api.MeshTools.buildMatrixFileFromModel(args.name, args.vEfficacy, fidfile=".".join([args.name, "fid"]), num_mc_points=args.noOfPoints, spike_shift_w=args.wEfficacy, reset_shift_w=args.wResetShift, use_area_calculation=args.isAreaCalc)

def cli_generateAllFiles(args):
    cli_generateLifMesh(args)
    cli_generateEmptyFid(args)	
    cli_generateModel(args)
    cli_generateMatrix(args)

def cli_drawMesh(args):	
    api.MeshTools.plotMesh(args.filename)

class SimWrapper:
    """Just a lazy port of Hugh's code from miindio.py (like the rest of this program, really)
    """
    def __init__(self, args):
        self.current_sim = api.MiindSimulation(args.filename, args.submitName)
        self.cwdfilename = 'miind_cwd'
        self.settingsfilename = op.expanduser('~/.miind_settings')
        self.miind_cmake_cache = op.join(directories3.miind_root(), 'build/CMakeCache.txt')
        self.debug = False

        self.settings = {}
        self.settings['mpi_enabled'] = False
        self.settings['openmp_enabled'] = False
        self.settings['root_enabled'] = False
        self.settings['cuda_enabled'] = False

        self.cwd_settings = {}
        self.cwd_settings['sim'] = self.current_sim.xml_fname
        self.cwd_settings['sim_project'] = self.current_sim.submit_name


        self.flags_set = [False,False,False,False]
        if op.exists(self.miind_cmake_cache):
                with open(self.miind_cmake_cache, 'r') as cachefile:
                        for line in cachefile:
                                tokens = line.strip().split('=')
                                if(tokens[0] == 'ENABLE_CUDA:BOOL'):
                                        self.settings['cuda_enabled'] = (tokens[1] == 'ON')
                                        self.flags_set[0] = True
                                if(tokens[0] == 'ENABLE_MPI:BOOL'):
                                        self.settings['mpi_enabled'] = (tokens[1] == 'ON')
                                        self.flags_set[1] = True
                                if(tokens[0] == 'ENABLE_OPENMP:BOOL'):
                                        self.settings['openmp_enabled'] = (tokens[1] == 'ON')
                                        self.flags_set[2] = True
                                if(tokens[0] == 'ENABLE_ROOT:BOOL'):
                                        self.settings['root_enabled'] = (tokens[1] == 'ON')
                                        self.flags_set[3] = True

        if(not op.exists(self.miind_cmake_cache) or not all(self.flags_set)):
                if not op.exists(self.settingsfilename):
                        print('CMakeCache.txt in MIIND_ROOT/Build directory not found. Fall back to user settings file...')
                        print('Settings file ('+ self.settingsfilename +') not found. MPI, OPENMP, ROOT and CUDA enabled by default.')

                        with open(self.settingsfilename, 'w') as settingsfile:
                                self.settings['mpi_enabled'] = True
                                self.settings['openmp_enabled'] = True
                                self.settings['root_enabled'] = True
                                self.settings['cuda_enabled'] = True
                                for k,v in self.settings.items():
                                        settingsfile.write(k + '=' + str(v) + '\n')
                else:
                        with open(self.settingsfilename, 'r') as settingsfile:
                                for line in settingsfile:
                                        tokens = line.split('=')
                                        self.settings[tokens[0].strip()] = (tokens[1].strip() == 'True')

        """
        with open(self.cwdfilename, 'w') as cwdsettingsfile:
                for k,v in self.cwd_settings.items():
                        cwdsettingsfile.write(k + '=' + str(v) + '\n')

        if not op.exists(self.cwdfilename):
                with open(self.cwdfilename, 'w') as cwdsettingsfile:
                        for k,v in self.cwd_settings.items():
                                cwdsettingsfile.write(k + '=' + str(v) + '\n')
        else: 
                # If miind_cwd already exists, SimWrapper is configured with settings specified therein
                # TODO If no lif.xml specified, we should read miind_cwd, otherwise we should overwrite it
                with open(self.cwdfilename, 'r') as cwdsettingsfile:
                        for line in cwdsettingsfile:
                                tokens = line.split('=')
                                # Expect sim to be a filename, otherwise expect a boolean
                                if tokens[0].strip() == 'sim':
                                        if tokens[1].strip() == 'NOT_SET':
                                                self.cwd_settings['sim'] = None
                                        else:
                                                self.cwd_settings['sim'] = tokens[1].strip()
                                elif tokens[0].strip() == 'sim_project':
                                        if tokens[1].strip() == 'NOT_SET':
                                                self.cwd_settings['sim_project'] = None
                                        else:
                                              self.cwd_settings['sim_project'] = tokens[1].strip()
        """

    def simSubmitRun(self, args):
            with open(self.cwdfilename, 'w') as settingsfile:
                    for k,v in self.cwd_settings.items():
                            settingsfile.write(k + '=' + str(v) + '\n')

            self.current_sim.submit(True,
                            self.settings['mpi_enabled'],
                            self.settings['openmp_enabled'],
                            self.settings['root_enabled'],
                            self.settings['cuda_enabled'])
        #   self.current_sim.run()	
				
def cli_simSubmitRun(args):
    sim = SimWrapper(args)
    sim.simSubmitRun(args)

if __name__ == "__main__":	
    parser = configureArgumentParser()
    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        parser.error("Too few arguments")
