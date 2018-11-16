# akamai-build-pipeline

The scripts contained within this project are used to facilitate the build and validation of Akamai configuration artifacts.

- **Build Scripts** transform templatized Akamai configuration data into stage (environment) specific artifacts
- **Validation** perform static code analysis on transformed (built) artifacts as a pre-deployment step

## Runtime Environment

Each script was developed and tested using a python 3 (3.6.2) interpeter.

It should also be noted that the scripts assume the runtime environment will be a Linux/Unix OS. Some scripts expect Linux specific directory structures.

# Script Installation

All package dependencies are maintained in the requirements.txt file. Use pip to install.

```pip install -r requirements.txt```


#  Script Usage

All scripts must be invoked using the python3 interpreter directly.

**Example**
python3 *\<script\>* *\<arguments\>*

## Build Scripts

The following scripts are used to transform templatized configuration artifacts in JSON format to stage specific variants.

### pullConfigFromVersion.py

In order to use this script, you will need to edit it to include your '.edgerc' location (the file containing your API authorizations).

Using a text editor, edit line 12 and provide the full system path to your .edgerc file.

**Example:**
edgeRcLoc = '/Users/bob/.edgerc'

Takes one **optional** argument, a version of the 'anf-md-staging' property to be ingested and used in a build process.

pullConfigFromVersion.py *\<Version Number\>*

*Version Number* - takes a numeric value (ex: '14') OR leave blank to specify 'latest' (to identify and pull the most recent version)

The script will pull the latest version of anf-md-staging, and create a file in the working directory 'anf-md-staging_pm.json'.

### extractVariables.py
<font face="verdana" color="red"><b>This script is now deprecated- all variables will be pulled from this project into the pipeline</b></font>

Takes one argument, a stage specific Akamai configuration artifact:

extractVariables.py *\<json file\>*

The script will generate a new artifact with a name of ‘json_file.json.var’ in a directory ‘./var’. Essentially, the script is simply pulling the variables element from the stage rule true passed as an argument, saving it as a discrete file. Prior to running the script, ensure that this ‘var/’ subdirectory exists within the working directory, otherwise the script will fail.

### injectVariables.py

This script takes 2 arguments:

injectVariables.py *\<path to variable file\>* *\<anf-md-staging json\>*

The script will generate a json file in the current working directory. The outputted JSON file will contain the variables from the 'variable file' (argument 1) and replace the variables contained within the 'anf-staging-md json' file (argument 2).


## Validation Scripts

These scripts perform pre-deployment checks on artifacts following (or during) the build process, to certify them as deployable.

### validateVariables.py

This script takes two arguments:

validateVariables.py *\<anf-md-staging json\>* *\<stage variable json\>*

This script compares the population (count) and naming of each variable with the variables contained in the anf-md-staging json. If there is a discrepancy in the count or the naming of any variables, the script will produce a non-zero exit and log the discrepancy to the shell.

### validateSchema.py

In order to use this script, you will need to edit it to include your '.edgerc' location (the file containing your API authorizations).

Using a text editor, edit line 16 and provide the full system path to your .edgerc file.

**Example:**
edgeRcLoc = '/Users/bob/.edgerc'

This script takes one argument:

validateSchema.py *\<stage specific json file\>*

This script will produce a non-zero exit code if the JSON does not conform to the product schema. It will also log output to the shell indicating what specific JSON elements are incorrect, including their placement in the rule hierarchy.

 # Setting Up akamai-build-pipeline on Local environment
 - Make sure Docker is installed
 - In the directory where the project is checked out, run: ```docker build -t akamai-build-pipeline .```
 - Once that is complete, the command syntax is:
 ```docker run -v $HOME/.edgerc:/root/.edgerc akamai-build-pipeline -a cert -b abercrombie -t "Joel test comment" -n 7```
 - The ```-v``` option mounts your edgerc credentials where the image can find it \[MANDATORY\]
 - The ```-a``` option corresponds to the appropriate Abercrombie environment (cert|www03|www) \[MANDATORY\]
 - The ```-b``` option corresponds to the appropriate Brand (abercrombie|hollisterco) \[MANDATORY\]
 - The ```-t``` option corresponds to the appropriate comment for the change.  Must be enclosed in quotes. \[MANDATORY\]
 - The ```-n``` option corresponds to the appropriate version of the gold image to use. \[MANDATORY\]
 - Important note: The process only deploys to STAGING.  Deployments to production must happen as a promotion in Luna.

# Variable Modification

The ANF pipeline now requires that modifications to variables (adding/removing variables, or changing their value) occur using the variable artifacts contained within this Github project.

[Please reference this guide for specific instructions on variable modification](VARIABLES.md)
