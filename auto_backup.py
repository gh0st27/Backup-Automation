#!/usr/bin/python
import os
import shutil
import sys
import subprocess
import time
import smtplib
import re
from email.mime.text import MIMEText

class Bak:

	status = 0
	def __init__(self,dst_path,no_of_dir):
		self.dst_path = dst_path
		self.no_of_dir = no_of_dir

	def create_dst_dir_local(self):
		if not os.path.exists(self.dst_path):
			os.makedirs(self.dst_path)
			print 'daily backup directory created'
		else:
			print 'directory daily_backup already present'

	def check(self):
		my_range = self.no_of_dir
		list = range(my_range)
		print 'in check func\n'
		for a in list:
			directory = self.dst_path+'/bak'+str(a)
			if not os.path.exists(directory):
				os.makedirs(directory)
				print directory,"createdddddddddddddddddddd"
				return directory
			else:
				print directory,'already exists'
				Bak.status = Bak.status + 1

	def delete_old_directory(self):
                print 'in del funct'
                os.chdir(self.dst_path)
                files = sorted(os.listdir(os.getcwd()), key=os.path.getctime)
                oldest = files[0]
                del_file = os.path.join(self.dst_path,oldest)
                print 'oldest_fils is:',del_file
		shutil.rmtree(del_file)
                print del_file ,' deleted'


	def check_again(self):
		print 'in check_again fucnt'
		if Bak.status == self.no_of_dir:
			Backup.delete_old_directory()
			my_path2 = Backup.check()
			return my_path2

		else:
			print 'cant delete'


	def move(self,my_path1):
		print 'in move func'
		for root,dir,files in os.walk(self.dst_path):
			for file in files:
			matchObj = re.match(r'.*backup.tar',file)
				if matchObj:
					mat = matchObj.group()
					os.chdir(self.dst_path)
					shutil.move(mat,my_path1)

				else:
					print 'no match'

				break
			break

	def mount(self):
		print 'in mount fuct'
		try:
			mount_output_status = subprocess.check_call('mount xx:xx:xx:xx/location /mount_point_on_local'.split())
		except subprocess.CalledProcessError:
       			return 1
		return  mount_output_status


	def copy_to_nas(self,src,nas_dst,symlinks=False,ignore=None):
		split_path = os.path.split(src)
		delet_path = os.path.join(nas_dst,split_path[1])
		if os.path.exists(delet_path):
			print 'deleting path'
			shutil.rmtree(delet_path)
		else:
			print 'creating first time'

		shutil.copytree(src, delet_path, symlinks, ignore)

	def umount(self):
		print 'in umount fuct'
        	try:
                	unmount_output_status = subprocess.check_call('umount xx:xx:xx:xx/location /mount_point_on_local'.split())
        	except subprocess.CalledProcessError:
                	return 1
       		return unmount_output_status

	def mail(self):
		print 'in mail funct'
		filename = r"/path/to/log_of_this_script"
		print(os.getcwd())
		with open(filename,'rb') as fp:

			msg = MIMEText(fp.read())
			s = smtplib.SMTP('smtp.gmail.com',587) #add your mail server ip/name and port number
			s.starttls()				#start tls mechanism
			s.login('emailID','Passwor')

			msg['Subject'] = 'the backup logs are:'
			msg['From'] = 'from'
			msg['To'] = 'to'
			s.sendmail('from', 'to', msg.as_string())
			fp.close()
			s.quit()

	def ldap(self):

if __name__ =="__main__":
	no_of_dir_for_backup = 3  #Total no of directory for backup
	Backup = Bak(r'/path/to/local_backup_location',no_of_dir_for_backup)  #create instance  with total no of dir and  backup location on local HDD

	Backup.create_dst_dir_local() #calling create_dst_dir_local-- destination directory creation on local
	my_path1 = Backup.check()  #calling check funct--- checking dir alrady present or not
	print "path::::",my_path1  #path to store backup

	checkpoint = 0		      #creating checkpoint
	if my_path1 == None:      #if backup location not available check status
		if Bak.status == no_of_dir_for_backup: #comparing Backup status from check function with no of dir if true
			path = Backup.check_again()  #call check aganin fuction
			print 'my_path1:',path   #Backup path from check again fuction
			checkpoint = 1			# change checkpoint value to find accurate backup path
		else:
			print 'value of Bak_staus is not 2'
	else:
		print 'path is not none'
	#add backup funct here
	print  "calling ldap function"
	#end  backup funct here
	mount_output_status = Backup.mount()  #Mount NAS Directory

	nas_dst = r'/Backup_path_to_remote_NAS_location' #NAS Backup location
	if checkpoint == 0:
		Backup.move(my_path1)   #move backup data on local backup directory
		Backup.copy_to_nas(my_path1,nas_dst) #copy backup directory to NAS location
	elif checkpoint == 1:
		Backup.move(path)
		Backup.copy_to_nas(path,nas_dst)
	else:
		print 'something went wrong'

	unmount_output_status = Backup.umount() #unmount NAS
	Backup.mail()				#calling mail fuct
	sys.exit(1)

if __name__ =="__main__":
	main()

