import subprocess
import string


# import paramiko


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def find_input(cmd, text):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    if res.returncode == 0:
        return text in res.stdout
    else:
        return "FAIL"


def find_word(cmd, text, words=False):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    if res.returncode == 0:
        out = res.stdout
        if words:
            lst = out.translate(str.maketrans('', '', string.punctuation)).split()
            return text in lst
        else:
            return text in out
    else:
        return "FAIL"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    flag = find_input('ls /etc', 'fonts')
    print(flag)

    flag = find_input('cat /etc/fprintd.conf', 'storage')
    print(flag)

    flag = find_word('ls /etc', 'fonts', words=True)
    print(flag)

    flag = find_word('cat /etc/fprintd.conf', 'storage', words=True)
    print(flag)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
