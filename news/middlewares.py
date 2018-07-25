
from news.settings import USER_AGENT_LIST
import random


class RandomUserAgent(object):

    def process_request(self, request, spider):
        # if spider.name == "xlzt":
        UA = random.choice(USER_AGENT_LIST)
        request.headers["User-Agent"] = UA

