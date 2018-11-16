import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import json
import logging
import sys


logging.basicConfig(level='INFO', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()

# Add the location of your .edgerc file (full path)
edgeRcLoc = '/root/.edgerc'

# Add the section of the .edgerc file you would like to use (ex: default)
edgeRcSection = 'default'

# Add the propertyID you wish to use (default is for 'anf-md-staging_pm')
propertyId = 'prp_429105'

# sys.argv[1] = The version number we will use for the pull
argLen = len(sys.argv)
log.debug('Found ' + str(argLen) + ' command line arguments.')

for arg in sys.argv:
    log.debug('Argument: ' +  arg)


if argLen != 2:
    #log.info('No version specified, using latest.')
    log.error('No version specified- script will exit. Please pass a numeric version number!')
    #stagingVersion = 'latest'
    sys.exit(1)

else:
    log.info('Version: ' + sys.argv[1] + ' passed via command line arguments.')
    stagingVersion = sys.argv[1]


try:
    log.debug('Authenticating client using ' +  edgeRcLoc + ' authorization file.')
    edgerc = EdgeRc(edgeRcLoc)
    section = edgeRcSection
    baseurl = 'https://%s' % edgerc.get(section, 'host')
    s = requests.Session()
    s.auth = EdgeGridAuth.from_edgerc(edgerc, section)

except Exception as e:
    log.error('Error authenticating client.')
    log.error(e)


def getLatestVersion():

    endpoint = baseurl + '/papi/v1/properties/' + propertyId + '/versions/latest'

    try:
        result = s.get(endpoint).json()
        latestVersion = result['versions']['items'][0]['propertyVersion']

    except Exception as e:
        log.error('Encountered exception retrieving property version for property: ' + propertyId)
        log.error('Endpoint: ' + endpoint)
        log.error(e)

    return latestVersion

def checkActivationStatus(version):

    endpoint = baseurl + '/papi/v1/properties/' + propertyId + '/activations'
    activationStatus = None

    try:
        result = s.get(endpoint).json()
        activations = result['activations']['items']

    except Exception as e:
        log.error('Encountered exception retrieving activation list for property: ' + propertyId)
        log.error('Endpoint: ' + endpoint)
        log.error(e)


    log.debug('Found ' + str(len(activations)) + ' activations for property.')
    log.debug('Parsing activation list attempting to find a previously activation for version: ' + version)

    for activation in activations:
        if str(activation['propertyVersion']) == version:
            log.info('Found activation for version: ' + version)
            log.info('Activation status: ' + activation['status'])
            log.info('Activation Notes: ' + activation['note'])
            log.info('Submitted date: ' + activation['submitDate'] + ' Update Date: ' + activation['updateDate'])
            activationStatus = 'active'
            break

    return activationStatus

if stagingVersion == 'latest':
    log.info('Latest version requested for ' + propertyId)
    log.info('Finding latest version ID...')
    stagingVersion = str(getLatestVersion())
    log.info('Latest version identified is: ' + stagingVersion)

else:
    log.info('Pulling version ' + stagingVersion + ' for property ' + propertyId)

activationStatus = checkActivationStatus(stagingVersion)

if activationStatus is None:
    log.error('No activation status was found for property: ' + propertyId + ' version: ' + stagingVersion)
    log.error('Exiting!')
    sys.exit(1)

log.info('Retrieving rule tree for property: ' + propertyId)
endpoint = baseurl + '/papi/v1/properties/' + propertyId + '/versions/' + stagingVersion + '/rules'

log.debug('Using endpoint: ' + endpoint)
result = s.get(endpoint).json()

log.info('Updating property comments, appending version number (' + stagingVersion + ')')
comments = result['comments']
comments = '(original comments) ' + comments + ' (pipeline comments) Based on GOLD version: ' + stagingVersion

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