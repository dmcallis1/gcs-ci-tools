import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import json
import logging
import sys
from lib import ciHelper

# Initialize logging
logging.basicConfig(level='INFO', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

# Initialize run-time configurations
try:
    config = ciHelper.loadConfig('config.ex.yaml')
except Exception as e:
    log.error('Error loading config file...')
    log.error(e)
    sys.exit(1)

edgeRcLoc = config['edgerc']['location']
edgeRcSection = config['edgerc']['section']
propertyId = config['property']['propertyId']

# sys.argv[1] = The version number we will use for the pull
argLen = len(sys.argv)
log.debug('Found ' + str(argLen) + ' command line arguments.')
for arg in sys.argv:
    log.debug('Argument: ' + arg)


if argLen != 2:
    log.error('No version specified- script will exit. Please pass a numeric version number, or \'latest\'!')
    log.error('Usage: pullConfigFromVersion.py [version]')
    sys.exit(1)
else:
    log.info('Version: ' + sys.argv[1] + ' passed via command line arguments.')
    version = sys.argv[1]

try:
    log.debug('Authenticating client using ' + edgeRcLoc + ' authorization file.')
    edgerc = EdgeRc(edgeRcLoc)
    section = edgeRcSection
    baseurl = 'https://%s' % edgerc.get(section, 'host')
    session = requests.Session()
    session.auth = EdgeGridAuth.from_edgerc(edgerc, section)

except Exception as e:
    log.error('Error authenticating client.')
    log.error(e)


if version == 'latest':
    log.info('Latest version requested. Getting latest version')
    version = ciHelper.getLatestVersion(session, baseurl, propertyId)
    log.info('Latest version identified: ' + version)

try:
    log.info('Checking activation status on staging for version: ' + version)
    activations = ciHelper.getActivations(session, baseurl, propertyId)
except Exception as e:
    log.error('Encountered exception while checking activation status.')
    log.error(e)

for activation in activations:
    if str(activation['propertyVersion']) == version:
        log.info('Found activation for version: ' + version)
        log.info('Network: ' + activation['network'])
        log.info('Activation status: ' + activation['status'])
        log.info('Activation Notes: ' + activation['note'])
        log.info('Submitted date: ' + activation['submitDate'] + ' Update Date: ' + activation['updateDate'])
        break
    else:
        log.error('No activation found for version specified: ' + version)
        log.error('Ensure that the version specified is active on either STAGING or PRODUCTION network.')

result = ciHelper.getRuleTreeFromVersion(session, baseurl, propertyId, version)
log.info('Updating property comments, appending version number (' + version + ')')
comments = result['comments']
comments = '(original comments) ' + comments + ' (pipeline comments) Based on GOLD version: ' + version
log.info('New comments: \'' + comments + '\'')
result['comments'] = comments


outFile = str(result['propertyName'] + '.json')
log.info('Output file will be: ' + outFile)

try:
    # Write output to file
    with open(outFile, 'w') as outputFile:
        json.dump(result, outputFile, indent=4)
except Exception as e:
    log.error('Unable to write to file: ' + outFile)
    log.error(e)

log.info('Successfully pulled JSON for property: ' + result['propertyName'] + '. Wrote to file: ' + outFile)
