from jsonschema import validate
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import json
import logging
import sys
import os
import argparse
from lib import ciHelper

logging.basicConfig(level='INFO', format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger()


parser = argparse.ArgumentParser(description='Akamai CI toolkit -> ' + os.path.basename(__file__))
parser.add_argument('--config', '-c', action="store", default=os.environ['HOME'] + "/config.yaml", help="Full path to configuration YAML file")
parser.add_argument('--file', '-f', action="store", default=[], help="The version of the template property to ingest (default is latest version)")
args = parser.parse_args()

if len(sys.argv) <=2:
    parser.print_help()
    sys.exit(1)


# Initialize run-time configurations
try:
    config = ciHelper.loadConfig(args.config)
except Exception as e:
    log.error('Error loading config file...')
    log.error(e)
    parser.print_help()
    sys.exit(1)

edgeRcLoc = config['edgerc']['location']
edgeRcSection = config['edgerc']['section']
propertyId = config['property']['propertyId']
product = config['property']['productType']
ruleFormat = config['property']['ruleFormat']


try:
    sourceData = json.load(open(args.file))
except Exception as e:
    log.error('Error loading template JSON from arguments: ' + args.file)
    log.error(e)
    parser.print_help()
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

# Pull schema for product
endpoint = baseurl + '/papi/v1/schemas/products/' + product + '/' + ruleFormat

log.info('Retrieving schema from ' + endpoint)
result = s.get(endpoint)
schema = result.json()

try:
    log.info('Validating ' + args.file + ' against product \'' + product + '\' schema for ruleFormat \'' + ruleFormat + '\'.')
    validate(sourceData, schema)
except Exception as e:
    log.error('Error validating schema..')
    log.error(e)
    sys.exit(1)

log.info('Success! ' + args.file + ' conforms to rule format schema for product!')
