import datetime
import os
import re
import textwrap
from bs4 import BeautifulSoup
from urllib import request
from slack_sdk.web import WebClient


class Notifier:
    def __init__(self):
        self.weekdays = {
            0: "月(Mon)",
            1: "火(Tue)",
            2: "水(Wed)",
            3: "木(Thu)",
            4: "金(Fri)",
            5: "土(Sat)",
            6: "日(Sun)",
        }

        self.data = self.scrape_upcoming_contests()

    def __getitem__(self, idx):
        return self.data[idx]

    def scrape_upcoming_contests(self):
        data = []
        soup = BeautifulSoup(
            request.urlopen(
                url="https://atcoder.jp",
            ),
            "html.parser",
        )
        upcoming_table = soup.find("div", id="contest-table-upcoming")

        if upcoming_table is None:
            return data
        else:
            today = datetime.datetime.today()
            upcoming_contests = upcoming_table.find("tbody").find_all("tr")

            for contest in upcoming_contests:
                date = contest.find("time").text
                date = re.sub("\+.*", "", date)

                contest_date = self.str2datetime(formatted_date_string=date)
                if (contest_date - today).days >= 7:
                    break

                contest_date = self.datetime2str(datetime_object=contest_date)

                contest_url = "https://atcoder.jp"
                contest_url += contest.find(
                    name="a",
                    href=re.compile(
                        pattern="contests",
                    ),
                ).get("href")

                contest_name = contest.find_all(
                    name="td"
                )[-1].find("a").text

                data.append(
                    (
                        contest_name,
                        contest_url,
                        contest_date,
                    )
                )
            return data

    def str2datetime(self, formatted_date_string):
        """convert str (%Y-%m-%d %H:%M) object to datetime.datetime object

        Args:
            formatted_date_string (str)

        Returns:
            date (datetime.datetime)
        """
        return datetime.datetime.strptime(formatted_date_string, "%Y-%m-%d %H:%M:%S")

    def datetime2str(self, datetime_object):
        """convert str (%Y-%m-%d %H:%M) object to datetime.datetime object

        Args:
            datetime_object (datetime.datetime)

        Returns:
            formatted_date_string (str)
        """
        return "{0:04}-{1:02}-{2:02}({3}) {4:02}:{5:02}:{6:02}".format(
            datetime_object.year,
            datetime_object.month,
            datetime_object.day,
            self.weekdays[datetime_object.weekday()],
            datetime_object.hour,
            datetime_object.minute,
            datetime_object.second,
        )


class SlackBot:
    def __init__(self, token=""):
        self.token = token
        self.notifier = Notifier()
        self._init_client()

    def _init_client(self):
        self.client = WebClient(token=self.token)

    def alert_in_slack_channel(self):
        info = self.notifier.scrape_upcoming_contests()

        header = """
            <!channel>
            *今週のコンテスト*
        """
        content = ""

        for info_i in info:
            content += f"""
                > {info_i[0]}
                :page_facing_up: {info_i[1]}
                :date: {info_i[2]}
            """

        header = textwrap.dedent(header)
        content = textwrap.dedent(content)

        ret = self.client.chat_postMessage(
            text=header + content,
            channel='#notification',
            mrkdwn=True,
        )

        print(ret)


if __name__ == '__main__':
    bot = SlackBot(token=os.environ["ATCODER_NOTIFIER_TOKEN"])
    bot.alert_in_slack_channel()
