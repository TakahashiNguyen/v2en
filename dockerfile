# syntax=docker/dockerfile:latest
FROM tensorflow/tensorflow:2.13.0-gpu-jupyter

# init section
WORKDIR /home
ARG TZ="Asia/ho_chi_minh"
ARG DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"] 
USER root

RUN apt update && apt upgrade -y && apt -y install \ 
    # fixed slow apt download: https://github.com/NobodyXu/apt-fast-docker/blob/master/Dockerfile
    software-properties-common gnupg curl ca-certificates
RUN sed -i 's/htt[p|ps]:\/\/archive.ubuntu.com\/ubuntu\//mirror:\/\/mirrors.ubuntu.com\/mirrors.txt/g' /etc/apt/sources.list
# install gh cli for private repo
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main"\
    | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && apt update && apt upgrade -y

# install nodejs
RUN mkdir -p /etc/apt/keyrings && \ 
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt install \
    gcc git git-lfs vim gh nodejs \
    # xrdp features at https://github.com/danchitnis/container-xrdp/blob/master/ubuntu-xfce/Dockerfile
    xfce4 xfce4-terminal xfce4-xkb-plugin \
    sudo xorgxrdp xrdp \
    # ssh server
    openssh-server \
    # nodejs 
    nodejs \
    # necessary nvidia's package
    #libcublas-12-1 libcublas-dev-12-1 nvidia-cuda-toolkit cuda \
    -y  --no-install-recommends
# clean stage 
RUN apt clean && \
    apt remove -y light-locker xscreensaver && \
    apt autoremove -y && \
    rm -rf /var/cache/apt /var/lib/apt/lists/*

ENV name admin
ENV pass lmao
ENV issudo yes
ENTRYPOINT ["/bin/bash", "-c", "/usr/bin/run.sh ${name} ${pass} ${issudo}"]

# https://github.com/danielguerra69/ubuntu-xrdp/blob/master/Dockerfile
#RUN mkdir /var/run/dbus && \
#    cp /etc/X11/xrdp/xorg.conf /etc/X11 && \
#    sed -i "s/console/anybody/g" /etc/X11/Xwrapper.config && \
#    sed -i "s/xrdp\/xorg/xorg/g" /etc/xrdp/sesman.ini && \
#    echo "xfce4-session" >> /etc/skel/.Xsession
EXPOSE 3389

RUN service ssh start
EXPOSE 24444
EXPOSE 80
EXPOSE 443

# fix sound issue: https://superuser.com/questions/1539634/pulseaudio-daemon-wont-start-inside-docker
#RUN adduser root pulse-access

# Create SSH keys
RUN ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa

# Copy public key to container
COPY id_rsa.pub /root/.ssh/authorized_keys

# Fix permissions
RUN chmod 600 /root/.ssh/authorized_keys && \
    chown root:root /root/.ssh/authorized_keys

# Expose necessary ports for SSH access
EXPOSE 22/tcp

# Set command to run on container start
COPY ./.sh/run.sh /usr/bin/
RUN chmod +x /usr/bin/run.sh
CMD ["/usr/sbin/sshd", "-D"]