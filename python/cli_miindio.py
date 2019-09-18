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

    simSP = subparsers.add_parser("sim", help="Sets specified XML file as current simulation")
    simSP.add_argument("filename", type=str)			
    simSP.add_argument("submitName", type=str)			
    simSP.set_defaults(func=cli_sim)

    simSubmitSP = subparsers.add_parser("sim-submit", help="Submits simulation")
    simSubmitSP.add_argument("filename", type=str)			
    simSubmitSP.add_argument('submitName',type=str)
    simSubmitSP.set_defaults(func=cli_simSubmit)

    simSubmitRunSP = subparsers.add_parser("sim-submit-run", help="Specifies, submits, and runs simulation")
    simSubmitRunSP.add_argument("filename", type=str)			
    simSubmitRunSP.add_argument('submitName',type=str)
    simSubmitRunSP.set_defaults(func=cli_simSubmitRun)

    submitSP = subparsers.add_parser("submit", help="Submits simulation")
    submitSP.set_defaults(func=cli_submit)

    runSP = subparsers.add_parser("run", help="Runs simulation")
    runSP.set_defaults(func=cli_run)

    submitRunSP = subparsers.add_parser("submit-run", help="Submits and runs simulation")
    submitRunSP.set_defaults(func=cli_submitRun)

    generateMatsoMeshSP = subparsers.add_parser("generate-matso-mesh", help="Generates matso mesh using the MatsoMeshGenerator.py")
    generateMatsoMeshSP.add_argument("name",type=str)
    generateMatsoMeshSP.add_argument("tauR", type=float, help="Time constant for depressive effect")
    generateMatsoMeshSP.add_argument("tauU", type=float, help="Time constant for facilitating effect")
    generateMatsoMeshSP.add_argument("timestep", type=float)
    generateMatsoMeshSP.add_argument("duration", type=float)
    generateMatsoMeshSP.add_argument("alpha", nargs="+", type=float, help="Synaptic efficacy/ies for jump file generation")
    generateMatsoMeshSP.add_argument("--noOfBins", type=int, default=100)
    generateMatsoMeshSP.set_defaults(func=cli_generateMatsoMesh)

    generateDensityMovieSP = subparsers.add_parser("generate-density-movie", help="Generates density movie")
    generateDensityMovieSP.add_argument("nodeName", type=str, help="Name of simulation node for which to generate a movie")
    generateDensityMovieSP.add_argument("frameSize", type=int)
    generateDensityMovieSP.add_argument("timestep", type=float)
    generateDensityMovieSP.add_argument("movieName", type=str, help="Movie name sans extension")
    generateDensityMovieSP.set_defaults(func=cli_generateDensityMovie)

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
    # NB: vEfficacy redundant with jump file but the API method requires it
    if (hasattr(args, "jumpFile") and args.jumpFile):
        api.MeshTools.buildMatrixFileFromModel(basename=args.name, jump_file=args.jumpFile, num_mc_points=args.noOfPoints, fidfile=".".join([args.name, "fid"]), spike_shift_v=args.vEfficacy)
    else:
        api.MeshTools.buildMatrixFileFromModel(args.name, args.vEfficacy, fidfile=".".join([args.name, "fid"]), num_mc_points=args.noOfPoints, spike_shift_w=args.wEfficacy, reset_shift_w=args.wResetShift, use_area_calculation=args.isAreaCalc)

def cli_generateAllFiles(args):
    cli_generateLifMesh(args)
    cli_generateEmptyFid(args)	
    cli_generateModel(args)
    cli_generateMatrix(args)

def cli_drawMesh(args):	
    api.MeshTools.plotMesh(args.filename)

def cli_generateMatsoMesh(args):
    gen = api.MatsoMeshGenerator(basename=args.name, tauR=args.tauR, tauU=args.tauU, timestep=args.timestep, duration=args.duration, noOfBins=args.noOfBins)
    gen.generateMeshFile()
    gen.generateStationaryFile()
    gen.generateReversalFile()
    for alpha in args.alpha:
        gen.generateJumpFile(alpha)

class SimWrapper:
    """Just a lazy port of Hugh's code from miindio.py (like the rest of this program, really)
    """
    def __init__(self, args):
      self.cwdfilename = 'miind_cwd'
      settingsfilename = op.expanduser('~/.miind_settings')
      available_settingsfilename = os.path.join(directories3.miind_root(),'python','miind_settings')
      
      self.available_settings = {}
      self.available_settings['mpi_enabled'] = False
      self.available_settings['openmp_enabled'] = False
      self.available_settings['root_enabled'] = False
      self.available_settings['cuda_enabled'] = False
      self.settings = {}
      self.settings['root_enabled'] = False
      self.settings['cuda_enabled'] = False

      self.cwd_settings = {}
      self.cwd_settings['sim'] = 'NOT_SET'
      self.cwd_settings['sim_project'] = 'NOT_SET'

      if op.exists(available_settingsfilename):
          # Read available settings from MIIND installation.
          with open(available_settingsfilename, 'r') as settingsfile:
              for line in settingsfile:
                  tokens = line.split('=')
                  self.available_settings[tokens[0].strip()] = (tokens[1].strip() == 'ON')

          # Read or create settings as long as they're available in the installation.
          if not op.exists(settingsfilename):
              print('Settings file ('+ settingsfilename +') created. Using defaults from MIIND installation:')
              print('ROOT ENABLED = ' + str(self.available_settings['root_enabled']) + '')
              print('CUDA ENABLED = ' + str(self.available_settings['cuda_enabled']) + '\n')

              self.settings['root_enabled'] = self.available_settings['root_enabled']
              self.settings['cuda_enabled'] = self.available_settings['cuda_enabled']

              with open(settingsfilename, 'w') as settingsfile:
                  for k,v in self.settings.items():
                      if v:
                          settingsfile.write(k + '=ON\n')
                      else:
                          settingsfile.write(k + '=OFF\n')
          else:
              with open(settingsfilename, 'r') as settingsfile:
                  for line in settingsfile:
                      tokens = line.split('=')
                      self.settings[tokens[0].strip()] = (tokens[1].strip() == 'ON')

              # Verify settings.
              self.settings['root_enabled'] = self.available_settings['root_enabled'] and self.settings['root_enabled']
              self.settings['cuda_enabled'] = self.available_settings['cuda_enabled'] and self.settings['cuda_enabled']
      else:
          print('WARNING : MIIND installation is missing the available settings file ' +  + '. All settings switched OFF.')

          # Read or create settings as long as they're available in the installation.
          if not op.exists(settingsfilename):
              print('Settings file ('+ settingsfilename +') created. All settings disabled.\n')
              self.settings['root_enabled'] = False
              self.settings['cuda_enabled'] = False

              with open(settingsfilename, 'w') as settingsfile:
                  for k,v in self.settings.items():
                      if v:
                          settingsfile.write(k + '=ON\n')
                      else:
                          settingsfile.write(k + '=OFF\n')

          else:
              with open(settingsfilename, 'r') as settingsfile:
                  for line in settingsfile:
                      tokens = line.split('=')
                      self.settings[tokens[0].strip()] = (tokens[1].strip() == 'ON')

    def sim(self, args):
        # No settings specified and no lif.xml specified
        if not (op.exists(self.cwdfilename) or (hasattr(args, "filename") and args.filename)):
            raise Exception("No miind_cwd and no specified XML")
        # There is a specified lif.xml file and submit name, which take precedence over existing settings
        elif hasattr(args, "filename") and args.filename:
            self.current_sim = api.MiindSimulation(args.filename, args.submitName)
            self.cwd_settings['sim'] = self.current_sim.xml_fname
            self.cwd_settings['sim_project'] = self.current_sim.submit_name

            # Update settings file
            with open(self.cwdfilename, 'w') as settingsfile:
                for k,v in self.cwd_settings.items():
                    settingsfile.write(k + '=' + str(v) + '\n')
        # There is an existing cwdfile but no specified lif.xml etc.
        else:
            with open(self.cwdfilename, 'r') as cwdsettingsfile:
                for line in cwdsettingsfile:
                    tokens = line.split('=')
                    # Expect sim to be a filename, otherwise expect a boolean
                    if tokens[0].strip() == 'sim':
                        if tokens[1].strip() == 'NOT_SET':
                            raise Exception("Simulation XML not set in miind_cwd")
                        else:
                            self.cwd_settings['sim'] = tokens[1].strip()
                    elif tokens[0].strip() == 'sim_project':
                        if tokens[1].strip() == 'NOT_SET':
                            raise Exception("Project name not set in miind_cwd")
                        else:
                            self.cwd_settings['sim_project'] = tokens[1].strip()

            self.current_sim = api.MiindSimulation(self.cwd_settings['sim'], self.cwd_settings['sim_project'])

    def submit(self):
            self.current_sim.submit(True, [],
                  self.available_settings['mpi_enabled'],
                  self.available_settings['openmp_enabled'], 
                  self.settings['root_enabled'], 
                  self.settings['cuda_enabled'])

    def run(self): 
            self.current_sim.run()

def cli_sim(args):
    sim = SimWrapper(args)
    sim.sim(args)

def cli_simSubmit(args):
    sim = SimWrapper(args)
    sim.sim(args)
    sim.submit()
				
def cli_simSubmitRun(args):
    sim = SimWrapper(args)
    sim.sim(args)
    sim.submit()
    sim.run()

def cli_submit(args):
    sim = SimWrapper(args)
    sim.sim(args)
    sim.submit()

def cli_run(args):
    sim = SimWrapper(args)
    sim.sim(args)
    sim.run()

def cli_submitRun(args):
    sim = SimWrapper(args)
    sim.sim(args)
    sim.submit()
    sim.run()

def cli_generateDensityMovie(args):
    sim = SimWrapper(args)
    sim.sim(args)
    currentDensity = sim.current_sim.getDensityByNodeName(args.nodeName)
    currentDensity.generateDensityAnimation(args.movieName, 
                                            args.frameSize,
                                            True,
                                            args.timestep)

if __name__ == "__main__":	
    parser = configureArgumentParser()
    args = parser.parse_args()
    # TODO check this
    #https://stackoverflow.com/questions/48648036/python-argparse-args-has-no-attribute-func
    args.func(args)
