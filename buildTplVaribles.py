import json
import logging
import sys
import argparse
import os

logging.basicConfig(level='DEBUG', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

parser = argparse.ArgumentParser(description='Akamai CI toolkit -> ' + os.path.basename(__file__))
parser.add_argument('--file', '-f', action="store", default=[], help="The JSON of the template property to validate.")
parser.add_argument('--variables', '-v', action="store", default="latest", help="The variable file from VCS.")
args = parser.parse_args()

if len(sys.argv) <=2:
    parser.print_help()
    sys.exit(1)

try:
    # Load source data
    sourceData = json.load(open(args.file))
    # Load variables
    variables = json.load(open(args.variables))
    sourceVariables = sourceData['rules']['variables']

except Exception as e:
    log.error('Error parsing JSON!')
    log.error(e)
    sys.exit(1)

log.info('Scrubbing _TPL_ variables from source: ' + args.file)
for item in list(sourceVariables):
    if '_TPL_' in item['name']:
        sourceVariables.remove(item)

# Concatenate the lists
log.info('Concatenating worker and _TPL_ variables...')
variables.extend(sourceVariables)

try:
    # Write output to destination file
    log.info('Writing to output file: ' + args.variables)
    with open(args.variables, 'w') as outputFile:
        json.dump(variables, outputFile, indent=4)
except Exception as e:
    log.error('Unable to write to file!')
    log.error(e)
