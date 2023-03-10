# poreblazer_docker
 Instructions to build a Docker container for automated poreblazer calculations

# PoreBlazer Docker

This container houses the executable code for [PoreBlazer](https://github.com/SarkisovGitHub/PoreBlazer), a general-purpose simulation program for analysing molecuklar geometry of porous solids.  Further information on DL_MONTE can be found [here](https://pubs.acs.org/doi/10.1021/acs.chemmater.0c03575).

## Getting Started

These instructions will cover usage information and for the docker container 

### Prerequisites

In order to run this container you'll need docker installed.

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)

### Usage

The container has several pre-formatted python scripts to run poreblazer simulations when provided with a well-formatted .cif file of a molecular crystal. The container also contains a couple of example .cif files in the `/run/test_io/` directory for debugging/demonstration purposes.

To start the docker image, use the following command to instantiate a container of poreblazer. File transfer from a local disc can either be done by mounting a [volume](https://docs.docker.com/storage/volumes/) or using the `docker cp` command.

```
docker run --name pbtest -it jrhmanning/poreblazer:latest bash
```

Once instantiated, preprocess the .cif file using `poreblazer_preprocess.py`. An example for the test file Cu_BTC.cif is provided below:

```
python poreblazer_preprocess.py -i test_io/ -o data_io/ -f Cu_BTC --FrameworkSource 'local' --FrameworkFolder test_io/
```

PoreBlazer itself can be run using the python script `poreblazer_run.py`:

```
python poreblazer_run.py -f Cu_BTC -i data_io/ -o data_io/
```

From here, several output files are generated in `/run/data_io/summary.tgz`. Key takeaways can be generated by running `poreblazer.postprocess.py`:

```
python poreblazer_postprocess.py -f Cu_BTC -i data_io/ -o data_io/
```

This produces the file `/run/data_io/geometricProperties.json` which can then be coped across using `docker cp` or using volumes.

#### Script arguments

File input/output can be controlled using argument parsing inside the various python scripts to control or amend parameters. These should be uniform across all simulation scripts included.

* `InputFolder`
  * The input directory containing your input `.cif` file
* `OutputFolder`
  * The output directory whee your simulation outputs will be located. 
* `FrameworkName`
  * The name of your `.cif` file (without the file type, e.g. `Cu_BTC`, not `Cu_BTC.cif`)
  
## Built With

* PoreBlazer 4.0
* [ase](https://wiki.fysik.dtu.dk/ase/)


## Find Us

* [Github](https://github.com/SarkisovGitHub/PoreBlazer)

## License

This project is licensed under the BSD 3-clause License - see the LICENSE.md file for details.


