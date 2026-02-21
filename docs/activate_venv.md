## Installation packages in virtual environments
```bash
# Creation enviroment (Ubuntu)
python3 -m venv venv
source venv/bin/activate

# Example
pip install build
pip install flake8
flake8 --version

# Install the packages from requirements.txt
pip install -r requirements.txt

# Exit
deactivate
```