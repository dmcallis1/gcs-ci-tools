import json
import logging
import sys

logging.basicConfig(level='DEBUG', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

# sys.argv[1] = source JSON (The variables we will use as our basis for validation)
# sys.argv[2] = variable JSON (The variables we will check against the base JSON, argv[1])
argLen = len(sys.argv)
log.debug('Found ' + str(argLen) + ' command line arguments.')

for arg in sys.argv:
    log.debug('Argument: ' +  arg)

if argLen != 3:
    log.error('Incorrect number of arguments: ' + str(argLen))
    sys.exit()

try:
    # Load source data
    sourceData = json.load(open(sys.argv[1]))
    # Load variables
    variables = json.load(open(sys.argv[2]))
    sourceVariables = sourceData['rules']['variables']

except Exception as e:
    log.error('Error parsing JSON!')
    log.error(e)
    sys.exit(1)

if len(sourceVariables) != len(variables):
    log.error('Number of variables differs from source JSON!')
    log.error('Source JSON (' + sys.argv[1] + '): ' + str(len(sourceVariables)))
    log.error('Variable File (' + sys.argv[2] + '): ' + str(len(variables)))
    sys.exit(1)

log.info('Variable population is consistent...')
log.info('Source JSON (' + sys.argv[1] + '): ' + str(len(sourceVariables)))
log.info('Variable File (' + sys.argv[2] + '): ' + str(len(variables)))

log.info('Comparing variable structure...')



for sVar in sourceVariables:
    for var in variables:
        if sVar['name'] == var['name']:
            log.debug('Found matching variable: ' + sVar['name'] + ' in file: ' + sys.argv[2])
            found = True
    if found != True:
        log.error('Expected Variable: ' + sVar['name'] + ': not in ' + sys.argv[2] + '!')
        sys.exit(1)

log.info('Variables are found to be structurally and syntactially consistent!')