import json
import logging
import sys
import argparse
import os

logging.basicConfig(level='DEBUG', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

# sys.argv[1] = source JSON (The variables we will use as our basis for validation)
# sys.argv[2] = variable JSON (The variables we will check against the base JSON, argv[1])

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

if len(sourceVariables) != len(variables):
    log.error('Number of variables differs from source JSON!')
    log.error('Source JSON (' + args.file + '): ' + str(len(sourceVariables)))
    log.error('Variable File (' + args.variables + '): ' + str(len(variables)))
    sys.exit(1)

log.info('Variable population is consistent...')
log.info('Source JSON (' + args.file + '): ' + str(len(sourceVariables)))
log.info('Variable File (' + args.variables + '): ' + str(len(variables)))
log.info('Comparing variable structure...')

for sVar in sourceVariables:
    for var in variables:
        if sVar['name'] == var['name']:
            log.debug('Found matching variable: ' + sVar['name'] + ' in file: ' + args.variables)
            found = True
    if found != True:
        log.error('Expected Variable: ' + sVar['name'] + ': not in ' + args.variables + '!')
        sys.exit(1)

log.info('Variables are found to be structurally and syntactially consistent!')