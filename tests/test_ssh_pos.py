import pytest

from sshcheckers import ssh_co, put_files
import yaml

with open("config.yaml") as f:
    data = yaml.safe_load(f)


class TestPositive:
    def save_log(self, starttime, name):
        with open(name, 'w') as f:
            f.write(ssh_co(data["ip"], data["user"], data["passwd"], "journalctl --since '{}'".format(starttime))[1])

    def test_deploy(self, start_journal_time):
        res = []
        put_files(data["ip"], data["user"], data["passwd"], data["lpath"] + data["pkgname"] + ".deb",
                  "/home/{}/{}.deb".format(data["user"], data["pkgname"]))
        res.append(ssh_co(data["ip"], data["user"], data["passwd"], "echo '{}' | sudo -S dpkg -i"
                                                                    " /home/{}/{}.deb".format(data["passwd"],
                                                                                              data["user"],
                                                                                              data["pkgname"]),
                          "Настраивается пакет")[0])
        res.append(ssh_co(data["ip"], data["user"], data["passwd"], "echo '{}' | "
                                                                    "sudo -S dpkg -s {}".format(data["passwd"],
                                                                                                data["pkgname"]),
                          "Status: install ok installed")[0])
        self.save_log(start_journal_time, "log_deploy.txt")
        assert all(res), "test deploy FAIL"

    def test_add(self, ssh_mk_folders, ssh_clean_folders, ssh_mk_files, start_journal_time):
        res1 = ssh_co(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arx2.{}".format(data["folder_in2"],
                                                                                                data["folder_out2"],
                                                                                                data["type"]),
                      "Everything is Ok")[0]
        res2 = ssh_co(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folder_out2"]),
                      "arx2.{}".format(data["type"]))[0]
        self.save_log(start_journal_time, "log_add.txt")
        assert res1 and res2, "test add FAIL"

    def test_extract(self, ssh_mk_folders, ssh_clean_folders, ssh_mk_files,  start_journal_time):
        res = []
        res.append(ssh_co(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arx2.{}".format(data["folder_in2"],
                                                                                                    data["folder_out2"],
                                                                                                    data["type"]),
                          "Everything is Ok")[0])
        res.append(ssh_co(data["ip"], data["user"], data["passwd"], "cd {}; 7z e "
                                                                    "arx2.{} -o{} -y".format(data["folder_out2"],
                                                                                             data["type"],
                                                                                             data["folder_ext2"]),
                          "Everything is Ok")[0])
        for item in ssh_mk_files:
            res.append(ssh_co(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folder_ext2"]), item)[0])
        self.save_log(start_journal_time, "log_extract.txt")
        assert all(res), "test extract FAIL"

    def test_test(self, start_journal_time):
        res = ssh_co(data["ip"], data["user"], data["passwd"], "cd {}; 7z t arx2.{}".format(data["folder_out2"],
                                                                                            data["type"]),
                     "Everything is Ok")[0]
        self.save_log(start_journal_time, "log_test.txt")
        assert res, "test test FAIL"

    def test_update(self, start_journal_time):
        res = ssh_co(data["ip"], data["user"], data["passwd"], "cd {}; 7z u arx2.{}".format(data["folder_in2"],
                                                                                            data["type"]),
                     "Everything is Ok")[0]
        self.save_log(start_journal_time, "log_update.txt")
        assert res, "test update FAIL"

    def test_list(self, ssh_mk_folders, ssh_clean_folders, ssh_mk_files, start_journal_time):
        res = []
        res.append(ssh_co(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arx2.{}".format(data["folder_in2"],
                                                                                                    data["folder_out2"],
                                                                                                    data["type"]),
                          "Everything is Ok")[0])
        for item in ssh_mk_files:
            res.append(ssh_co(data["ip"], data["user"], data["passwd"], "cd {}; 7z l arx2.{}".format(data["folder_out2"],
                                                                                                     data["folder_ext2"],
                                                                                                     data["type"]),
                              item)[0])
        self.save_log(start_journal_time, "log_list.txt")
        assert all(res), "test list FAIL"

    def test_extract2(self, ssh_mk_folders, ssh_clean_folders, ssh_mk_files, ssh_mk_subfolder, start_journal_time):
        res = []
        res.append(ssh_co(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arx2.{}".format(data["folder_in2"],
                                                                                                    data["folder_out2"],
                                                                                                    data["type"]),
                          "Everything is Ok")[0])
        res.append(ssh_co(data["ip"], data["user"], data["passwd"], "cd {}; 7z x arx2.{} -o{} -y".format(
            data["folder_out2"], data["type"], data["folder_ext2"]), "Everything is Ok")[0])

        for item in ssh_mk_files:
            res.append(
                ssh_co(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folder_ext2"]), item)[0])

        res.append(ssh_co(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folder_ext2"]),
                          ssh_mk_subfolder[0])[0])
        res.append(ssh_co(data["ip"], data["user"], data["passwd"], "ls {}/{}".format(data["folder_ext2"],
                                                                                      ssh_mk_subfolder[0]),
                          ssh_mk_subfolder[1])[0])
        self.save_log(start_journal_time, "log_extract2.txt")
        assert all(res), "test extract2 FAIL"

    def test_hash(self, start_journal_time):
        file_hash = ssh_co(data["ip"], data["user"], data["passwd"], f"cd {data['folder_out2']}; "
                                                                         f"crc32 arx2.{data['type']}")[1]
        res = ssh_co(data["ip"], data["user"], data["passwd"], f"cd {data['folder_out2']}; 7z h arx2.{data['type']}",
                     file_hash.upper()[0])
        assert res, "test hash FAIL"

    def test_delete(self, start_journal_time):
        res = ssh_co(data["ip"], data["user"], data["passwd"], "cd {}; 7z d arx2.{}".format(data["folder_out2"],
                                                                                           data['type']),
                     "Everything is Ok")[0]
        self.save_log(start_journal_time, "log_delete.txt")
        assert res, "test delete FAIL"

    def test_clean_deploy(self, ssh_clean_folders, start_journal_time):
        res = []
        res.append(ssh_co(data["ip"], data["user"], data["passwd"], "echo '{}' | sudo -S dpkg -r {}".format(data["passwd"],
                                                                                                     data["pkgname"]),
                   "Удаляется")[0])

        res.append(ssh_co(data["ip"], data["user"], data["passwd"], "echo '{}' | sudo -S dpkg -s {}".format(data["passwd"],
                                                                                                  data["pkgname"]),
                            "Status: deinstall ok")[0])
        assert all(res), "test clean deploy FAIL"
