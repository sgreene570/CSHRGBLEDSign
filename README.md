# cshrgbledsign

WIP Networked RGB LEDs using Flask and the pi-blaster library.
For wiring, refer to the following image:
http://mitchtech.net/wp-content/uploads/2013/01/raspi_rgb_led-300x194.png
Colors are parsed through the python colour package.
Colors can be passed as Hex Codes(#FFFFFF), rgb values(1, .5, 1), and english phrases("blue").

The included iButton.py script allows for user iButtons to access an LDAP server to find a .colors configuration in user homedirs.
To start the Flask server, sudo su and then type 
<code>
Flask run --host=x.x.x.x --port=80
</code>
To start the iButton script, install the requirements.txt and run the script.
The iButton script will print out recognized iButtons and the corresponding colors that are set.

For CSH members, see the wiki to learn more about current configurations.


