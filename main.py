import json
import subprocess
import os


class LoadBalancing:
    F = open('config.json')
    MAX_FILES = 5

    def __init__(self):
        self.json = json.load(self.F)
        self.srv_path = self.json["server"]
        self.batch_dir = self.json["batch_dir"]
        self.autoImport_dir = self.json["autoImport_dir"]
        self.root = self.json["root"]
        self.movefile()

    def movefile(self):

        batch_src = self.root + self.batch_dir
        for srv in self.srv_path:
            dir_srv = srv + self.autoImport_dir
            try:
                scandir = self.scandir(dir_srv)
                for rep in scandir:
                    dest_path = f'{srv}{self.autoImport_dir}/{rep}'
                    if os.path.isdir(dest_path):
                        for file in self.scandir(batch_src):
                            checker = self.check_nb_files(dest_path)
                            if checker:
                                try:
                                    cmd = subprocess.run(f'scp {self.root}{self.batch_dir}/{file} {dest_path}',
                                                         shell=True,
                                                         capture_output=True)
                                    print(cmd.stdout.decode('utf-8'))
                                except:
                                    print(cmd.stderr.decode('utf-8'))

                            else:
                                print(
                                    f'Le repertoire {dest_path} contient 5 /{self.MAX_FILES}')
                                break
            except:
                continue

    def scandir(self, dir):
        try:
            list_dir = os.listdir(dir)
            return list_dir
        except:
            print(f'Le Chemin {dir} est introuvable')

    def check_nb_files(self, dir):
        if os.path.exists(dir):
            d = self.scandir(dir)
            try:
                d.remove('cache')
            except ValueError:
                pass
            nb = len(d)

            if nb < self.MAX_FILES:
                return True
            return False


LoadBalancing()
