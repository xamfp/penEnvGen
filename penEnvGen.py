#!/usr/bin/env python2
import sys
import os
sys.path.append('lib' + os.sep + 'Sublist3r')
import shutil
import random
import uuid
import re
import base64
import sublist3r

class PenEnvGen:
    def __init__(self):
        self.VERSION = "1.0.0 Alpha"

    def Main(self):
        try:
            print(self.banner(self.VERSION))
            self.TARGET = sys.argv[1]
            self.generate_Init_workspace(self.TARGET)
            self.subdomain_search(self.TARGET)
            self.generate_Sub_workspace(self.TARGET)
            self.nmap_subdomains()
        except KeyboardInterrupt:
            os._exit(1)

    def subdomain_search(self, target):
        print("[~] Scanning for subdomains. This may take a moment...")
        subdomains = sublist3r.main(target, 40,'Workspaces/{0}/Recon/subdomain-scan.txt'.format(self.TARGET), ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
    def nmap_subdomains(self):
        with open("Workspaces/{0}/Recon/subdomain-scan.txt".format(self.TARGET)) as sub_workspaces:
            print("[~] Preforming port scan on {}".format(self.TARGET))
            os.system("nmap -Pn {0} -oN Workspaces/{1}/Recon/nmap-scan.txt >> /dev/null".format(self.TARGET, self.TARGET))
            print("[-] Saving portscan to Workspaces/{1}/Recon/nmap-scan.txt".format(self.TARGET, self.TARGET))

            for subdomain in sub_workspaces.read().strip().split("\r\n"):
                print("[~] Preforming port scan on {}".format(subdomain))
                os.system("nmap -Pn {0} -oN Workspaces/{1}/Subdomains/{2}/Recon/nmap-scan.txt >> /dev/null".format(subdomain, self.TARGET, subdomain))
                print("[-] Saving portscan to Workspaces/{0}/Subdomains/{1}/Recon/nmap-scan.txt".format(self.TARGET, subdomain))
    def delete_Workspace(self):
        if self.TARGET == "All" and self.TARGET != "":
            del_confirm = self.y_n_prompt("[!] Are you sure you want to delete all of your workspaces?")
            self.TARGET = ""
            if del_confirm.lower() == "y":
                try:
                    shutil.rmtree("Workspaces")
                except Exception as e:
                    if "OSError: [Errno 2] No such file or directory:" in str(e):
                        pass
                os.remove('.workspaces')
                print("[!] All Workspaces Deleted!")
        if os.path.exists("Workspaces/" + self.TARGET) and self.TARGET != "":
            del_confirm = self.y_n_prompt("[!] Are you sure you want to delete {} from your workspaces?".format(self.TARGET))
            if del_confirm.lower() == "y":
                try:
                    shutil.rmtree("Workspaces/{}".format(self.TARGET))
                except Exception as e:
                    if "OSError: [Errno 2] No such file or directory:" in str(e):
                        pass
                os.remove('.workspaces')
                print("[!] Workspace '{}' has been Deleted!".format(self.TARGET))
                self.TARGET = ""
        else:
            print("[!] Workspace doesn't exist")

    def generate_Init_workspace(self, target):
        default_folders = ["Recon", "Payloads", "Exploits", "Loot"]
        for folder in default_folders:
            try:
                os.makedirs("Workspaces" + os.sep + target + os.sep + folder)
                print("[+] Directory Created: {}".format("Workspaces" + os.sep + target + os.sep + folder))
            except Exception as e:
                if 'OSError: [Errno 17] File exists' in str(e):
                    pass
        with open("Workspaces" + os.sep + target + os.sep + "notes.txt", "a+") as workspace_notes:
            with open("Workspaces" + os.sep + target + os.sep + "notes.txt", "r") as workspace_read:
                if "### Notes for: {}\r\n".format(target) in workspace_read.read():
                    pass
                else:
                    workspace_notes.write("### Notes for: {}\r\n".format(target))
                    print("[+] File Created: {}".format("Workspaces" + os.sep + target + os.sep + "notes.txt"))

    def generate_Sub_workspace(self, target):
        default_folders = ["Recon", "Payloads", "Exploits", "Loot"]
        with open("Workspaces/{0}/Recon/subdomain-scan.txt".format(target)) as sub_workspaces:
            for subdomain in sub_workspaces.read().strip().split("\r\n"):
                for folder in default_folders:
                    try:
                        os.makedirs("Workspaces" + os.sep + target + os.sep + "Subdomains" + os.sep + subdomain)
                        print("[+] Directory Created: {}".format("Workspaces" + os.sep + target + os.sep + "Subdomains" + os.sep + subdomain))
                        for def_folder in default_folders:
                            os.makedirs("Workspaces" + os.sep + target + os.sep + "Subdomains" + os.sep + subdomain + os.sep + def_folder)
                            print("[+] Directory Created: {}".format("Workspaces" + os.sep + target + os.sep + "Subdomains" + os.sep + subdomain + os.sep + def_folder))
                            with open("Workspaces" + os.sep + target + os.sep + "Subdomains" + os.sep + subdomain + os.sep + "notes.txt", "a+") as workspace_notes:
                                with open("Workspaces" + os.sep + target + os.sep + "Subdomains" + os.sep + subdomain + os.sep + "notes.txt", "r") as workspace_read:
                                    if "### Notes for: {}\r\n".format(subdomain) in workspace_read.read():
                                        pass
                                    else:
                                        workspace_notes.write("### Notes for: {}\r\n".format(subdomain))
                                        print("[+] File Created: {}".format("Workspaces" + os.sep + target + os.sep + "Subdomains" + os.sep + subdomain + os.sep + "notes.txt"))
                    except Exception as e:
                        if 'OSError: [Errno 17] File exists' in str(e):
                            pass
            '''
            with open("Workspaces" + os.sep + target + os.sep + subdomain + os.sep + "notes.txt", "a+") as workspace_notes:
                with open("Workspaces" + os.sep + target + os.sep + subdomain + os.sep +  "notes.txt", "r") as workspace_read:
                    if "### Notes for: {} \r\n".format(target) in workspace_read.read():
                        pass
                    else:
                        workspace_notes.write("### Notes for: {} \r\n".format(subdomain))
                        print("lololol: {}".format("Workspaces" + os.sep + target + os.sep + subdomain + os.sep + "notes.txt"))
            '''


    def banner(self, version):
        Logos = ['DQogICAgICAgICAgICAgKGBgJywNCiAgICAgICAgICAgIC8gYCcnLw0KICAgICAgICAgICAvICAgIC8NCiAgICAgICAgT1wvICAgIC8NCiAgICAgICAgXCwgICAgLw0KICAgICAgICAoICAgIC8gICAgICAgICAgICAgIFBlbmV0cmF0aW9uIFRlc3RpbmcgRW52aXJvbm1lbnQgR2VuZXJhdG9yDQogICAgICAgL3hgJyc3LyAgICAgICAgICAgICAgVmVyc2lvbjogMS4wLjAgQWxwaGENCiAgICAgICh4ICAgLy9gXCAgICAgICAgIA0KICAgICAvIGAnJzcnYFwgXA0KICAgIC8gICAgLyAgIC8oKVwNCiAgICggICAgLyAgIGB8fn58YA0KICAgIGAnJycgICAgIHwgIHwNCiAgICAgICAgICAgICB8ICB8DQogICAgICAgICAgICAgfCAgfA0KICAgICAgICAgICAgIHwgIHwNCiAgICAgICAgICAgICB8ICB8DQogICAgICAgICAgIC9gICAgIGBcDQogLC0tLS0tLS0nYCAgICAgICAgYCctLS0tLS0tLA0KYH5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5g','ICAgICAgLC0uDQogICAgIC8gXCAgYC4gIF9fLi4tLE8NCiAgICA6ICAgXCAtLScnXy4uLScuJyAgICAgICAgICAgUGVuZXRyYXRpb24gVGVzdGluZyBFbnZpcm9ubWVudCBHZW5lcmF0b3INCiAgICB8ICAgIC4gLi0nIGAuICcuICAgICAgICAgICAgVmVyc2lvbjogezB9DQogICAgOiAgICAgLiAgICAgLmAuJw0KICAgICBcICAgICBgLiAgLyAgLi4NCiAgICAgIFwgICAgICBgLiAgICcgLg0KICAgICAgIGAsICAgICAgIGAuICAgXA0KICAgICAgLHwsYC4gICAgICAgIGAtLlwNCiAgICAgJy58fCAgYGAtLi4uX18uLi1gDQogICAgICB8ICB8DQogICAgICB8X198DQogICAgICAvfHxcDQogICAgIC8vfHxcXA0KICAgIC8vIHx8IFxcDQogX18vL19ffHxfX1xcX18NCictLS0tLS0tLS0tLS0tLSc=','ICAgICAgICAgICAgIF9fX19fXw0KICAgICAgICAgICwnIiAgICAgICAiLS5fDQogICAgICAgICwnICAgICAgICAgICAgICAiLS5fIF8uXw0KICAgICAgICA7ICAgICAgICAgICAgICBfXywtJy8gICB8DQogICAgICAgO3wgICAgICAgICAgICwtJyBfLCciJy5fLC4NCiAgICAgICB8OiAgICAgICAgICAgIF8sJyAgICAgIHxcIGAuDQogICAgICAgOiBcICAgICAgIF8sLScgICAgICAgICB8IFwgIGAuICAgICAgICAgUGVuZXRyYXRpb24gVGVzdGluZyBFbnZpcm9ubWVudCBHZW5lcmF0b3INCiAgICAgICAgXCBcICAgLC0nICAgICAgICAgICAgIHwgIFwgICBcICAgICAgICBWZXJzaW9uOiAxLjAuMCBBbHBoYQ0KICAgICAgICAgXCAnLiAgICAgICAgIC4tLiAgICAgfCAgICAgICBcICAgICANCiAgICAgICAgICBcICBcICAgICAgICAgIiAgICAgIHwgICAgICAgIDoNCiAgICAgICAgICAgYC4gYC4gICAgICAgICAgICAgIHwgICAgICAgIHwNCiAgICAgICAgICAgICBgLiAiLS5fICAgICAgICAgIHwgICAgICAgIDsNCiAgICAgICAgICAgICAvIHxgLl8gYC0uXyAgICAgIEwgICAgICAgLw0KICAgICAgICAgICAgLyAgfCBcIGAuXyAgICItLl9fXyAgICBfLCcNCiAgICAgICAgICAgLyAgIHwgIFxfLi0iLS5fX18gICAiIiIiDQogICAgICAgICAgIFwgICA6ICAgICAgICAgICAgLyIiIg0KICAgICAgICAgICAgYC5fXF8gICAgICAgX18uJ18NCiAgICAgICBfXywtLScnXyAnICItLScnJycgXF8gIGAtLl8NCiBfXywtLScgICAgIC4nIC9fICB8ICAgX18uIGAtLl8gICBgLS5fDQo8ICAgICAgICAgICAgYC4gIGAtLi0nJyAgX18sLScgICAgIF8sLScNCiBgLiAgICAgICAgICAgIGAuICAgXywtJyIgICAgICBfLC0nDQogICBgLiAgICAgICAgICAgICcnIiAgICAgICBfLC0nDQogICAgIGAuICAgICAgICAgICAgICAgIF8sLScNCiAgICAgICBgLiAgICAgICAgICBfLC0nDQogICAgICAgICBgLiAgIF9fLCciDQogICAgICAgICAgIGAnIg=='] 
        return base64.b64decode(random.choice(Logos)).decode('utf-8').format(version)



if __name__ == "__main__":
    EnvGen = PenEnvGen()
    EnvGen.Main()
    
