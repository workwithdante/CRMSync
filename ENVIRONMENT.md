# Install
conda env create -f environment.yml --verbose
conda activate crmsync
poetry env use $(which python)
poetry install

# Uninstall
conda deactivate
conda env remove -n crmsync

# Broken numpy with poetry
conda install numpy=1.26 --force-reinstall
python -c "import numpy; print(numpy.__version__)"
python -c "import cudf; print(cudf.__version__)"

# Info Env
conda info --envs