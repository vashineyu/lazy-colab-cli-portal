import os, subprocess
import json, random, string, requests

NGROK_PACK = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip"

def init_portal(password=None, ngrok_auth=None, ipy_shell=get_ipython()):
	assert ngrok_auth is not None, "Get your ngrok auth from https://dashboard.ngrok.com/auth"
	
	### Download NGROK and unpack
	cmds = [
		"wget -q -c -nc {}".format(NGROK_PACK),
		"unzip -qq -n ngrok-stable-linux-amd64.zip",
		"apt install -qq -o=Dpkg::Use-Pty=0 openssh-server pwgen > /dev/null"
	]
	for cmd in cmds:
		subprocess.run(cmd, check=True, shell=True)

	### Use connected-notebook's interactive shell to run portal
	ipy_shell.system_raw('/usr/sbin/sshd -D &')
	### Get password and setup environment
	if password is None:
		password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(16))

	cmds = [
		"echo root:{} | chpasswd".format(password),
		"mkdir -p /var/run/sshd",
		"echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config",
		"echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config",
		"echo 'LD_LIBRARY_PATH=/usr/lib64-nvidia' >> /root/.bashrc",
		"echo 'export LD_LIBRARY_PATH' >> /root/.bashrc",
	]
	for cmd in cmds:
		subprocess.run(cmd, check=True, shell=True)

	### Build up connection
	ipy_shell.system_raw("./ngrok authtoken {} && ./ngrok tcp 22 &".format(ngrok_auth))
	

	resp = requests.get("http://localhost:4040/api/tunnels")
	data = json.loads(resp.content.decode())

	info = data["tunnels"][0]["public_url"].split(":")
	host = "root@{}".format(info[1][2:])
	port = info[2]

	print("Connection Link: ssh -p {} {}".format(port, host))