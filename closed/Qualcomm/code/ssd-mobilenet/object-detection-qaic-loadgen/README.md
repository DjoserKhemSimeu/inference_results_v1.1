# Qualcomm Cloud AI - MLPerf Inference - Object Detection

1. [Installation](#installation)
    1. [Install system-wide prerequisites](#install_system)
    1. [Install CK](#install_ck)
    1. [Set platform scripts](#set_platform_scripts)
    1. [Detect Python](#detect_python)
    1. [Detect GCC](#detect_gcc)
    1. [Set up CMake](#install_cmake)
    1. [Install Python dependencies](#install_python_deps)
    1. [Install the MLPerf Inference repo](#install_inference_repo)
    1. [Prepare the COCO 2017 validation dataset](#prepare_coco)
        - [Download](#prepare_coco_download)
        - [Preprocess](#prepare_coco_preprocess)
            - [SSD-ResNet34](#prepare_coco_preprocess_ssd_resnet34)
            - [SSD-MobileNet](#prepare_coco_preprocess_ssd_mobilenet)
    1. [Prepare the workload model](#prepare_workload)
        - [Calibrate](#prepare_workload_calibrate)
            - [SSD-ResNet34](#prepare_workload_calibrate_ssd_resnet34)
            - [SSD-MobileNet](#prepare_workload_calibrate_ssd_mobilenet)
        - [Compile](#prepare_workload_compile)
            - [SSD-ResNet34](#prepare_workload_compile_ssd_resnet34)
            - [SSD-MobileNet](#prepare_workload_compile_ssd_mobilenet)

1. [Benchmark](#benchmark)
    1. [SSD-ResNet34](#benchmark_ssd_resnet34)
    1. [SSD-MobileNet](#benchmark_ssd_mobilenet)

1. [Further info](#info)


<a name="installation"></a>
# Installation

Tested on a ([Gigabyte R282-Z93](https://www.gigabyte.com/Enterprise/Rack-Server/R282-Z93-rev-100)) server with CentOS 7.9 and QAIC Platform SDK 1.5.6:

<pre><b>[anton@dyson ~]&dollar;</b> rpm -q centos-release
centos-release-7-9.2009.1.el7.centos.x86_64</pre>

<pre><b>[anton@dyson ~]&dollar;</b> uname -a
Linux dyson.localdomain 5.4.1-1.el7.elrepo.x86_64 #1 SMP Fri Nov 29 10:21:13 EST 2019 x86_64 x86_64 x86_64 GNU/Linux</pre>

<pre><b>[anton@dyson ~]&dollar;</b> cat /opt/qti-aic/versions/platform.xml</pre>
```
<versions>
        <ci_build>
           <base_name>AIC</base_name>
           <base_version>1.5</base_version>
           <build_id>6</build_id>
        </ci_build>
        </versions>
```

<a name="install_system"></a>
## Install system-wide prerequisites

**NB:** Run the below commands with `sudo` or as superuser.

<a name="install_system_centos7"></a>
### CentOS 7

#### Generic

<pre>
<b>[anton@dyson ~]&dollar;</b> sudo yum upgrade -y
<b>[anton@dyson ~]&dollar;</b> sudo yum install -y \
make which patch vim git wget zip unzip openssl-devel bzip2-devel libffi-devel
<b>[anton@dyson ~]&dollar;</b> sudo yum clean all
</pre>

#### dnf  ("the new yum"!)

<pre>
<b>[anton@dyson ~]&dollar;</b> sudo yum install -y dnf
</pre>


#### Python 3.6 (default)

<pre>
<b>[anton@dyson ~]&dollar;</b> sudo dnf install -y python3 python3-pip python3-devel
<b>[anton@dyson ~]&dollar;</b> python3 --version
Python 3.6.8
</pre>

#### Python 3.7 (optional; required only for power measurements)

<pre>
<b>[anton@dyson ~]&dollar;</b> sudo su
<b>[root@dyson anton]#</b> export PYTHON_VERSION=3.7.11
<b>[root@dyson anton]#</b> cd /usr/src \
&& wget https://www.python.org/ftp/python/&dollar;{PYTHON_VERSION}/Python-&dollar;{PYTHON_VERSION}.tgz \
&& tar xzf Python-&dollar;{PYTHON_VERSION}.tgz \
&& rm -f Python-&dollar;{PYTHON_VERSION}.tgz \
&& cd /usr/src/Python-&dollar;{PYTHON_VERSION} \
&& ./configure --enable-optimizations  --enable-shared --with-ssl && make -j 32 altinstall \
&& rm -rf /usr/src/Python-&dollar;{PYTHON_VERSION}*
<b>[root@dyson ~]#</b> exit
exit
<b>[anton@dyson ~]&dollar;</b> python3.7 --version
Python 3.7.11
</pre>

#### GCC 9

<pre>
<b>[anton@dyson ~]&dollar;</b> sudo yum install -y centos-release-scl
<b>[anton@dyson ~]&dollar;</b> sudo yum install -y scl-utils
<b>[anton@dyson ~]&dollar;</b> sudo yum install -y devtoolset-9
<b>[anton@dyson ~]&dollar;</b> echo "source scl_source enable devtoolset-9" >> ~/.bashrc
<b>[anton@dyson ~]&dollar;</b> source ~/.bashrc
</pre>

##### `gcc`

<pre>
<b>[anton@dyson ~]&dollar;</b> scl enable devtoolset-9 "gcc --version"
gcc (GCC) 9.3.1 20200408 (Red Hat 9.3.1-2)
Copyright (C) 2019 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
</pre>

##### `g++`

<pre>
<b>[anton@dyson ~]&dollar;</b> scl enable devtoolset-9 "g++ --version"
g++ (GCC) 9.3.1 20200408 (Red Hat 9.3.1-2)
Copyright (C) 2019 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
</pre>

<a name="install_ck"></a>
## Install [Collective Knowledge](http://cknowledge.org/) (CK)

<pre>
<b>[anton@dyson ~]&dollar;</b> export CK_PYTHON=`which python3`
<b>[anton@dyson ~]&dollar;</b> &dollar;CK_PYTHON -m pip install --ignore-installed pip setuptools testresources --user --upgrade
<b>[anton@dyson ~]&dollar;</b> &dollar;CK_PYTHON -m pip install ck==1.55.5
<b>[anton@dyson ~]&dollar;</b> echo 'export PATH=&dollar;HOME/.local/bin:&dollar;PATH' >> &dollar;HOME/.bashrc
<b>[anton@dyson ~]&dollar;</b> source &dollar;HOME/.bashrc
<b>[anton@dyson ~]&dollar;</b> ck version
V1.55.5
</pre>

<a name="install_ck_repos"></a>
## Install CK repositories

<pre>
<b>[anton@dyson ~]&dollar;</b> ck pull repo --url=https://github.com/krai/ck-qaic
</pre>


<a name="set_platform_scripts"></a>
## Set platform scripts

### `r282_z93_q5`: use QAIC settings (ECC on)

<pre>
<b>[anton@dyson ~]&dollar;</b> ck detect platform.os --platform_init_uoa=qaic

OS CK UOA:            linux-64 (4258b5fe54828a50)

OS name:              CentOS Linux 7 (Core)
Short OS name:        Linux 5.4.1
Long OS name:         Linux-5.4.1-1.el7.elrepo.x86_64-x86_64-with-centos-7.9.2009-Core
OS bits:              64
OS ABI:               x86_64

Platform init UOA:    qaic

<b>[anton@dyson ~]&dollar;</b> cat $(ck find repo:local)/cfg/local-platform/.cm/meta.json
{
  "platform_init_uoa": {
    "linux-64": "qaic"
  }
}
</pre>


### `aedk`: use AEDK settings

<pre>
<b>[anton@aedk3 ~]&dollar;</b> ck detect platform.os --platform_init_uoa=aedk

OS CK UOA:            linux-64 (4258b5fe54828a50)

OS name:              CentOS Linux 8 (Core)
Short OS name:        Linux 4.19.81
Long OS name:         Linux-4.19.81-aarch64-with-centos-8.0.1905-Core
OS bits:              64
OS ABI:               aarch64

Platform init UOA:    aedk

<b>[anton@aedk3 ~] ~]&dollar;</b> cat $(ck find repo:local)/cfg/local-platform/.cm/meta.json
{
  "platform_init_uoa": {
    "linux-64": "aedk"
  }
}
</pre>


<a name="detect_python"></a>
## Detect Python

**NB:** Please detect only one Python interpreter. Python 3.6, the default on CentOS 7, is <font color="#268BD0"><b>recommended</b></font>. While CK can normally detect available Python interpreters automatically, we are playing safe here by only detecting a particular one. Please only detect multiple Python interpreters, if you understand the consequences.

### <font color="#268BD0">Python v3.6 (default)</font>

<pre>
<b>[anton@dyson ~]&dollar;</b> ck detect soft:compiler.python --full_path=`which python3`
<b>[anton@dyson ~]&dollar;</b> ck show env --tags=compiler,python
Env UID:         Target OS: Bits: Name:  Version: Tags:

ce146fbbcd1a8fea   linux-64    64 python 3.6.8    64bits,compiler,host-os-linux-64,lang-python,python,target-os-linux-64,v3,v3.6,v3.6.8
</pre>

<a name="detect_gcc"></a>
## Detect (system) GCC

**NB:** CK can normally detect compilers automatically, but we are playing safe here.

<pre>
<b>[anton@dyson ~]&dollar;</b> which gcc
/opt/rh/devtoolset-9/root/usr/bin/gcc
<b>[anton@dyson ~]&dollar;</b> ck detect soft:compiler.gcc --full_path=`which gcc`
<b>[anton@dyson ~]&dollar;</b> ck show env --tags=compiler,gcc
Env UID:         Target OS: Bits: Name:          Version: Tags:

2e27213b1488daf9   linux-64    64 GNU C compiler 9.3.1    64bits,compiler,gcc,host-os-linux-64,lang-c,lang-cpp,target-os-linux-64,v9,v9.3,v9.3.1
</pre>

<a name="install_cmake"></a>
## Detect (system) CMake or install CMake from source

<a name="install_cmake_detect"></a>
### <font color="#268BD0"><b>Detect</b></font>

Try detecting CMake on your system:
<pre>
<b>[anton@dyson ~]&dollar;</b> ck detect soft --tags=tool,cmake
<b>[anton@dyson ~]&dollar;</b> ck show env --tags=cmake
Env UID:         Target OS: Bits: Name: Version: Tags:

4b6cb0f07e9fd005   linux-64    64 cmake 3.17.5   64bits,cmake,host-os-linux-64,target-os-linux-64,tool,v3,v3.17,v3.17.5
</pre>

<a name="install_cmake_install"></a>
### Install

If this fails, install CMake from source:

<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=tool,cmake,from.source
<b>[anton@dyson ~]&dollar;</b> ck show env --tags=tool,cmake,from.source
Env UID:         Target OS: Bits: Name: Version: Tags:

9784ba222cddacb6   linux-64    64 cmake 3.20.5   64bits,cmake,compiled,compiled-by-gcc,compiled-by-gcc-9.3.0,from.source,host-os-linux-64,source,target-os-linux-64,tool,v3,v3.20,v3.20.5
</pre>

<a name="install_python_deps"></a>
## Install Python dependencies (in userspace)

#### Install implicit dependencies via pip

**NB:** These dependencies are _implicit_, i.e. CK will not try to satisfy them. If they are not installed, however, the workflow will fail.

<pre>
&dollar; export CK_PYTHON=/usr/bin/python3
&dollar; &dollar;CK_PYTHON -m pip install --user --upgrade \
  wheel pyyaml onnx-simplifier
</pre>

#### Install explicit dependencies via CK (also via `pip`, but register with CK at the same time)

**NB:** These dependencies are _explicit_, i.e. CK will try to satisfy them automatically. On a machine with multiple versions of Python, things can get messy, so we are playing safe here.

<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=python-package,numpy
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=python-package,absl
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=python-package,cython
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=python-package,opencv-python-headless
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=python-package,matplotlib
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=python-package,onnx --force_version=1.8.1
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=python-package,torch --force_version=1.8.1
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=tool,coco
</pre>


<a name="install_inference_repo"></a>
## Install the MLPerf Inference repo and build LoadGen

<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=mlperf,inference,source
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=mlperf,loadgen,static
</pre>


<a name="prepare_coco"></a>
## Prepare the COCO 2017 validation dataset (5,000 images)

### Hint
Once you have downloaded the COCO 2017 validation dataset using CK, you can register it with CK again if needed (e.g. if you reset your CK environment) as follows:

<pre>
<b>[anton@dyson ~]&dollar;</b> ck detect soft:dataset.coco.2017.val --extra_tags=detected,full \
--full_path=/datasets/dataset-coco-2017-val/val2017/000000000139.jpg
</pre>

<a name="prepare_coco_download"></a>
###  Download

<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package --ask --tags=dataset,coco,val,2017
</pre>


<a name="prepare_coco_preprocess"></a>
### Preprocess

<a name="prepare_coco_preprocess_ssd_resnet34"></a>
#### SSD-ResNet34

**NB:** Since the preprocessed `1200x1200` COCO dataset takes up 21G, you may wish to change its destination directory by appending `--ask` to the below command.

<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package --ask \
--dep_add_tags.lib-python-cv2=opencv-python-headless \
--tags=dataset,object-detection,for.ssd_resnet34.onnx.preprocessed.quantized,using-opencv,full \
--extra_tags=using-opencv
</pre>


<a name="prepare_coco_preprocess_ssd_mobilenet"></a>
#### SSD-MobileNet

<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package \
--dep_add_tags.lib-python-cv2=opencv-python-headless \
--tags=dataset,object-detection,for.ssd_mobilenet.onnx.preprocessed.quantized,using-opencv,full \
--extra_tags=using-opencv
</pre>


<a name="prepare_workload"></a>
## Prepare the workload

<a name="prepare_workload_calibrate"></a>
### Calibrate the model

#### Calibrate on your own

**NB:** For more information, please see the [calibration README](https://github.com/krai/ck-qaic/blob/main/package/model-qaic-calibrate/README.md#ssd_resnet34).

The COCO 2017 training dataset takes `20G`. Use `--ask` to confirm the destination directory.

<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package --ask --tags=dataset,coco,train,2017
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=dataset,coco,calibration,mlperf
</pre>

<a name="prepare_workload_calibrate_ssd_resnet34"></a>
##### SSD-ResNet34

<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package --ask \
--tags=dataset,coco.2017,calibration,for.ssd_resnet34.onnx.preprocessed
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=profile,ssd_resnet34
</pre>

<a name="prepare_workload_calibrate_ssd_mobilenet"></a>
##### SSD-MobileNet

<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package --ask \
--tags=dataset,coco.2017,calibration,for.ssd_mobilenet.onnx.preprocessed
<b>[anton@dyson ~]&dollar;</b> ck install package --tags=profile,ssd_mobilenet
</pre>

#### Use precalibrated profiles

##### SSD-ResNet34

<pre>
<b>[anton@dyson ~]&dollar;</b> echo "vdetected" | ck detect soft:compiler.glow.profile \
--full_path=$(ck find repo:qualcomm-private)/profile/ssd-resnet34/bs.1/profile.yaml \
--extra_tags=detected,ssd_resnet34
</pre>

##### SSD-MobileNet

##### `bs.1`
<pre>
<b>[anton@dyson ~]&dollar;</b> echo "vdetected" | ck detect soft:compiler.glow.profile \
--full_path=$(ck find repo:qualcomm-private)/profile/ssd-mobilenet/bs.1/profile.yaml \
--extra_tags=detected,ssd_mobilenet,bs.1
</pre>

##### `bs.4`
<pre>
<b>[anton@dyson ~]&dollar;</b> echo "vdetected" | ck detect soft:compiler.glow.profile \
--full_path=$(ck find repo:qualcomm-private)/profile/ssd-mobilenet/bs.4/profile.yaml \
--extra_tags=detected,ssd_mobilenet,bs.4
</pre>

<a name="prepare_workload_compile"></a>
### Compile the workload

<a name="prepare_workload_compile_ssd_resnet34"></a>
#### SSD-ResNet34

##### Compile the Server/Offline model for the PCIe server cards

<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package \
--tags=model,qaic,ssd_resnet34,ssd_resnet34.pcie.16nsp
</pre>


##### Compile and install the models to the 15W AEDK

###### Offline
<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package \
--tags=model,qaic,ssd_resnet34,ssd_resnet34.aedk_15w.offline

<b>[anton@dyson ~]&dollar;</b> ck install package --tags=install-to-aedk \
--dep_add_tags.model-qaic=ssd_resnet34,ssd_resnet34.aedk_15w.offline \
--env.CK_AEDK_IPS="aedk1" --env.CK_AEDK_PORTS="3231" --env.CK_AEDK_USER=$USER
</pre>

###### SingleStream
<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package \
--tags=model,qaic,ssd_resnet34,ssd_resnet34.aedk_15w.singlestream

<b>[anton@dyson ~]&dollar;</b> ck install package --tags=install-to-aedk \
--dep_add_tags.model-qaic=ssd_resnet34,ssd_resnet34.aedk_15w.singlestream \
--env.CK_AEDK_IPS="aedk1" --env.CK_AEDK_PORTS="3231" --env.CK_AEDK_USER=$USER
</pre>

##### Compile and install the models to the 20W AEDK

###### Offline
<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package \
--tags=model,qaic,ssd_resnet34,ssd_resnet34.aedk_20w.offline

<b>[anton@dyson ~]&dollar;</b> ck install package --tags=install-to-aedk \
--dep_add_tags.model-qaic=ssd_resnet34,ssd_resnet34.aedk_20w.offline \
--env.CK_AEDK_IPS="aedk3" --env.CK_AEDK_PORTS="3233" --env.CK_AEDK_USER=$USER
</pre>

##### SingleStream
<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package \
--tags=model,qaic,ssd_resnet34,ssd_resnet34.aedk_20w.singlestream

<b>[anton@dyson ~]&dollar;</b> ck install package --tags=install-to-aedk \
--dep_add_tags.model-qaic=ssd_resnet34,ssd_resnet34.aedk_20w.singlestream \
--env.CK_AEDK_IPS="aedk3" --env.CK_AEDK_PORTS="3233" --env.CK_AEDK_USER=$USER
</pre>

<a name="prepare_workload_compile_ssd_mobilenet"></a>
#### SSD-MobileNet

##### Compile the Server/Offline model for the PCIe server cards

<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package \
--tags=model,qaic,ssd_mobilenet,ssd_mobilenet.pcie.16nsp
</pre>


##### Compile and install the models to the 15W AEDK

###### Offline
<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package \
--tags=model,qaic,ssd_mobilenet,ssd_mobilenet.aedk_15w.offline

<b>[anton@dyson ~]&dollar;</b> ck install package --tags=install-to-aedk \
--dep_add_tags.model-qaic=ssd_mobilenet,ssd_mobilenet.aedk_15w.offline \
--env.CK_AEDK_IPS="aedk1" --env.CK_AEDK_PORTS="3231" --env.CK_AEDK_USER=$USER
</pre>

###### SingleStream
<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package \
--tags=model,qaic,ssd_mobilenet,ssd_mobilenet.aedk_15w.singlestream

<b>[anton@dyson ~]&dollar;</b> ck install package --tags=install-to-aedk \
--dep_add_tags.model-qaic=ssd_mobilenet,ssd_mobilenet.aedk_15w.singlestream \
--env.CK_AEDK_IPS="aedk1" --env.CK_AEDK_PORTS="3231" --env.CK_AEDK_USER=$USER
</pre>

##### Compile and install the models to the 20W AEDK

###### Offline
<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package \
--tags=model,qaic,ssd_mobilenet,ssd_mobilenet.aedk_20w.offline

<b>[anton@dyson ~]&dollar;</b> ck install package --tags=install-to-aedk \
--dep_add_tags.model-qaic=ssd_mobilenet,ssd_mobilenet.aedk_20w.offline \
--env.CK_AEDK_IPS="aedk3" --env.CK_AEDK_PORTS="3233" --env.CK_AEDK_USER=$USER
</pre>

##### SingleStream
<pre>
<b>[anton@dyson ~]&dollar;</b> ck install package \
--tags=model,qaic,ssd_mobilenet,ssd_mobilenet.aedk_20w.singlestream

<b>[anton@dyson ~]&dollar;</b> ck install package --tags=install-to-aedk \
--dep_add_tags.model-qaic=ssd_mobilenet,ssd_mobilenet.aedk_20w.singlestream \
--env.CK_AEDK_IPS="aedk3" --env.CK_AEDK_PORTS="3233" --env.CK_AEDK_USER=$USER
</pre>

<a name="benchmark"></a>
# Benchmark

<a name="benchmark_ssd_resnet34"></a>
## SSD-ResNet34 (Datacenter, Edge)

- [`Offline`](https://github.com/krai/ck-qaic/blob/main/program/object-detection-qaic-loadgen/README.ssd-resnet34.offline.md).
- [`Server`](https://github.com/krai/ck-qaic/blob/main/program/object-detection-qaic-loadgen/README.ssd-resnet34.server.md).
- [`Single Stream`](https://github.com/krai/ck-qaic/blob/main/program/object-detection-qaic-loadgen/README.ssd-resnet34.singlestream.md).

<a name="benchmark_ssd_mobilenet"></a>
## SSD-MobileNet (Edge only)

- [`Offline`](https://github.com/krai/ck-qaic/blob/main/program/object-detection-qaic-loadgen/README.ssd-mobilenet.offline.md).
- [`Single Stream`](https://github.com/krai/ck-qaic/blob/main/program/object-detection-qaic-loadgen/README.ssd-mobilenet.singlestream.md).

<a name="info"></a>
# Further info

Please contact anton@krai.ai if you have any problems or questions.
