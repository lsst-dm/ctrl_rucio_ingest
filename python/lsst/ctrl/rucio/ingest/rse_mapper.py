from typing import Dict
import yaml

class RseMapper:

    def __init__(self, filename):
        with open(filename) as file:
            rse_list = yaml.load(file, Loader=yaml.FullLoader)

            if 'rses' not in rse_list:
                raise Exception("Can't find 'rses'")
            self._rse_dict = rse_list['rses']
            if 'broker' not in rse_list:
                raise Exception("Can't find 'broker'")
            self._brokers = rse_list['broker']

    def resplice(self, rse: str, url: str) -> str:
        mapping_dict = self._rse_dict[rse]
        rucio_prefix = mapping_dict['rucio_prefix']
        fs_prefix = mapping_dict['fs_prefix']
        print('resplice: %s %s <> %s %s' % (rse, url, rucio_prefix, fs_prefix))
        ret = url.replace(rucio_prefix, fs_prefix)
        return ret

    def topics(self) -> list:
        return list(self._rse_dict.keys())

    def brokers(self) -> str:
        return self._brokers
