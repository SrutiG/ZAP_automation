import os
import ZAPCommon
import argparse
import sys
'''
add command git clone origin https://github.com/asadasivan/ZAP_automation.git;cd ZAP_automation;python zapRun.py; to jenkins
'''
ZAP_Common = ZAPCommon.ZAPCommon()

def addConfiguration(application):
	config = ZAP_Common.config
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
	appData = args.application
	addConfiguration(application)
	os.system("python ZAP_automation/zapInstallation.py --zap i") #Install ZAP
	ZAP_Common.startZap() #start zap
	#load the session from S3*** in ZAP_manual.py
	os.system("python ZAP_automation/ZAP_manual.py") #spider
	os.system("python ZAP_automation/ZAP_ActiveScan.py") #active scan
	os.system("python ZAP_automation/generateReports.py") #generate HTML Report
	#send reports to S3***
	ZAP_Common.stopZap()
	os.system("python ZAP_automation/zapInstallation.py --zap r") #Remove ZAP
	os.system("rm -rf ZAP_automation")