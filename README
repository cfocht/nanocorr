# Nanocorr

This is a fork of jgurtowski's nanocorr. It makes some changes to the way that nanocorr is run to make it easier to use with Non-SGE clusters. Nanocorr can now simply be run with a simple bash loop. For example:
```bash
for file in *
  do sbatch --wrap "nanocorr $file ../4349.fasta" -J nanocorr"$file" --mem 2
done
```

Error correction for oxford nanopore reads


Requires:
        Blast to be in path
        SGE or similar scheduler

Installation:
        Clone the repository to a shared filesysem on a cluster
        
        >git clone https://github.com/cfocht/nanocorr
        >cd nanocorr        
        
        Create a virtual environment to install python dependencies

        >virtualenv nanocorr_ve
        >source nanocorr_ve/bin/activate
        
        install the following packages using pip:

            pip install git+https://github.com/cython/cython
            pip install numpy
            pip install h5py
            pip install git+https://github.com/jgurtowski/pbcore_python
            pip install git+https://github.com/jgurtowski/pbdagcon_python
            pip install git+https://github.com/jgurtowski/jbio
            pip install git+https://github.com/jgurtowski/jptools
        
        #Finally install the nanocorr package itself
        
        > python setup.py install

        
