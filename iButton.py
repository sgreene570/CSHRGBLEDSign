import os
import time
import csh_ldap as ldap
import login


def main():
    global cshldap
    cshldap  = ldap.CSHLDAP(login.ldap_user, login.ldap_pass)
    get_ibutton()


def find_user(varID):
    ibutton = varID.strip()
    ibutton = "*" + ibutton[3:] + "01"

    try:
        member = cshldap.get_member_ibutton(ibutton)
        return member.homeDirectory
    except Exception as e:
        print(e)
        return None


def get_ibutton():
    base_dir = '/sys/devices/w1_bus_master1/w1_master_slaves'
    delete_dir = '/sys/devices/w1_bus_master1/w1_master_remove'
    while True:
        data = open(base_dir, "r")
        ibutton = data.read()
        ibutton = ibutton.strip()
        data.close()
        d = open(delete_dir, "w")
        if ibutton != "not found.":
            print(ibutton)
            d.write(ibutton)
            d.flush()
            try:
                find_colors(find_user(ibutton))
            except Exception as e:
                print(e)

        time.sleep(3)

    d.close()


def find_colors(user_dir):
    if user_dir is not None:
        cfile = os.path.join(user_dir, ".colors")
        temp = os.popen("ssh -i /home/sgreen/.ssh/id_rsa "
             + login.file_server + " cat " + cfile)
        colors =  temp.read().split()
        temp.close()
        for line in colors:
            if(line[:5] is "delay"):
                time.sleep(float(line[7:]))
            else:
                print(line)
                os.system("curl -X POST -d 'color=" + line +
                "' localhost:80")


if __name__ == "__main__":
    main()
