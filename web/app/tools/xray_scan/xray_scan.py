import json
import os.path
import subprocess

from app.arlconfig import Config
from app import utils

logger = utils.get_logger()

import asyncio


async def run_command(command, timeout):
    process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.PIPE)
    try:
        # 读取输出流
        while True:
            line = await asyncio.wait_for(process.stdout.readline(), timeout=timeout)
            if not line:
                break
            logger.info(line.decode().strip())

        # 等待子进程完成
        await asyncio.wait_for(process.wait(), timeout=timeout)
    except asyncio.TimeoutError:
        process.terminate()
        logger.info("Timeout exit!")


async def xray(xray_path, result):
    command = f'{xray_path} webscan --listen 127.0.0.1:7777 --json-output {result}'
    logger.info(command)
    timeout = 180  # 十秒钟
    await run_command(command, timeout)


async def rad(rad_path, targets):
    await asyncio.sleep(60)
    logger.info('wait 60s')
    command = f'{rad_path} -uf {targets} -http-proxy 127.0.0.1:7777'
    logger.info(command)
    await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE,
                                          stderr=asyncio.subprocess.PIPE)


async def main(rad_path, targets, xray_path, result):
    await asyncio.gather(xray(xray_path, result), rad(rad_path, targets))


def xray_run(rad_path, targets, xray_path, result):
    asyncio.run(main(rad_path, targets, xray_path, result))


class XrayScan(object):
    def __init__(self, targets: list):
        self.targets = targets

        tmp_path = Config.TMP_PATH
        rand_str = utils.random_choices()

        self.xray_target_path = os.path.join(tmp_path,
                                             "xray_target_{}.txt".format(rand_str))

        self.xray_result_path = os.path.join(tmp_path,
                                             "xray_result_{}.json".format(rand_str))

        self.xray_bin_path = Config.XRAY_BIN

    def _delete_file(self):
        try:
            os.unlink(self.xray_target_path)
            if os.path.exists(self.xray_result_path):
                os.unlink(self.xray_result_path)
        except Exception as e:
            logger.warning(e)

    def _gen_target_file(self):
        with open(self.xray_target_path, "w") as f:
            for domain in self.targets:
                domain = domain.strip()
                if not domain:
                    continue
                f.write(domain + "\n")

    def dump_result(self) -> list:
        try:
            data = []
            if os.path.exists(self.xray_result_path):
                with open(self.xray_result_path, "r") as f:
                    data = f.read()
                    if data.endswith(']'):
                        data = data
                    else:
                        data = data + ']'
                data = json.loads(data)
            else:
                data = data
            return data
        except Exception as e:
            logger.warning(e)

    def exec_xray(self):
        self._gen_target_file()
        xray_run(Config.RAD_BIN, self.xray_target_path, self.xray_bin_path, self.xray_result_path)

    def run(self):
        self.exec_xray()
        results = self.dump_result()
        if results:
            results1 = results
        else:
            results1 = []
        self._delete_file()
        return results1


def xray_scans(targets: list):
    if not targets:
        return []

    n = XrayScan(targets=targets)
    return n.run()
