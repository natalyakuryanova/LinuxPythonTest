from checkers import co
import subprocess
import yaml, pytest

with open("config.yaml") as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_add(self, mk_folders, clean_folders, mk_files):
        res = []
        res.append(co(f"cd {data['folder_in']}; 7z a {data['folder_out']}/{data['arx_name']}", "Everything is Ok"))
        res.append(co(f"ls {data['folder_out']}", data['arx_name']))
        assert all(res), "test add FAIL"

    def test_extract(self, mk_folders, clean_folders, mk_files):
        res = []
        res.append(co(f"cd {data['folder_in']}; 7z a {data['folder_out']}/{data['arx_name']}", "Everything is Ok"))
        res.append(co(f"cd {data['folder_out']}; 7z e {data['arx_name']} -o{data['folder_ext']} -y", "Everything is Ok"))
        for item in mk_files:
            res.append(co(f"ls {data['folder_ext']}", item))
        assert all(res), "test extract FAIL"

    def test_test(self):
        assert co(f"cd {data['folder_out']}; 7z t {data['arx_name']}", "Everything is Ok"), "test test FAIL"

    def test_update(self):
        assert co(f"cd {data['folder_out']}; 7z u {data['arx_name']}", "Everything is Ok"), "test update FAIL"

    def test_list(self, mk_folders, clean_folders, mk_files):
        res = []
        res.append(co(f"cd {data['folder_in']}; 7z a {data['folder_out']}/{data['arx_name']}", "Everything is Ok"))
        for item in mk_files:
            res.append(co(f"cd {data['folder_out']}; 7z l {data['arx_name']}", item))
        assert all(res), "test list FAIL"

    def test_extract2(self, mk_folders, clean_folders, mk_files, mk_subfolder):
        res = []
        res.append(co(f"cd {data['folder_in']}; 7z a {data['folder_out']}/{data['arx_name']}", "Everything is Ok"))
        res.append(co(f"cd {data['folder_out']}; 7z x {data['arx_name']} -o{data['folder_ext']} -y", "Everything is Ok"))
        for item in mk_files:
            res.append(co(f"ls {data['folder_ext']}", item))

        res.append(co(f"ls {data['folder_ext']}", mk_subfolder[0]))
        res.append(co(f"ls {data['folder_ext']}/{mk_subfolder[0]}", mk_subfolder[1]))
        assert all(res), "test extract2 FAIL"

    def test_hash(self):
        file_hash = subprocess.run(f"d {data['folder_out']}; crc32 {data['arx_name']}", shell=True, stdout=subprocess.PIPE,
                                   encoding='utf-8')
        res = co(f"cd {data['folder_out']}; 7z h {data['arx_name']}", file_hash.stdout.upper())
        assert res, "test hash FAIL"

    def test_delete(self):
        assert co(f"cd {data['folder_out']}; 7z d {data['arx_name']}", "Everything is Ok")
        "test delete FAIL"
