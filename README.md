## Lazy Colab Cli Portal (LCCP)
This tool is used to build a ssh connection portal to your existing colab.  

### Prerequisite
1. Get a ngrok account (free: https://ngrok.com/)
2. Generate an [access token](https://dashboard.ngrok.com/auth/your-authtoken)  

### Usage
Execute the following script on your colab notebook  
```python
!git clone https://github.com/vashineyu/lazy_colab_cli_portal

from lazy_colab_cli_portal.portal import Portal
import getpass

authtoken = getpass.getpass()
password = [YOUR_PASSWORD]
### it will show up a column for you to fill in your token

portal = Portal(ipy_shell=get_ipython(), password=password, ngrok_auth=authtoken)
```
Then, you can execute ssh .... from your local terminal to the environment.
