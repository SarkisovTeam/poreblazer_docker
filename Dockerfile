FROM python:3.8-slim-buster
USER root
WORKDIR /run
ENV PYTHONPATH "${PYTHONPATH}:/run"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gfortran \
    make \
    unzip \
#    wget \
	git \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY Pipfile Pipfile
RUN python -m pip install --no-cache-dir --upgrade pip pipenv
RUN pipenv install --skip-lock --system --verbose && \
     pipenv --clear

# Include filetypes
# COPY runscript.sh runscript.sh
COPY UFF.atoms UFF.atoms
COPY input.dat input.dat
COPY defaults.dat defaults.dat
COPY probe_occupiable_volume.xyz probe_occupiable_volume.xyz
COPY runscript.py runscript.py
COPY poreblazer_preprocess.py poreblazer_preprocess.py
COPY poreblazer_run.py poreblazer_run.py
COPY poreblazer_postprocess.py poreblazer_postprocess.py
<<<<<<< Updated upstream
COPY copy_files.py copy_files.py
=======
>>>>>>> Stashed changes



RUN mkdir data_io

# Install Poreblazer
RUN git clone https://github.com/SarkisovGitHub/PoreBlazer.git && \
	cd PoreBlazer/src && \
	rm *.exe && \
	ls && \
	make -f Makefile_gfort poreblazer.exe && \
	mv poreblazer.exe /run && \
    rm -fr PoreBlazer && \
	mkdir /run/output
