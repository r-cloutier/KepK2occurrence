from imports import *
from catalog_object import *


def compile_results(prefix):
    # get all objects with different indices
    fs = np.array(glob.glob('%s*'%prefix))

    # initialize all arrays
    self = loadpickle(fs[0])
    self.fname = '%sFULL'%prefix
    
    # append all results into one master object
    for i in range(1, fs.size):

        print float(i) / fs.size
        
        # load object
        d = loadpickle(fs[i])
        self.Nstars     += d.Nstars
        self.N_hasGAIA  += d.N_hasGAIA
        self.N_isMdwarf += d.N_isMdwarf
        self.N_iscool   += d.N_iscool
        
        # append values
        for a in dir(self):

            # skip hidden variables
            if (a[0] != '_') and (a != 'fname'):
                setattr(self, a, np.append(getattr(self,a), getattr(d,a)))
                
    # save the compiled object
    assert type(self.fname) == str
    self._pickleobject()


if __name__ == '__main__':
    prefix = 'Results/K2lowmassstars_all_GAIA'
    compile_results(prefix)
