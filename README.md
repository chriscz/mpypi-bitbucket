An example base project for mpypi.
- Supports private bitbucket repositories
- Developer specific configuration possible

## Installation procedure ##

### Pre release configuration
- Before releasing your mpypi implementation to developers,
  you should specify your packages in the `packages.py` file.

### Initialization & Configuration
- clone this repository
- cd into it the directory
- run the initialization script: `./init`
- copy `default_config.py` to `config.py` and update it with your
  specific configuration. 

### Configuring pip to use your mpypi server ##
- Look at how to do the [less intrusive installation](https://github.com/chriscz/mpypi#less-intrusive-installation) 
  on the mpypi page.

### Starting server
- Run `./bootstrap` to start the server
