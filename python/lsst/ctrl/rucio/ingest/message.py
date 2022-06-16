from typing import Dict, Tuple

RSE_KEY = 'dstRse'
URL_KEY = 'dstUrl'

class Message:

    def __init__(self, message):
        self.message = message

    def extract_rse_info(self) -> Tuple[str, str]:
        m_list = self.message.headers
        headers = dict(m_list)
        dstRse = headers[RSE_KEY].decode()
        dstUrl = headers[URL_KEY].decode()
        return dstRse, dstUrl
        
