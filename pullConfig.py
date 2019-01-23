import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import json
import logging
import sys
import os
import argparse
from lib import ciHelper

# Initialize logging
logging.basicConfig(level='INFO', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

parser = argparse.ArgumentParser(description='Akamai CI toolkit -> ' + os.path.basename(__file__))
parser.add_argument('--config', '-c', action="store", default=os.environ['HOME'] + "/config.yaml", help="Full path to configuration YAML file")
parser.add_argument('--version', '-t', action="store", default="latest", help="The version of the template property to ingest (default is latest version)")
args = parser.parse_args()


if len(sys.argv) <=2:
    parser.print_help()
    sys.exit(1)

version = args.version

# Initialize run-time configurations
try:
    config = ciHelper.loadConfig(args.config)
except Exception as e:
    log.error('Error loading config file...')
    log.error(e)
    parser.print_help()
    sys.exit(1)

# Initialize worker variables from config file
edgeRcLoc = config['edgerc']['location']
edgeRcSection = config['edgerc']['section']
propertyId = config['property']['propertyId']

# Authenticate the client
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

# Get the activation status
try:
    log.info('Checking activation status on staging for version: ' + version)
    activations = ciHelper.getActivations(session, baseurl, propertyId)
except Exception as e:
    log.error('Encountered exception while checking activation status.')
    log.error(e)


# Parse through activation list, checking if the version we are pulling is active
isActive = None
for activation in activations:
    if str(activation['propertyVersion']) == version:
        log.info('Found activation for version: ' + version)
        log.info('Network: ' + activation['network'])
        log.info('Activation status: ' + activation['status'])
        log.info('Activation Notes: ' + activation['note'])
        log.info('Submitted date: ' + activation['submitDate'] + ' Update Date: ' + activation['updateDate'])
        isActive = True
        break

if isActive is None or isActive != True:
    log.error('No activation found for version specified: ' + version)
    log.error('Ensure that the version specified is active on either STAGING or PRODUCTION network. GOLD property activation is required to ensure consistent builds on this release version.')
    sys.exit(1)

result = ciHelper.getRuleTreeFromVersion(session, baseurl, propertyId, version)
log.info('Updating property comments, appending version number (' + version + ')')

if 'comments' not in result:
    comments = 'None.'
else:
    comments = result['comments']
    comments = '(original comments) ' + comments + ' (pipeline comments) Based on GOLD version: ' + version
    result['comments'] = comments

log.info('New comments: \'' + comments + '\'')


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
