from jsonschema import validate
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import json
import logging
import sys

logging.basicConfig(level='INFO', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

# Run time settings
product = 'prd_SPM'
ruleFormat = 'latest'
# Full path to '.edgerc' file
# Ex: /home/user/.edgerc
edgeRcLoc = ''

# sys.argv[1] = source JSON (The variables we will extract)
argLen = len(sys.argv)
log.debug('Found ' + str(argLen) + ' command line arguments.')

for arg in sys.argv:
    log.debug('Argument: ' +  arg)


if argLen != 2:
    log.error('Incorrect number of arguments: ' + str(argLen))
    sys.exit()

try:
    sourceData = json.load(open(sys.argv[1]))
except Exception as e:
    log.error('Error loading JSON from arguments: ' + sys.argv[1])
    sys.exit(1)


# EdgeGrid authentication
try:
    edgerc = EdgeRc(edgeRcLoc)
    section = 'default'
    baseurl = 'https://%s' % edgerc.get(section, 'host')
    s = requests.Session()
    s.auth = EdgeGridAuth.from_edgerc(edgerc, section)

except Exception as e:
    log.error('Error authenticating client.')
    log.error(e)

endpoint = baseurl + '/papi/v1/schemas/products/' + product + '/' + ruleFormat

log.info('Retrieving schema from ' + endpoint)
result = s.get(endpoint)
schema = result.json()

try:
    log.info('Validating ' + sys.argv[1] + ' against product \'' + product + '\' schema for ruleFormat \'' + ruleFormat + '\'.')
    validate(sourceData, schema)
except Exception as e:
    log.error('Error validating schema..')
    log.error(e)
    # Provide non-zero exit
    sys.exit(1)

log.info('Success! ' + sys.argv[1] + ' conforms to rule format schema for product!')
