import os
import time
import RPi.GPIO as GPIO
import credentials as login
import ldap
GPIO.setmode(GPIO.BCM)
import colorhandler


def find_user(varID, cache={}):
    ibutton = varID.strip()
    if ibutton in cache:
        return cache[ibutton]

    try:
    #conn = ldap.initialize(login.ldap_server, bytes_mode=True)
        conn = ldap.initialize(login.ldap_server)
        conn.simple_bind_s(login.ldap_user, login.ldap_pass)
        ldap_results = conn.search_s('ou=Users,dc=csh,dc=rit,dc=edu',
            ldap.SCOPE_SUBTREE, "(*ibutton=%s)" % ibutton, ['uid', 'homeDirectory'])
        print('(ibutton=%s)' % ibutton)
        return ldap_results[0][1]['homeDirectory'][0]
    except Exception as e:
        print(e)
        return None


def get_ibutton():
    GPIO.setup(27,GPIO.OUT)
    base_dir = '/sys/devices/w1_bus_master1/w1_master_slaves'
    delete_dir = '/sys/devices/w1_bus_master1/w1_master_remove'
    GPIO.output(27,True)
    startTime = time.time()

    while True:
        data = open(base_dir, "r")
        ibutton = data.read()
        ibutton = ibutton.strip()
        data.close()
        if ibutton != 'not found.\n':
            GPIO.output(27,False)
            time.sleep(3)
            print(ibutton)
            try:
                user_dir = find_user("67" + ibutton[3:] + "01")
                if user is None:
                    print("User not found")
                else:
                    find_colors(user_dir)

            except Exception as e:
                print(e)

            d = open(delete_dir, "w")
            d.write(ibutton)
            GPIO.output(27, True)

    d.close()
    GPIO.cleanup()


def find_colors(user_dir):
    cfile = os.path.join(userDir, ".color")


if __name__ == "__main__":
    main()
