# cshrgbledsign (aka MOLS)

WIP Networked RGB LEDs using Flask and the pi-blaster library.
<br>
# Base Setup
To set up the LEDs and other hardware, refer to [this wiring diagram.](http://mitchtech.net/wp-content/uploads/2013/01/raspi_rgb_led-300x194.png)
<br>
Before starting the flask server, ensure that [pi-blaster](https://github.com/sarfata/pi-blaster) is properly installed.
<br>
Colors are parsed through the [python colour package.](https://pypi.python.org/pypi/colour)
<br>
For example, colors can be passed as Hex Codes(<code>#FFFFFF</code>), rgb values(<code>1, .5, 1</code>), and english phrases(<code>"blue"</code>).
<br>
# Using iButtons
The included iButton.py script allows for user iButtons to access an LDAP server to find a .colors configuration stored in user homedirs on a file system.
This particular project relies on the CSH LDAP python library which was explicitly written for CSH([Computer Science House](http:csh.rit.edu)) members.
CSH LDAP credentials are stored outisde of the python script for obvious security reasons.
<br>
To install the iButton script requirements, type the following:
<br>
<code>
pip -r install requirements.txt
</code>
<br>
The iButton script will print out recognized iButtons and the corresponding colors that are set.
For CSH members, see the wiki to learn more about on floor LED setups.
# Running the Flask Server
To start the Flask server, sudo su and then type 
<br>
<code>
Flask run --host=0.0.0.0 --port=80
</code>
<br>
