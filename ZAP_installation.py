#!/usr/bin/python
import os
import sys
import argparse
import ZAPCommon


'''
Install zap
'''
class ZAP_installation:

	def __init__(self):
		ZAP_Common = ZAPCommon.ZAPCommon()
		config = ZAP_Common.config
		self.directory = config['ZAP_info']['ZAP_directory']
		self.zapVersion = config['ZAP_info']['ZAP_version']

	'''
	get the latest release from github, extract files, and save to 'zap' directory
	'''
	def zapInstall(self):
		print "[Info] Installing ZAP..."
		os.system("wget - https://github.com/zaproxy/zaproxy/releases/download/%s/ZAP_%s_Linux.tar.gz"%(self.zapVersion, self.zapVersion))
		os.system("tar zxf ZAP_%s_Linux.tar.gz -C %s"%(self.zapVersion, self.directory))
		os.system("ln -s %sZAP_%s %szap"%(self.directory, self.zapVersion, self.directory))

	'''
	remove tar files, zap directory, and logs
	'''
	def removeZap(self):
		print "[Info] Removing ZAP..."
		os.system("rm -rf %sZAP_%s"%(self.directory,self.zapVersion))
		os.system("rm -rf %szap"%self.directory)
		os.system("rm -rf ZAP_%s_Linux.tar.gz"%self.zapVersion)
		os.system("rm -rf %s.ZAP"%(self.directory))
	
	


'''
install zap by calling ZAP_installation with arg --zap
	--zap i : install zap
	--zap r : remove zap
'''
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='install or remove zap')
	parser.add_argument('--zap', type=str, default="n",
	                   help='install zap: --zap i for installation, --zap r to remove')
	args = parser.parse_args()

	zap_installation = ZAP_installation()

	if args.zap == "i":
		zap_installation.zapInstall()
	elif args.zap == "r":
		zap_installation.removeZap()
	else:
		print "please enter an option --zap i for install or --zap r for remove"
