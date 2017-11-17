# gate
Docker image and utilities for data science things.

## gate.py
### Commands
#### Building
`./gate.py --build`

This will build the jupyter docker image. Make sure docker is running beforehand!

#### Running
`./gate.py --jupyter .`
This will run the jupyter docker image with with the other argument being the working directory. Will not function if image is not built.
