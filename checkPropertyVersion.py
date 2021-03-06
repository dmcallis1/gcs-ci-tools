import json
import sys
import re


if len(sys.argv) != 3:
    sys.exit(1)

try:
    # Delivery config obtained from VCS
    vcs_config = open(sys.argv[1], 'r')
    vcs_config_data = json.load(vcs_config)

    # Delivery config obtained from PM
    pm_config = open(sys.argv[2], 'r')
    pm_config_data = json.load(pm_config)
except Exception as e:
    print ('Exception encountered parsing json.')
    print (e)

print ('Metadata version: ' + str(pm_config_data['propertyVersion']))
print ('VCS version: ' + str(vcs_config_data['propertyVersion']))

# Compare the delivery config versions
if pm_config_data['propertyVersion'] > vcs_config_data['propertyVersion']:
    try:
        if 'CI_READY' in pm_config_data['comments']:
            comment = re.sub('(CI_READY)', r'\1', pm_config_data['comments'])
            pm_config_data['comments'] = comment
            print ('Config ' + sys.argv[2] + ' is ready for integration.')
            sys.exit(0)
    except Exception as e:
        print ('Property is missing \'comments\' attribute.')
        print (e)
else:
    print ('Config ' + sys.argv[2] + ' not ready for integration, exiting.')
    sys.exit(1)