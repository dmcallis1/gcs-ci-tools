import json
import sys
import logging
import os
import argparse

logging.basicConfig(level='DEBUG', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

parser = argparse.ArgumentParser(description='Akamai CI toolkit -> ' + os.path.basename(__file__))
parser.add_argument('--file', '-f', action="store", default=[], help="The JSON of the template property to transform into an environment release artifact.")
parser.add_argument('--variables', '-v', action="store", default="latest", help="The variable file from VCS.")
args = parser.parse_args()


if len(sys.argv) <=2:
    parser.print_help()
    sys.exit(1)


try:
    # Take variables from SOURCE and modify the OUTPUT
    outputData = json.load(open(args.file))
    log.info('Source metadata: ' + args.file)
    sourceData = json.load(open(args.variables))
    log.info('Variables: ' + args.variables)
except Exception as e:
    log.error('Error loading input JSON.')
    log.error(e)

log.info('Transforming source JSON with target variable values.')
log.info('Source JSON contains ' + str(len(sourceData)) + ' variable entries.')
outputData['rules']['variables'] = sourceData

destinationFile = os.path.basename(args.variables.replace('.var.json', '.json'))

try:
    # Write output to destination file
    with open(destinationFile, 'w') as outputFile:
        json.dump(outputData, outputFile, indent=4)
except Exception as e:
    log.error('Unable to write to file!')
    log.error(e)

log.info(str(destinationFile + ' has been transformed and built.'))