import mesh
import writemesh
import numpy as np
import uuid
import sys
import os

class MatsoMeshGenerator:
    def __init__(self, basename, tauR, tauU, timestep, duration, noOfBins=100):
        self.basename = basename
        self.tauR = tauR
        self.tauU = tauU
        self.dt = timestep
        self.t_end = duration
        self.noOfBins = noOfBins

    def generateMeshFile(self):
        times = np.arange(0., self.t_end+self.dt, self.dt) 
        rStart = np.linspace(0., 1., self.noOfBins)
        uStart = 1.

        with open('.'.join([self.basename, "mesh"]), 'w') as meshFile:
            meshFile.write('irrelevant\n')
            meshFile.write(str(self.dt)+'\n')

            for r in rStart[::-1]:
                rs, us = self.generateStationaryPoint(r, uStart, times)
                for el in zip(rs, us):
                    meshFile.write(str(el[0]) +'\t')
                meshFile.write('\n')
                for el in zip(rs, us):
                    meshFile.write(str(el[1]) +'\t')
                meshFile.write('\n')
            meshFile.write('closed\n')

            r_start_2 = 0
            u_start_2 = np.linspace(0.,1., self.noOfBins)
            for u in u_start_2[::-1]:
                rs, us  = self.generateStationaryPoint(r_start_2, u, times)
                for el in zip(rs, us):
                    if el[1] <= 1.:
                        meshFile.write(str(el[0]) +'\t')
                meshFile.write('\n')
                for el in zip(rs, us):
                    if el[1] <=1.:
                        meshFile.write(str(el[1]) +'\t')
                meshFile.write('\n')
            meshFile.write('closed\n')
            meshFile.write('end\n')

        self.mesh = mesh.Mesh('.'.join([self.basename, "mesh"]))

    def generateStationaryFile(self): 
        dim_r = np.exp(-self.t_end/self.tauR)
        dim_u = np.exp(-self.t_end/self.tauU)

        if dim_r < dim_u:
            dim = dim_r
        else:
            dim = dim_u
            
        with open('.'.join([self.basename, "stat"]),'w') as statFile:
            statFile.write('<Stationary>\n')
            statFile.write('<Quadrilateral>')
            statFile.write('<vline>')
            statFile.write(' '.join([str(1.-dim), str(1.-dim), str(1.), str(1.)]))
            statFile.write('</vline>')
            statFile.write('<wline>')
            statFile.write(' '.join([str(0.), str(dim), str(dim), str(0.)]))
            statFile.write('</wline>')
            statFile.write('</Quadrilateral>\n')
            statFile.write('</Stationary>')

    def generateReversalFile(self):
        with open('.'.join([self.basename, "rev"]),'w') as revFile:
            revFile.write('<Mapping type=\"Reversal\">\n')
            for i in range(1, len(self.mesh.cells)):
                revFile.write(str(i) + ',0\t0,0\t1.0\n')
            revFile.write('</Mapping>\n')

    def generateJumpFile(self, alpha=0.1):
        with open('.'.join([self.basename+"_"+str(alpha).replace(".", "_"), 'jmp']),'w') as jumpFile:
            jumpFile.write('<Jump>\n')
            jumpFile.write('<Efficacy>' + str(alpha) +', 0.0</Efficacy>\n')
            # TODO the fix for the parsing problem is probably just to wrap the following output as a <Cell> element or whatever
            jumpFile.write('<Cell>\n')
            for i, cells in enumerate(self.mesh.cells):
                for j, cell in enumerate(cells):
                    jumpFile.write(str(i) + ',' + str(j) + '\t' + str(-cell.centroid[0]*cell.centroid[1]) + '\t' + str(alpha*(1-cell.centroid[1])) +'\n')  
            jumpFile.write('</Cell>\n')
            jumpFile.write('</Jump>')

    def generateStationaryPoint(self, rStart, uStart, times):
        rs = 1. - (1 -rStart)*np.exp(-times/self.tauR)
        us = uStart*np.exp(-times/self.tauU)    
        return rs, us

if __name__ == "__main__":
    # In the 2019 paper, (t_r = 0.1, t_u = 0.9) for facilitating synapses and (t_r = 0.9, t_u = 0.1) for depressing synapses
    # t_r == trec
    # t_u == tfac

    mmG = MatsoMeshGenerator(basename="matso", tauR=0.1, tauU=0.9, timestep=0.005, duration=1.0, noOfBins=100)
    mmG.generateMeshFile()
    mmG.generateStationaryFile()
    mmG.generateReversalFile()
    mmG.generateJumpFile()
