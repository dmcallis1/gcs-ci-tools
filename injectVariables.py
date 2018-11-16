import json
import sys
import logging
import os

# Variables
destDir = './var/'

logging.basicConfig(level='DEBUG', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

# sys.argv[1] = source JSON (The variables we will extract)
argLen = len(sys.argv)

if argLen != 3:
    log.error('Incorrect number of arguments: ' + str(argLen))
    sys.exit()

log.debug('Passed arguments - 1: ' + str(sys.argv[1]) + ' (source variables) 2: ' + str(sys.argv[2]) + ' (source metadata)')

try:
    # Take variables from SOURCE and modify the OUTPUT
    sourceData = json.load(open(sys.argv[1]))
    outputData = json.load(open(sys.argv[2]))
except Exception as e:
    log.error('Error loading input JSON.')
    log.error(e)

log.info('Transforming source JSON with target variable values.')
log.info('Target JSON contains ' + str(len(sourceData)) + ' variable entries.')

outputData['rules']['variables'] = sourceData

destinationFile = os.path.basename(sys.argv[1].replace('.var.json', '.json'))

try:
    # Write output to destination file
    with open(destinationFile, 'w') as outputFile:
        json.dump(outputData, outputFile, indent=4)
except Exception as e:
    log.error('Unable to write to file!')
    log.error(e)

log.info(str(destinationFile + ' has been transformed and built.'))