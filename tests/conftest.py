from checkers import co
from datetime import datetime
import string, random
import yaml, pytest

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
