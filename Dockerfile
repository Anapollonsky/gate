FROM pritunl/archlinux
MAINTAINER Andrew Apollonsky <anapollonsky@gmail.com>

# Install Pacman packages
RUN pacman -Syyu
RUN pacman --noconfirm -S \
base-devel \
curl \
expac \
git \
ipython \
jdk8-openjdk \
jupyter \
openssl \
perl \
python-pip \
python-numpy \
python-pandas \
python-matplotlib \
python-scipy \
python-scikit-learn \
sudo \
yajl \
vi


# AUR packages
# Install Pacaur
RUN sed -i '/NOPASSWD/s/\#//' /etc/sudoers
RUN useradd -r -g wheel build

WORKDIR /build
RUN chown -R build /build

WORKDIR /home/build
RUN chown -R build /home/build
USER build
RUN gpg --recv-keys --keyserver hkp://pgp.mit.edu 1EB2638FF56C0C53

WORKDIR /build
RUN git clone https://aur.archlinux.org/cower.git
WORKDIR /build/cower
RUN PATH=$PATH:/usr/bin/core_perl; makepkg --noconfirm -i

WORKDIR /build
RUN git clone https://aur.archlinux.org/pacaur.git
WORKDIR /build/pacaur
RUN PATH=$PATH:/usr/bin/core_perl; makepkg --noconfirm -i

# Install Pacaur packages
RUN  pacaur --noedit --noconfirm -Syu \
google-cloud-sdk

# Clean up after pacaur
USER root

RUN sed -i '/silent/s/true/false/; /silent/s/#//' /etc/xdg/pacaur/config
ENV AURDEST /build
ENV PACMAN pacaur

# Install PIP packages
RUN pip install \
datalab 
# google-cloud-bigquery

# Configure IPYTHON
COPY config/ipython_config.py /root/.ipython/profile_default/ipython_config.py
COPY config/ipython_kernel_config.py /root/.ipython/profile_default/ipython_kernel_config.py

# Tini entrypoint
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]
# CMD [ "/bin/bash" ]
# EXPOSE 8888

# Install Drill
# RUN pacman --noconfirm -S wget
# WORKDIR /build
# RUN wget http://apache.mirrors.hoobly.com/drill/drill-1.11.0/apache-drill-1.11.0.tar.gz
# RUN mkdir -p /opt/drill
# RUN tar -xvzf apache-drill-1.11.0.tar.gz -C /opt/drill


WORKDIR /local

