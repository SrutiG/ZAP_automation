import os
import ZAPCommon
import argparse
import sys
import json
'''
add command: rm -rf ZAP_automation; pip install requests; git clone https://github.com/SrutiG/ZAP_automation.git; python ZAP_automation/ZAP_run.py --config $APP_INFO;
where $APP_INFO is a parameter defined in jenkins: a json object for the key "application" in the config file.
'''
ZAP_Common = ZAPCommon.ZAPCommon()

#add the custom configuration to the config file
def addConfiguration(application):
	config = ZAP_Common.config
	application = json.loads(application)
	config['application'] = application
	configFile = open('ZAP_automation/ZAPconfig.json', 'w')
	configFile.write(json.dumps(config))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='json object with application configuration')
	parser.add_argument('--config', type=str, default="n",
	                   help='application config')
	args = parser.parse_args()
	if args.config == "n":
		print "needs application config"
		sys.exit(1)
	appData = args.config

	#add the parameters to run the scan
	addConfiguration(appData)
	os.system("python ZAP_automation/ZAP_installation.py --zap i") #Install ZAP
	ZAP_Common.startZap() #start ZAP
	#load the session from S3*** in ZAP_manual.py
	os.system("python ZAP_automation/ZAP_manual.py --session y") #spider/set up zap
	os.system("python ZAP_automation/ZAP_ActiveScan.py") #active scan
	os.system("python ZAP_automation/generateReports.py") #generate HTML Report
	#send reports to S3***
	ZAP_Common.stopZap() #shutdown ZAP server
	os.system("python ZAP_automation/ZAP_installation.py --zap r") #Remove ZAP
	os.system("rm -rf ZAP_automation")

