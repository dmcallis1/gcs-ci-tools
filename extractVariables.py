import json
import sys
import logging

# Variables
destDir = './var/'

logging.basicConfig(level='DEBUG', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

# sys.argv[1] = source JSON (The variables we will extract)
argLen = len(sys.argv)

if argLen != 2:
    log.error('Incorrect number of arguments: ' + str(argLen))
    sys.exit()

log.debug('Passed arguments - 1: ' + str(sys.argv[1]))

try:
    # Take variables from SOURCE and modify the OUTPUT
    sourceData = json.load(open(sys.argv[1]))
except Exception as e:
    log.error('Error loading input JSON.')
    log.error(e)

log.info('Extracting variables from ' + str(sys.argv[1]))

inputVariables = sourceData['rules']['variables']

log.info('Source JSON contains ' + str(len(inputVariables)) + ' variable entries.')

# Create output variable file: inputfile.var.json
outFile = destDir + sys.argv[1].replace('.json', '.var.json')

try:
    # Write output to file
    with open(outFile, 'w') as outputFile:
        json.dump(inputVariables, outputFile, indent=4)
except Exception as e:
    log.error('Unable to write to file!')
    log.error(e)