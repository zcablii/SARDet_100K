## Install
```
# # create env
conda create -y -n MSSM python=3.8
conda activate MSSM

# install pytorch
conda install -y pytorch==2.0.1 torchvision==0.15.2 cudatoolkit=11.8 -c pytorch

# install dependencies of openmmlab
pip install -U openmim
mim install "mmengine==0.8.4"
mim install "mmcv==2.0.1"
mim install "mmdet==3.1.0"

# install other dependencies
pip install -r requirements.txt

# install MSSM
pip install -v -e .
```