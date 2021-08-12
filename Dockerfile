FROM kbase/sdkbase2:python
MAINTAINER Roxane Ouango

RUN \
    apt-get update && \
    apt-get -y install build-essential cmake gcc zlib1g-dev
RUN mkdir -p /kb/module
WORKDIR /kb/module
RUN git clone https://bouango@bitbucket.org/bouango/jgi-miniscrub.git
COPY ./scripts/miniscrub-install.sh /kb/module/scripts/miniscrub-install.sh
RUN ./scripts/miniscrub-install.sh
# RUN cd jgi-miniscrub
# RUN python3 nodocker-setup.py
# RUN python3 miniscrub.py my-reads.fastq 
# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
