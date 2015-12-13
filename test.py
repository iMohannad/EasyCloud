
import subprocess
import socket
import ipaddress
import apt
import os


subnet = 0
gateway = 0

def install_ansible():
	print "\n\nAnsible will be installed\n\n"

	"""
	sudo apt-get install software-properties-common
	sudo apt-add-repository ppa:ansible/ansible
	sudo apt-get update
	sudo apt-get install ansible"""

	softwareproperties = ["sudo", "apt-get", "install", "software-properties-common", "-y"]
	addrepository = ["sudo", "apt-add-repository", "ppa:ansible/ansible", "-y"]
	update = ["sudo", "apt-get", "update", "-y"]
	ansible = ["sudo", "apt-get", "install", "ansible", "-y"]
	openssh = ["sudo", "apt-get", "install", "openssh-server", "-y"]
	
	
	cache = apt.Cache()
	if  not cache['software-properties-common'].is_installed:
		subprocess.call(softwareproperties)
	if  not cache['openssh-server'].is_installed:
		subprocess.call(openssh)
	if not cache['ansible'].is_installed:
		subprocess.call(addrepository)
		subprocess.call(update)
		subprocess.call(ansible)

	mkdir = ["mkdir", os.path.expanduser("~/.ssh")]
	chmod = ["chmod", "700", os.path.expanduser("~/.ssh")]
	keygen = ["ssh-keygen", "-t", "rsa"]
	

	subprocess.call(mkdir)
	subprocess.call(chmod)
	subprocess.call(keygen)
	

	



def add_cobbler():
	print "\n\nCobbler needs to be installed in order to automate the installation\n\n"
	print "Enter the IP address of cobbler machine"
	print "\n\n***********************************"
	print "Please make sure that Fedora is installed on the target machine"
	print "***********************************\n\n"
	
	username = raw_input("Enter the username of cobbler: ")
	ipcobbler = raw_input("Enter ip address: ")

	while not valid_ip(ipcobbler):
		print "Error: IP is not valid"
		ipcobbler = raw_input("Make sure to enter a valid IP: ")

	sshcopy = ["ssh-copy-id", username + "@" + ipcobbler]
	subprocess.call(sshcopy) 

	sshadd = ["ssh-add"]
	subprocess.call(sshadd)
	

	#ipaddress.ip_network(unicode(get_ip(), "utf-8"))
	"""netmask = raw_input("Enter netmask: ") #
	subnet = raw_input("Enter subnet: ") #
	gateway = raw_input("Enter gateway: ") #
	dns1 = raw_input("Enter dns1: ") #
	dns2 = raw_input("Enter dns2 (leave it empty if you don't have another one: ") #
	range1 = raw_input("Enter range of ip address you want the cloud machine to take (Keep a space between the two ip addresses): ") 
	"""
	subnet = '255.255.0.0'
	netmask = '172.16.0.0'
	gateway = '172.16.0.253'
	dns1 = '172.16.0.1'
	dns2 = '196.1.65.1'
	range1 = '172.16.69.200 172.16.69.230'
	with open('dhcp.template', 'r') as f:
		newlines = []
		for line in f.readlines():
			if 'subnet 172.16.0.0 netmask 255.255.0.0 {' in line:
				newlines.append(line.replace('subnet 172.16.0.0 netmask 255.255.0.0 {', 'subnet '+ netmask+' netmask '+ subnet+' {'))
			elif 'option routers             172.16.0.253;' in line:
				newlines.append(line.replace('option routers             172.16.0.253;', 'option routers             '+gateway+';'))
			elif 'option domain-name-servers 172.16.0.1, 196.1.65.1;' in line:
				if dns2 == '':
					newlines.append(line.replace('option domain-name-servers 172.16.0.1, 196.1.65.1;', 'option domain-name-servers '+dns1+';'))
				newlines.append(line.replace('option domain-name-servers 172.16.0.1, 196.1.65.1;', 'option domain-name-servers '+dns1+','+dns2+';'))
			elif 'option subnet-mask         255.255.0.0;' in line:
				newlines.append(line.replace('option subnet-mask         255.255.0.0;', 'option subnet-mask         '+subnet+';'))
			elif '     range dynamic-bootp        172.16.69.150 172.16.69.200;'in line:
				newlines.append(line.replace('     range dynamic-bootp        172.16.69.150 172.16.69.200;', '     range dynamic-bootp        '+range1+';'))
			else:
				newlines.append(line)
	with open('ansible/dhcp.template', 'w') as f:
		for line in newlines:
			f.write(line)

	with open('ansible/settings', 'r') as f:
		newlines = []
		for line in f.readlines():
			if 'next_server: ' in line:
				newlines.append('next_server: ' + ipcobbler +'\n')
			elif 'server: 0.0.0.0' in line:
				newlines.append('server: ' + ipcobbler +'\n')
			else:
				newlines.append(line)
	with open('ansible/settings', 'w') as f:
		for line in newlines:
			f.write(line)


	with open('ansible/hosts', 'r') as f:
		newlines = []
		for line in f.readlines():
			if '[fedora]' in line:
				newlines.append(line)
				newlines.append(username + '@' + ipcobbler + '\n')
			else:
				newlines.append(line)
	with open('ansible/hosts', 'w') as f:
		for line in newlines:
			f.write(line)


	with open('ansible/group_vars/master.yml', 'r') as f:
		newlines = []
		for line in f.readlines():
			if 'IP_Fedora' in line:
				newlines.append('IP_Fedora: ' + ipcobbler + '\n')
			else:
				newlines.append(line)
	with open('ansible/group_vars/master.yml', 'w') as f:
		for line in newlines:
			f.write(line)



	copyfiles = ['sudo', 'cp', 'ansible/hosts', '/etc/ansible/']
	subprocess.call(copyfiles)
	copyfiles = ['sudo', 'cp', 'ansible/settings', '/etc/ansible/']
	subprocess.call(copyfiles)
	copyfiles = ['sudo', 'cp', 'ansible/cloud_install.yml', '/etc/ansible/']
	subprocess.call(copyfiles)
	copyfiles = ['sudo', 'cp', 'ansible/p1.yml', '/etc/ansible/']
	subprocess.call(copyfiles)
	copyfiles = ['sudo', 'cp', 'ansible/pp2.yml', '/etc/ansible/']
	subprocess.call(copyfiles)
	copyfiles = ['sudo', 'cp', '-r', 'ansible/group_vars', '/etc/ansible/group_vars']
	subprocess.call(copyfiles)
	copyfiles = ['sudo', 'cp', 'ansible/settings', '/etc/ansible/']
	subprocess.call(copyfiles)
	copyfiles = ['sudo', 'cp', 'ansible/iptables', '/etc/ansible/']
	subprocess.call(copyfiles)
	copyfiles = ['sudo', 'cp', 'ansible/config', '/etc/ansible/']
	subprocess.call(copyfiles)
	copyfiles = ['sudo', 'cp', 'ansible/dhcp.template', '/etc/ansible/']
	subprocess.call(copyfiles)
	copyfiles = ['sudo', 'cp', 'ansible/ubuntu-server-14.04-unattended-cobbler.seed', '/etc/ansible/']
	subprocess.call(copyfiles)
	copyfiles = ['sudo', 'cp', 'ansible/ubuntu-14.04.3-server-amd64.iso', '/etc/ansible/']
	subprocess.call(copyfiles)


	fileCobbler = '/etc/ansible/p1.yml'
	addcobblerAnsible = ['ansible-playbook', fileCobbler, '--ask-sudo-pass']
	subprocess.call(addcobblerAnsible)
	#download cobbler
	#ansiblecobbler = ["", ""]
	#subprocess.call(ansiblecobbler)



def hello_message():
	print
	print "###########################################################"
	print "#                      EasyCloud                          #"
	print "###########################################################"

	print "\nHello there!! EasyCloud will be install on this computer"
	print "IP of this computer is " + get_ip()

def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	ip = s.getsockname()[0]
	s.close()
	return ip


def valid_ip(address):
    try: 
        socket.inet_aton(address)
        return True
    except:
        return False



def add_master():

	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print "                Install Master                      "
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

	ipMaster = get_ip()
	with open('ansible/hosts', 'r') as f:
		newlines = []
		for line in f.readlines():
			if '[master]' in line:
				newlines.append(line)
				newlines.append('easycloud@' + ipMaster)
			else:
				newlines.append(line)
	with open('ansible/hosts', 'w') as f:
		for line in newlines:
			f.write(line)

	with open('ansible/group_vars/master.yml', 'r') as f:
		newlines = []
		for line in f.readlines():
			if 'Master' in line:
				newlines.append('IP_Master: ' + ipMaster + '\n')
			else:
				newlines.append(line)
	with open('ansible/group_vars/master.yml', 'w') as f:
		for line in newlines:
			f.write(line)

	copyfiles = ['sudo', 'cp', 'ansible/hosts', '/etc/ansible/']
	subprocess.call(copyfiles)

	copyfiles = ['sudo', 'cp', '-r', 'ansible/group_vars', '/etc/ansible/']
	subprocess.call(copyfiles)
	subprocess.call(['sudo', './Master.sh'])



def add_node():
	nodeip = raw_input("Enter the Node IP you want to add: ")
	nodemac = raw_input("Enter the MAC of the NODE: ")

	with open('ansible/group_vars/master.yml', 'r') as f:
		newlines = []
		for line in f.readlines():
			if 'Node' in line:
				newlines.append('IP_Node: ' + nodeip + '\n')
			elif 'Host_MAC' in line:
				newlines.append('Host_MAC: ' + nodemac + '\n')
			elif 'Subnet' in line:
				newlines.append('Subnet: ' + subnet + '\n')
			elif 'Gateway' in line:
				newlines.append('IP_Gateway: ' + gateway)
			else:
				newlines.append(line)
	with open('ansible/group_vars/master.yml', 'w') as f:
		for line in newlines:
			f.write(line)


	print
	copyfiles = ['sudo', 'cp', '-r', 'ansible/group_vars', '/etc/ansible/']
	subprocess.call(copyfiles)

	fileCobbler = '/etc/ansible/p1.yml'
	addcobblerAnsible = ['ansible-playbook', fileCobbler, '--ask-sudo-pass']
	subprocess.call(addcobblerAnsible)


if __name__ == "__main__":
	hello_message()

	print "Choose an option:"
	print "1. Install EasyCloud (Ansible, cobbler, and Master Node)"
	print "2. Add new node"
	option = int(raw_input("Choose an option: "))
	if option == 1:
		install_ansible()
		add_cobbler()
		add_master()
	elif option == 2:
		add_node()

	else:
		print "Option is not valid"
