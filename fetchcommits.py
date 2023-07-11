from github import Github
from github import Auth
from jproperties import Properties
from datetime import datetime, timedelta
import traceback
import pandas as pd
import sendmail as sendmail

class GitFetch:

    def __init__(self):
        self.access_token = ""
        self.githost = ""
        self.gitrepo = ""

    def readinputs(self,usefile,configdict):
        if usefile:
            f = "inputs.properties"
            configs = Properties()
            with open(f, 'rb') as configf:
                configs.load(configf)

            configdictfile = {}
            for item in configs.items():
                configdictfile[item[0]] = item[1].data

            print(configdictfile)

            self.access_token = configdictfile["ACCESS_TOKEN"]
            self.githost = configdictfile["GITHUB_HOST"]+"api/v3"
            self.gitrepo = configdictfile["OWNER"]+"/"+configdictfile["REPO_NAME"]
            self.g = self.getgithubobj()
            self.repo = self.g.get_repo(self.gitrepo)
        else:
            self.access_token = configdict["ACCESS_TOKEN"]
            self.githost = configdict["GITHUB_HOST"]+"api/v3"
            self.gitrepo = configdict["OWNER"]+"/"+configdict["REPO_NAME"]
            self.g = self.getgithubobj()
            self.repo = self.g.get_repo(self.gitrepo)

    def getgithubobj(self):
        try:
            if self.access_token != '':
                auth = Auth.Token(self.access_token)
                g = Github(base_url=self.githost, auth=auth)
            else:
                g = Github()
            return g
        except:
            print("Cannot authenticate with the Github host. \n Please check your access token / host url")

    def fetchpullreqs(self,prstate,timeframe,indraft=False):
        try:
            allpulls = self.repo.get_pulls(state=prstate)
            pullsintf = [pull for pull in allpulls if pull.created_at >= timeframe]
            outputdict = {"Title": [],"PR Number":[]}
            for pr in pullsintf:
                if indraft:
                    if "WIP" in pr.title:
                        outputdict["Title"].append(pr.title)
                        outputdict["PR Number"].append(pr.number)
                else:
                    outputdict["Title"].append(pr.title)
                    outputdict["PR Number"].append(pr.number)

            outputdf = pd.DataFrame(outputdict)
            print(str(outputdf))
            sendmail.sendmailtoconsole(str(outputdf))
            return outputdf
        except:
            traceback.print_exc()
            print("Cannot get pull requests based on state "+prstate)


if __name__ == '__main__':

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    lastweek = today - timedelta(days=7)

    gf = GitFetch()
    gf.readinputs(True,None)
    gf.fetchpullreqs("open",lastweek)
    gf.fetchpullreqs("closed",lastweek)
    gf.fetchpullreqs("open",lastweek,indraft=True)
