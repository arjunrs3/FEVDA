# FEVDA
FEVDA, Fuel Efficient Vehicle Design and Analysis, is an open source project that uses physical relationships to estimate the efficiencies of simple vehicles. It was originally developed to aid in initial design of vehicles for the Shell Eco Marathon competition.

## Getting Started

### Prerequisites
Python 3 is needed before a development environment can be created. Note that python is not necessary if FEVDA is installed with an executable.

### Installing
Executables will be issued with every release after 1.0.0. To set up a development environment, follow these steps: 

First, clone the repository using your method of choice: see [Cloning a Repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

In a command prompt, navigate to the project root directory (e.g., D:/FEVDA/):
```
cd D:/FEVDA/
```

Next, create a virtual environment named venv (Note that a version of python 3 must be installed for this to work. 
```
python -m venv venv
```

Follow these steps to activate the virtual environment (needed every time you want to run the program): 
```
cd venv
cd Scripts
./activate
cd ..
cd ..
```

Install the prerequisites in the activated virtual environment using: 
```
pip install -r requirements.txt
```

After the prerequisites are installed, the program can be run from the root directory using: 
```
python Ecocalc.py
```
Make sure to activate the virtual environment and use this command in the root directory. 

## Contributing
Thanks for your interest in contributing to this project! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute 

### Contributors
* **Arjun Shah (University of Illinois at Urbana-Champaign)** - *Initial work*
See also the list of [contributors](https://github.com/arjunrs3/FEVDA/contributors) who participated in this project

## License 
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
