from checkers import co
import subprocess

folder_in = "/home/user/tst"
folder_out = "/home/user/out"
folder_ext = "/home/user/folder1"
folder_ext2 = "/home/user/folder2"


def test_add():
    res1 = co(f"cd {folder_in}; 7z a {folder_out}/arx2.7z",
              "Everything is Ok")
    res2 = co(f"ls {folder_out}", "arx2.7z")
    assert res1 and res2, "test add FAIL"


def test_extract():
    res1 = co(f"cd {folder_out}; 7z e arx2.7z -o{folder_ext} -y",
              "Everything is Ok")
    res2 = co(f"ls {folder_ext}", "testfile.txt")
    assert res1 and res2, "test extract FAIL"


def test_test():
    assert co(f"cd {folder_out}; 7z t arx2.7z", "Everything is Ok")
    "test test FAIL"


def test_update():
    assert co(f"cd {folder_out}; 7z u arx2.7z",
              "Everything is Ok")
    "test update FAIL"


def test_list():
    res1 = co(f"cd {folder_out}; 7z l arx2.7z", "testfile.txt")
    res2 = co(f"cd {folder_out}; 7z l arx2.7z", "testfile2.txt")
    assert res1 and res2, "test list FAIL"


def test_extract2():
    res1 = co(f"cd {folder_out}; 7z x arx2.7z -o{folder_ext2} -y",
              "Everything is Ok")
    res2 = co(f"ls {folder_ext2}", "testfile2.txt")
    res3 = co(f"ls {folder_ext2}", "testdir")
    assert res1 and res2 and res3, "test extract2 FAIL"


def test_hash():
    file_hash = subprocess.run(f"d {folder_out}; crc32 arx2.7z", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    res = co(f"cd {folder_out}; 7z h arx2.7z", file_hash.stdout.upper())
    assert res, "test hash FAIL"


def test_delete():
    assert co(f"cd {folder_out}; 7z d arx2.7z", "Everything is Ok")
    "test delete FAIL"
