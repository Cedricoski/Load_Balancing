import json
import subprocess
import time
import os


class LoadBalancing:
    F = open('config.json')
    MAX_FILES = 5

    def __init__(self):
        self.json = json.load(self.F)
        self.srv_path = self.json["server"]
        self.batch_dir = self.json["batch_dir"]
        self.root = self.json["root"]
        self.movefile()

    def ping(self):
        for srv in self.srv_path:
            cmd = subprocess.run(f'ping {srv}', shell=True, capture_output=True, universal_newlines=True)
            print(cmd.stdout)
            time.sleep(4)
            print('ok')

    def movefile(self):
        dir = os.listdir(f'{self.root}{self.batch_dir}')
        for srv in self.srv_path:
            for file in dir:
                nb_files_dest = len(os.listdir(f'{srv}{self.batch_dir}'))
                if nb_files_dest < self.MAX_FILES:
                    cmd = subprocess.run(f'scp {self.root}{self.batch_dir}/{file} {srv}{self.batch_dir}', shell=True,
                                         capture_output=True)

                    print(cmd.stdout.decode('utf-8'))

                else:
                    print(f'Le repertoire {srv}{self.batch_dir} contient {nb_files_dest}/{self.MAX_FILES}')
                    break


LoadBalancing()
