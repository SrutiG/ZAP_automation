#!/usr/bin/python
import sys
import os
import subprocess
#import re
import requests
#import yaml
import json
from urlparse import urlparse
import time
import urllib
import ZAPFormAuth 
import  ZAPCommon 
import argparse


############ Default Values ############
# # Load configuration
# configFile = 'ZAPconfig.json'
# with open(configFile) as json_data_file:
#     config = json.load(json_data_file)
# ZAP_apikey = config['default']['ZAP_apikey']
# ZAP_baseURL = config['default']['ZAP_baseURL'] # ip of ZAP node
# ZAP_apiformat = config['default']['ZAP_apiformat']
ZAPCommon = ZAPCommon.ZAPCommon()
config = ZAPCommon.config
ZAP_apikey = ZAPCommon.ZAP_apikey
ZAP_baseURL = ZAPCommon.ZAP_baseURL
ZAP_apiformat = ZAPCommon.ZAP_apiformat


def getProxyHistory():
    viewSitesPath = config['ZAP_core']['viewSitesPath']
    #viewSiteURL = ZAP_baseURL + "/" + viewSitesPath
    payload ={'zapapiformat':ZAP_apiformat,'apikey':ZAP_apikey}
    site_list = ZAPCommon.initiateZAPAPI(viewSitesPath,'','',payload)
    return site_list.json()

def spiderURLwithUserCred(contextId, userId, URL):
    # The url must be url encoded
    #URL_enc = urllib.quote_plus(URL)
    scanAsUserPath =  config['spider']['scanAsUserPath']
    payload = {'zapapiformat':ZAP_apiformat,'apikey':ZAP_apikey,'contextId':contextId,'userId':userId,'url':URL}
    spiderAsUser_resp = ZAPCommon.initiateZAPAPI(scanAsUserPath,'','',payload)
    if spiderAsUser_resp.status_code == 200:
        print "[Info] Currently crawling the application: " + URL
        return 
        
# Scan status
def getSpiderStatus(scanId=None):
    spiderStatusPath = config['spider']['spiderStatus_User'] 
    #StatusURL = ZAP_baseURL + "/" + statusPath
    payload = {'apikey':ZAP_apikey,'zapapiformat':ZAP_apiformat,'scanId':scanId}
    spiderStatus_response = ZAPCommon.initiateZAPAPI(spiderStatusPath,'','',payload)
    return spiderStatus_response         
    
    
    
####################### Main #########################################        


# Clean up scan and logs and create new session
'''
Uncomment after testing is done
'''
#newSession_response = createNewSession()
# if newSession_response.status_code != 200:
#     print "[Error] Error occurred while trying to create a session"


#ZAPCommon = ZAPCommon.ZAPCommon.__init__() # initiate common method class


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='session already loaded or new session')
    parser.add_argument('--session', type=str, default="n",
                       help='--session y for loaded session, default: --session n for new session')
    parser.add_argument('--spider', type=str, default="n",
                       help='--spider y for spider, default: --spider n for no spider')
    args = parser.parse_args()
    loadSession = args.session
    spider = args.spider
    FormAuth = ZAPFormAuth.FormAuth(ZAPCommon)
    # Alert filter requires target applications to be in the context of ZAP
    # include all URLs in history to Context
    if loadSession == "y":
        ZAPCommon.loadSession() #load a saved session
    contextName = config['context']['name']
    create_response = ZAPCommon.createContext(contextName)
    contextId = create_response.json()['contextId']
    URL = config['application']['applicationURL']
    if loadSession == "y":
        site_list = getProxyHistory()['sites'] 
        for site in site_list:
            print site
            include_response = ZAPCommon.includeURLContext(contextName,URL)
    else:
        include_response = ZAPCommon.includeURLContext(contextName,URL)
    if include_response.status_code == 200:
        FormAuth.setAuthentication(contextId)
        FormAuth.setLoginIndicator(contextId)
        FormAuth.setLogoutIndicator(contextId)
        #setupUser(contextId)  
        userName = config['application']['userName']  
        createUser_resp = ZAPCommon.createNewUser(contextId, userName) # Create new user
        userId = createUser_resp.json()['userId']
        setAuthCreds_resp = ZAPCommon.setAuthCredentialUser(userId, userName, contextId) # Add user credentials
        enableUser_resp = ZAPCommon.enableUser(contextId,userId,userName) # Enable user
        if spider == "y":
            spiderAsUser_resp = spiderURLwithUserCred(contextId, userId, URL)
            scan_status = -1
            while (int(scan_status) < 100):
                time.sleep(10) # 10 seconds
                scan_status = getSpiderStatus().json()['status']
                print "[Info] Currently spidering the application. " + scan_status + "% Completed. " + "Please wait...."
            print "[Done] Spidering completed" 
            # ToDo check spider scan status



