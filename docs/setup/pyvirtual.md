# Setup Python Virtual Environment

It is recommended that you setup a Python virtual environment for this lab to avoid cluttering the global Python installation with this project-specific packages and ensures reproducibility for this tutorial.

To create the Virtual Environment after cloning the GitHub repository for this tutorial, use the following example:

```bash
git clone https://github.com/martimy/model-driven-configuration-tutorial tutorial
cd tutorial
python3 -m venv .pyenv
```

To activate the environment:

```bash
source .pyenv/bin/activate
```

Afterwards, you can install any required Python packages individually using `pip install <package-name>`, or install all required packages using the `requirements.txt`


```bash
install -r requirements.txt
```

To deactivate the virtual environment,

```bash
deactivate
```

