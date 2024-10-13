from checkers import co_negative
import yaml

with open("config.yaml") as f:
    data = yaml.safe_load(f)


class TestNegative:

    def test_exec(self, mk_folders, clean_folders, mk_files, mk_bad_arx):
        res = co_negative(f"cd {data['folder_out']}; 7z e {mk_bad_arx} -o{data['folder_ext']} -y", "ERRORS")
        assert res, "test negative exec FAIL"

    def test_test(self, mk_folders, clean_folders, mk_files, mk_bad_arx):
        res = co_negative(f"cd {data['folder_out']}; 7z t {mk_bad_arx}", "ERRORS")
        assert res, "test negative test FAIL"
