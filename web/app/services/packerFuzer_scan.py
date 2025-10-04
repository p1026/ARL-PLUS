import json
import os
import time

from app import utils
from .baseThread import BaseThread
from app.arlconfig import Config
import requests.exceptions

logger = utils.get_logger()


def delete_files_in_directory(directory_path):
    try:
        for root, dirs, files in os.walk(directory_path, topdown=False):
            for filename in files:
                file_path = os.path.join(root, filename)
                if filename != "arl_update.lock":
                    os.remove(file_path)
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)
    except Exception as e:
        pass


class Packerzuuer(BaseThread):
    def __init__(self, urls, result_file, concurrency=10):
        super().__init__(urls, concurrency=concurrency)
        self.result_file = result_file
        self.result = {}

    def work(self, url):
        try:
            command = ["/root/miniconda3/envs/arl/bin/python", Config.PackerFuzzer_PATH,
                       "-u", url,
                       "-o", self.result_file]
            logger.info(" ".join(command))
            utils.exec_system(command, timeout=24 * 60 * 60)
        except requests.exceptions.RequestException as e:
            pass
        except Exception as e:
            pass

    def run(self):
        t1 = time.time()
        logger.info("start PackerFuzzer {}".format(len(self.targets)))
        self._run()
        if os.path.exists(Config.PFresult_PATH + f"/{self.result_file}_result.json"):
            out = open(Config.PFresult_PATH + f"/{self.result_file}_result.json", 'r').read()
            out = out[:-1]
            if out != '':
                self.result["data"] = out
            else:
                self.result["data"] = ''
        logger.info(f'PFZ run end')
        return self.result


def Packerzuuer_scan(urls, result_file, concurrency=20):
    c = Packerzuuer(urls, result_file, concurrency)
    return c.run()
