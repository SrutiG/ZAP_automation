import os
import ZAPCommon
import argparse
import sys
import json
'''
add command git clone origin https://github.com/asadasivan/ZAP_automation.git;cd ZAP_automation;python zapRun.py; to jenkins
'''

def addConfiguration(application):
	ZAP_Common = ZAPCommon.ZAPCommon()
	config = ZAP_Common.config
	application = json.loads(application)
	config['application'] = application
	configFile = open('ZAP_automation/ZAPConfig.json', 'w')
	configFile.write(json.dumps(config))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='install or remove zap')
	parser.add_argument('--config', type=str, default="n",
	                   help='application config')
	args = parser.parse_args()
	if args.config == "n":
		print "needs application config"
		sys.exit(1)
	appData = args.config
	addConfiguration(appData)
	os.system("python ZAP_automation/zapInstallation.py --zap i") #Install ZAP
	#load the session from S3*** in ZAP_manual.py
	os.system("python ZAP_automation/ZAP_manual.py") #spider
	os.system("python ZAP_autonation/ZAP_ActiveScan.py") #active scan
	os.system("python ZAP_autonation/generateReports.py") #generate HTML Report
	#send reports to S3***
	os.system("python ZAP_automation/zapInstallation.py --zap r") #Remove ZAP
