import yaml
import requests
import json

def loadConfig(config):

    config = yaml.load(open(config))
    return config

def getLatestVersion(session, baseurl, propertyId):
    endpoint = baseurl + '/papi/v1/properties/' + propertyId + '/versions/latest'

    result = session.get(endpoint).json()
    latestVersion = result['versions']['items'][0]['propertyVersion']

    return str(latestVersion)

def getActivations(session, baseurl, propertyId):

    endpoint = baseurl + '/papi/v1/properties/' + propertyId + '/activations'
    result = session.get(endpoint).json()
    activations = result['activations']['items']

    return activations

def getRuleTreeFromVersion(session, baseurl, propertyId, version):

    endpoint = baseurl + '/papi/v1/properties/' + propertyId + '/versions/' + version + '/rules'
    result = session.get(endpoint).json()

    return result
