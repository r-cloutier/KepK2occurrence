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
	ignore = ['fname','Nstars','N_hasGAIA','N_isMdwarf','N_iscool']
        for a in dir(self):

            # skip hidden variables
            if (a[0] != '_') and (a not in ignore):
                setattr(self, a, np.append(getattr(self,a), getattr(d,a)))
                
    # save the compiled object
    assert type(self.fname) == str
    self._pickleobject()

    # save to a file for access by ORION
    hdr='EPIC,ra_deg,dec_deg,GBPmag,e_GBPmag,GRPmag,e_GRPmag,Kepmag,Jmag,e_Jmag,Hmag,e_Hmag,Kmag,e_Kmag,parallax_mas,e_parallax,dist_pc,ehi_dist,elo_dist,mu,ehi_mu,elo_mu,AK,e_AK,MK,ehi_MK,elo_MK,Rs_RSun,ehi_Rs,elo_Rs,Teff_K,ehi_Teff,elo_Teff,Ms_MSun,ehi_Ms,elo_Ms,logg_dex,ehi_logg,elo_logg'
    g = (np.isfinite(self.MKs)) & (np.isfinite(self.Rss2)) & (np.isfinite(self.Teffs2)) & (np.isfinite(self.Mss2))
    outarr = np.array([self.EPICnums,self.ras,self.decs,self.GBPmags,self.eGBPmags,self.GRPmags,self.eGRPmags,np.repeat(np.nan,self.Nstars),self.Jmags,
                       self.e_Jmags,self.Hmags,self.e_Hmags,self.Kmags,self.e_Kmags,self.pars,self.epars,self.dists,self.ehidists,self.elodists,
                       self.mus,self.ehimus,self.elomus,self.AKs,self.eAKs,self.MKs,self.ehi_MKs,self.elo_MKs,self.Rss2,self.ehi_Rss2,self.elo_Rss2,
                       self.Teffs2,self.ehi_Teffs2,self.elo_Teffs2,self.Mss2,self.ehi_Mss2,self.elo_Mss2,self.loggs2,self.ehi_loggs2,self.elo_loggs2])
    np.savetxt('../../GAIAMdwarfs/GAIAMdwarfs/input_data/K2targets/K2lowmassstars_sens.csv', outarr[:,g].T, delimiter=',', fmt='%.8e', header=hdr)


if __name__ == '__main__':
    prefix = 'Results/K2lowmassstars_all_GAIA'
    compile_results(prefix)
