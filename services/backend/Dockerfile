###################################################
# Stage 1 - docker container to build ensembl-vep #
###################################################
FROM ubuntu:22.04 AS builder

# Update aptitude and install some required packages
# a lot of them are required for Bio::DB::BigFile
RUN apt update
RUN apt full-upgrade -y
RUN apt install -y build-essential
RUN apt install -y git
RUN apt install -y libpng-dev
RUN apt install -y zlib1g-dev
RUN apt install -y libbz2-dev
RUN apt install -y liblzma-dev
RUN apt install -y perl
RUN apt install -y perl-base
RUN apt install -y unzip
RUN apt install -y wget

# Setup VEP environment
ENV OPT /opt/vep
ENV OPT_SRC $OPT/src
ENV HTSLIB_DIR $OPT_SRC/htslib
ARG ENSEMBL_VEP_BRANCH
ENV BRANCH ${ENSEMBL_VEP_BRANCH}
ARG ENSEMBL_VEP_MAIN_RELEASE_BRANCH
ENV MAIN_RELEASE_BRANCH ${ENSEMBL_VEP_MAIN_RELEASE_BRANCH}

# Working directory
WORKDIR $OPT_SRC


# Clone/download repositories/libraries

# Get ensembl cpanfile in order to get the list of the required Perl libraries
RUN wget -q "https://raw.githubusercontent.com/Ensembl/ensembl/$MAIN_RELEASE_BRANCH/cpanfile" -O "ensembl_cpanfile"

# Clone ensembl-vep git repository
RUN git clone --branch $BRANCH --depth 1 https://github.com/Ensembl/ensembl-vep.git
RUN chmod u+x ensembl-vep/*.pl

# Clone ensembl-variation git repository and compile C code
RUN git clone --branch $MAIN_RELEASE_BRANCH --depth 1 https://github.com/Ensembl/ensembl-variation.git
RUN mkdir var_c_code
RUN cp ensembl-variation/C_code/*.c ensembl-variation/C_code/Makefile var_c_code/
RUN rm -rf ensembl-variation
RUN chmod u+x var_c_code/*

# Clone bioperl-ext git repository - used by Haplosaurus
RUN git clone --depth 1 https://github.com/bioperl/bioperl-ext.git

# Download ensembl-xs - it contains compiled versions of certain key subroutines used in VEP
RUN wget https://github.com/Ensembl/ensembl-xs/archive/2.3.2.zip -O ensembl-xs.zip
RUN unzip -q ensembl-xs.zip
RUN mv ensembl-xs-2.3.2 ensembl-xs
RUN rm -rf ensembl-xs.zip

# Clone/Download other repositories: bioperl-live is needed so the cpanm dependencies installation from the ensembl-vep/cpanfile file takes less disk space
RUN ensembl-vep/travisci/get_dependencies.sh

# Only keep the bioperl-live "Bio" library
RUN mv bioperl-live bioperl-live_bak
RUN mkdir bioperl-live
RUN mv bioperl-live_bak/Bio bioperl-live/
RUN rm -rf bioperl-live_bak

## A lot of cleanup on the imported libraries, in order to reduce the docker image ##
RUN rm -rf Bio-HTS/.??* Bio-HTS/Changes Bio-HTS/DISCLAIMER Bio-HTS/MANIFEST* Bio-HTS/README Bio-HTS/scripts Bio-HTS/t Bio-HTS/travisci \
    bioperl-ext/.??* bioperl-ext/Bio/SeqIO bioperl-ext/Bio/Tools bioperl-ext/Makefile.PL bioperl-ext/README* bioperl-ext/t bioperl-ext/examples \
    ensembl-vep/.??* ensembl-vep/docker \
    ensembl-xs/.??* ensembl-xs/TODO ensembl-xs/Changes ensembl-xs/INSTALL ensembl-xs/MANIFEST ensembl-xs/README ensembl-xs/t ensembl-xs/travisci \
    htslib/.??* htslib/INSTALL htslib/NEWS htslib/README* htslib/test

# Only keep needed kent-335_base libraries for VEP - used by Bio::DB::BigFile (bigWig parsing)
RUN mv kent-335_base kent-335_base_bak
RUN mkdir -p kent-335_base/src
RUN cp -R kent-335_base_bak/src/lib kent-335_base_bak/src/inc kent-335_base_bak/src/jkOwnLib kent-335_base/src/
RUN cp kent-335_base_bak/src/*.sh kent-335_base/src/
RUN rm -rf kent-335_base_bak

# Setup bioperl-ext
WORKDIR bioperl-ext/Bio/Ext/Align/
RUN perl -pi -e"s|(cd libs.+)CFLAGS=\\\'|\$1CFLAGS=\\\'-fPIC |" Makefile.PL

# Install htslib binaries (for 'bgzip' and 'tabix')
# htslib requires the packages 'zlib1g-dev', 'libbz2-dev' and 'liblzma-dev'
WORKDIR $HTSLIB_DIR
RUN make install
RUN rm -f Makefile *.c

# Compile Variation LD C scripts
WORKDIR $OPT_SRC/var_c_code
RUN make
RUN rm -f Makefile *.c


###################################################
# Stage 2 - docker container to build ensembl-vep #
###################################################
FROM ubuntu:22.04

# Update aptitude and install some required packages
# a lot of them are required for Bio::DB::BigFile
RUN apt update
RUN apt full-upgrade -y
RUN apt install -y build-essential
RUN apt install -y cpanminus
RUN apt install -y curl
RUN apt install -y libmysqlclient-dev
RUN apt install -y libpng-dev
RUN apt install -y libssl-dev
RUN apt install -y zlib1g-dev
RUN apt install -y libbz2-dev
RUN apt install -y liblzma-dev
RUN apt install -y locales
RUN apt install -y openssl
RUN apt install -y perl
RUN apt install -y perl-base
RUN apt install -y unzip
RUN apt install -y vim

# Setup VEP environment
ENV OPT /opt/vep
ENV OPT_SRC $OPT/src
ENV PERL5LIB_TMP $PERL5LIB:$OPT_SRC/ensembl-vep:$OPT_SRC/ensembl-vep/modules
ENV PERL5LIB $PERL5LIB_TMP:$OPT_SRC/bioperl-live
ENV KENT_SRC $OPT/src/kent-335_base/src
ENV HTSLIB_DIR $OPT_SRC/htslib
ENV MACHTYPE x86_64
ENV DEPS $OPT_SRC
ENV PATH $OPT_SRC/ensembl-vep:$OPT_SRC/var_c_code:$PATH
ENV LANG_VAR en_US.UTF-8

# Create vep user
RUN useradd -r -m -U -d "$OPT" -s /bin/bash -c "VEP User" -p '' vep
RUN usermod -a -G sudo vep
RUN mkdir -p $OPT_SRC
USER vep

# Copy downloaded libraries (stage 1) to this image (stage 2)
COPY --chown=vep:vep --from=builder $OPT_SRC $OPT_SRC

# Change user to root for the following complilations/installations
USER root

# Install bioperl-ext, faster alignments for haplo (XS-based BioPerl extensions to C libraries)
WORKDIR $OPT_SRC/bioperl-ext/Bio/Ext/Align/
RUN perl Makefile.PL
RUN make
RUN make install
RUN rm -f Makefile*

# Install ensembl-xs, faster run using re-implementation in C of some of the Perl subroutines
RUN cpanm Test::Deep
RUN cpanm Test::LeakTrace
WORKDIR $OPT_SRC/ensembl-xs
RUN perl Makefile.PL
RUN make
RUN make install
RUN rm -f Makefile* cpanfile


WORKDIR $OPT_SRC

# Install/compile more libraries
RUN ensembl-vep/travisci/build_c.sh

# Remove unused Bio-DB-HTS files
RUN rm -rf Bio-HTS/cpanfile Bio-HTS/Build.PL Bio-HTS/Build Bio-HTS/_build Bio-HTS/INSTALL.pl

# Install ensembl perl dependencies (cpanm)
RUN cpanm --installdeps --with-recommends --notest --cpanfile ensembl_cpanfile .
RUN cpanm --installdeps --with-recommends --notest --cpanfile ensembl-vep/cpanfile .

# Delete bioperl and cpanfiles after the cpanm installs as bioperl will be reinstalled by the INSTALL.pl script
RUN rm -rf bioperl-live ensembl_cpanfile ensembl-vep/cpanfile

# Configure "locale", see https://github.com/rocker-org/rocker/issues/19
RUN echo "$LANG_VAR UTF-8" >> /etc/locale.gen
RUN locale-gen en_US.utf8
RUN /usr/sbin/update-locale LANG=$LANG_VAR

# Copy htslib executables. It also requires the packages 'zlib1g-dev', 'libbz2-dev' and 'liblzma-dev'
RUN cp $HTSLIB_DIR/bgzip $HTSLIB_DIR/tabix $HTSLIB_DIR/htsfile /usr/local/bin/

ENV LC_ALL $LANG_VAR
ENV LANG $LANG_VAR

# Switch back to vep user
USER vep
ENV PERL5LIB $PERL5LIB_TMP

# Final steps
WORKDIR $OPT_SRC/ensembl-vep
# Update bash profile
RUN echo >> $OPT/.profile
RUN echo PATH=$PATH:\$PATH >> $OPT/.profile
RUN echo export PATH >> $OPT/.profile

# Run INSTALL.pl and remove the ensemb-vep tests and travis
RUN ./INSTALL.pl -a a -l -n
RUN rm -rf t travisci .travis.yml

###################################################
# ensembl-vep is built!                           #
###################################################


# Switch back to root user
USER root

# Python install
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHON_VERSION 3.10
ENV PYTHONIOENCODING UTF-8
RUN apt install -y python3.10-minimal python3.10-venv python3-venv

# VT install
WORKDIR /opt
RUN apt install -y git
RUN git clone https://github.com/atks/vt.git
WORKDIR /opt/vt
ARG VT_BRANCH
RUN git checkout ${VT_BRANCH}
RUN apt install -y build-essential automake libz-dev
RUN make
ENV PATH "/opt/vt:${PATH}"

# Create default user
ARG USER_NAME docker_user
ARG USER_UID 1000
ARG USER_GID 1000
RUN groupadd ${USER_NAME} --non-unique --gid ${USER_GID}
RUN useradd ${USER_NAME} --non-unique --uid ${USER_UID} --gid ${USER_GID} --create-home --shell /bin/bash

# Add defaut user to vep group
ENV PATH $OPT_SRC/ensembl-vep:$OPT_SRC/var_c_code:$PATH
RUN usermod -a -G vep ${USER_NAME}

# Install usefull tools
RUN apt install -y netcat
RUN apt install -y gettext
RUN apt install -y wget

# Create required directories
RUN mkdir -p /code/services/backend
RUN mkdir /code/services/backend/.tox
RUN mkdir /code/services/backend/biodb
RUN mkdir /code/services/backend/media
RUN mkdir /code/services/backend/static
RUN mkdir /code/services/backend/venv
RUN chown -R ${USER_UID}:${USER_GID} /code

# Define environment variables
ENV PYTHONPATH $PATHONPATH:/code/lib

# Copy source code
WORKDIR /code
COPY . .
RUN chown -R ${USER_UID}:${USER_GID} /code

# App install
WORKDIR /code/services/backend
USER ${USER_NAME}
RUN make venv
RUN make install

# Change directory
WORKDIR /code
