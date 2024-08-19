FROM odoo:16.0
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends systemctl

# RUN useradd --user-group --create-home --shell /bin/bash ros ;\
#         echo "ros ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
### For Windows, uncomment the following lines to install WSLg dependencies and utilize vGPU acceleration 
# ENV DEBIAN_FRONTEND=noninteractive
# RUN apt-get update \
#    && apt-get -y install \
#           vainfo \
#           mesa-va-drivers \
#           mesa-utils \
#    # Clean up
#         && apt-get autoremove -y \
#         && apt-get clean -y \
#         && rm -rf /var/lib/apt/lists/*
# ENV LIBVA_DRIVER_NAME=d3d12
# ENV LD_LIBRARY_PATH=/usr/lib/wsl/lib
# CMD vainfo --display drm --device /dev/dri/card0
# ENV DEBIAN_FRONTEND=dialog

# ** [Optional] Uncomment this section to install additional packages. **
#
# ENV DEBIAN_FRONTEND=noninteractive
# RUN apt-get update \
#    && apt-get -y install --no-install-recommends software-properties-common \
#    wget \
#    #
#    # Clean up
#    && apt-get autoremove -y \
#    && apt-get clean -y \
#    && rm -rf /var/lib/apt/lists/*
# ENV DEBIAN_FRONTEND=dialog

ENV SHELL /bin/bash

# Set up auto-source of workspace for ros user
USER odoo










# RUN ${WORKSPACE}/scripts/install-dependencies.sh
################
# uncomment below for nvidia support
# Expose the nvidia driver to allow opengl 
# Dependencies for glvnd and X11.
################
# RUN apt-get update \
# && apt-get install -y -qq --no-install-recommends \
# libglvnd0 \
# libgl1 \
# libglx0 \
# libegl1 \
# libxext6 \
# libx11-6 \
# && rm -rf /var/lib/apt/lists/*

# Env vars for the nvidia-container-runtime.
# ENV NVIDIA_VISIBLE_DEVICES all
# ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute

# ENV QT_X11_NO_MITSHM=1
# # RUN echo "if [ -f ${WORKSPACE}/install/setup.bash ]; then source ${WORKSPACE}/install/setup.bash; fi" >> /home/ros/.bashrc
# USER ros