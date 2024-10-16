from checkers import co
from sshcheckers import ssh_co

from datetime import datetime

import string, random
import yaml, pytest
import subprocess

with open("config.yaml") as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def mk_folders():
    return co(f"mkdir {data['folder_in']} {data['folder_out']} {data['folder_ext']}", "")


@pytest.fixture()
def clean_folders():
    return co(f"rm -rf {data['folder_in']}/* {data['folder_out']}/* {data['folder_ext']}/*", "")


@pytest.fixture()
def mk_files():
    list_files = []
    for i in range(data["number_files"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if co(f"cd {data['folder_in']}; dd if=/dev/urandom of={filename} bs={data['bs']} count=1 iflag=fullblock", ""):
            list_files.append(filename)
    return list_files


@pytest.fixture()
def mk_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    if not co(f"cd {data['folder_in']}; mkdir -v {subfoldername}", "создан каталог"):
        return None, None
    if not co(
            f"cd {data['folder_in']}/{subfoldername}; dd if=/dev/urandom of={testfilename} bs=1M count=1 iflag=fullblock",
            ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture()
def mk_bad_arx():
    co(f"cd {data['folder_in']}; 7z a {data['folder_out']}/barx.{data['type']} -t{data['type']}", "Everything is Ok")
    co(f"truncate -s 1 {data['folder_out']}/barx.{data['type']}")
    yield f"barx.{data['type']}"
    co(f"rm -f {data['folder_out']}/barx.{data['type']}")


@pytest.fixture(autouse=True)
def get_stat():
    yield
    stat = subprocess.run("cat /proc/loadavg", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    co(f"echo 'time: {datetime.now().strftime('%H:%M:%S.%f')} count:{data['number_files']} size: {data['bs']} load: {stat.stdout}'>> stat.txt")


@pytest.fixture()
def ssh_mk_folders():
    return ssh_co(data["ip"], data["user"], data["passwd"],
                  "mkdir {} {} {}".format(data["folder_in2"], data["folder_out2"], data["folder_ext2"]), "")[0]


@pytest.fixture()
def ssh_clean_folders():
    return ssh_co(data["ip"], data["user"], data["passwd"],
                        "rm -rf {}/* {}/* {}/*".format(data["folder_in2"], data["folder_out2"],
                                                            data["folder_ext2"]), "")[0]


@pytest.fixture()
def ssh_mk_files():
    list_of_files = []
    for i in range(data["number_files"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_co(data["ip"], data["user"], data["passwd"],
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in2"],
                                                                                               filename, data['bs']), "")[0]:
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def ssh_mk_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    if not ssh_co(data["ip"], data["user"], data["passwd"],
                        "cd {}; mkdir {}".format(data["folder_in2"], subfoldername), "")[0]:
        return None, None
    if not ssh_co(data["ip"], data["user"], data["passwd"],
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in2"],
                                                                                                  subfoldername,
                                                                                                  testfilename), "")[0]:
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def ssh_mk_bad_arx():
    ssh_co(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arxbad -t{}".format(data["folder_in2"],
                                                                                               data["folder_out2"],
                                                                                               data["type"]),
                 "Everything is Ok")[0]
    ssh_co(data["ip"], data["user"], data["passwd"], "truncate -s 1 {}/arxbad.{}".format(data["folder_out2"],
                                                                                               data["type"]),
                 "Everything is Ok")[0]
    yield "arxbad"
    ssh_co(data["ip"], data["user"], data["passwd"],
                 "rm -f {}/arxbad.{}".format(data["folder_out2"], data["type"]), "")[0]


@pytest.fixture()
def start_journal_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
