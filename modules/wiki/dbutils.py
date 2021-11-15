from typing import Union

import ujson as json
from tenacity import retry, stop_after_attempt

from core.elements import MessageSession
from database import session, auto_rollback_error
from .orm import WikiTargetSetInfo, WikiInfo, WikiAllowList


class WikiTargetInfo:
    @retry(stop=stop_after_attempt(3))
    @auto_rollback_error
    def __init__(self, msg: [MessageSession, str]):
        if isinstance(msg, MessageSession):
            targetId = msg.target.targetId
        else:
            targetId = msg
        self.query = session.query(WikiTargetSetInfo).filter_by(targetId=targetId).first()
        if self.query is None:
            session.add_all([WikiTargetSetInfo(targetId=targetId, iws='{}', headers='{}')])
            session.commit()
            self.query = session.query(WikiTargetSetInfo).filter_by(targetId=targetId).first()

    @retry(stop=stop_after_attempt(3))
    @auto_rollback_error
    def add_start_wiki(self, url):
        self.query.link = url
        session.commit()
        session.expire_all()
        return True

    def get_start_wiki(self) -> Union[str, None]:
        if self.query is not None:
            return self.query.link if self.query.link is not None else None

    @retry(stop=stop_after_attempt(3))
    @auto_rollback_error
    def config_interwikis(self, iw: str, iwlink: str = None, let_it=True):
        interwikis = json.loads(self.query.iws)
        if let_it:
            interwikis[iw] = iwlink
        else:
            if iw in interwikis:
                del interwikis[iw]
        self.query.iws = json.dumps(interwikis)
        session.commit()
        session.expire_all()
        return True

    def get_interwikis(self) -> dict:
        q = self.query.iws
        if q is not None:
            iws = json.loads(q)
            return iws
        else:
            return {}

    @retry(stop=stop_after_attempt(3))
    @auto_rollback_error
    def config_headers(self, headers, let_it: [bool, None] = True):
        headers = json.loads(headers)
        headers_ = json.loads(self.query.headers)
        if let_it:
            for x in headers:
                headers_[x] = headers[x]
        elif let_it is None:
            headers_ = {}
        else:
            for x in headers:
                if x in headers_:
                    del headers_[x]
        self.query.headers = json.dumps(headers_)
        session.commit()
        return True

    def get_headers(self):
        if self.query is not None:
            q = self.query.headers
            headers = json.loads(q)
        else:
            headers = {'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}
        return headers


class WikiSiteInfo:
    @retry(stop=stop_after_attempt(3))
    @auto_rollback_error
    def __init__(self, api_link):
        self.api_link = api_link
        self.query = session.query(WikiInfo).filter_by(apiLink=api_link).first()

    def get(self):
        if self.query is not None:
            return self.query.siteInfo, self.query.timestamp
        return False

    @retry(stop=stop_after_attempt(3))
    @auto_rollback_error
    def update(self, info: dict):
        if self.query is None:
            session.add_all([WikiInfo(apiLink=self.api_link, siteInfo=json.dumps(info))])
        else:
            self.query.siteInfo = json.dumps(info)
        session.commit()
        return True


class Audit:
    def __init__(self, api_link):
        self.api_link = api_link

    @property
    @retry(stop=stop_after_attempt(3))
    @auto_rollback_error
    def inAllowList(self) -> bool:
        session.expire_all()
        return True if session.query(WikiAllowList).filter_by(apiLink=self.api_link).first() else False

    @retry(stop=stop_after_attempt(3))
    @auto_rollback_error
    def add_to_AllowList(self, op) -> bool:
        if self.inAllowList:
            return False
        session.add_all([WikiAllowList(apiLink=self.api_link, operator=op)])
        session.commit()
        session.expire_all()
        return True

    @retry(stop=stop_after_attempt(3))
    @auto_rollback_error
    def remove_from_AllowList(self) -> bool:
        if not self.inAllowList:
            return False
        session.query(WikiAllowList).filter_by(apiLink=self.api_link).first().delete()
        session.expire_all()
        return True

    @staticmethod
    def get_audit_list() -> list:
        return session.query(WikiAllowList.apiLink, WikiAllowList.operator)
