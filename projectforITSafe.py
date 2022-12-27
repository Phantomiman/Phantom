from samsfunction import importer

user = "Phantomiman"
password = "S3cN4t"


list = {'username':"Phantomiman",'password':"S3cN4t"}

class myf(object):
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def get_user(self):
        print("[+] Greetings your user is {0}".format(self.user))
    def get_password(self):
        print("[!] Don't share or save your password {0}".format(self.password))
    def logger(self,user , password):
        print("""-------- Robot Validation Interface ---------
        Please Type Your User And Your Password""")

        usercheck = input("ID : ")
        passwordcheck = input("Password : ")
        if usercheck and passwordcheck in list.values():
            print("[+] Logged In ")
            importer()
        else:
            print("[-] Please try again, user or password are incorrect")

caller = myf(user, password)
caller.get_user()
caller.get_password()
caller.logger(user, password)