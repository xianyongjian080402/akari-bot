from config import Config
from core.dirty_check import check
from modules.wiki.utils.UTC8 import UTC8
from modules.wiki.wikilib import WikiLib


async def ab_qq(wiki_url):
    wiki = WikiLib(wiki_url)
    qq_account = Config("qq_account")
    query = await wiki.get_json(action='query', list='abuselog', aflprop='user|title|action|result|filter|timestamp',
                                afllimit=99)
    pageurl = wiki.wiki_info.articlepath.replace("$1", 'Special:AbuseLog')
    nodelist = [{
        "type": "node",
        "data": {
            "name": f"滥用过滤器日志地址",
            "uin": qq_account,
            "content": [
                {"type": "text", "data": {"text": pageurl}}]
        }
    }]
    ablist = []
    userlist = []
    titlelist = []
    for x in query["query"]["abuselog"]:
        userlist.append(x['user'])
        titlelist.append(x['title'])
    checked_userlist = await check(*userlist)
    user_checked_map = {}
    for u in checked_userlist:
        user_checked_map[u['original']] = u['content']
    checked_titlelist = await check(*titlelist)
    title_checked_map = {}
    for t in checked_titlelist:
        title_checked_map[t['original']] = t['content']
    for x in query["query"]["abuselog"]:
        t = []
        t.append(f"用户：{user_checked_map[x['user']]}")
        t.append(f"页面标题：{title_checked_map[x['title']]}")
        t.append(f"过滤器名：{x['filter']}")
        t.append(f"操作：{x['action']}")
        result = x['result']
        if result == '':
            result = 'pass'
        t.append(f"处理结果：{result}")
        t.append(UTC8(x['timestamp'], 'full'))
        ablist.append('\n'.join(t))
    for x in ablist:
        nodelist.append(
            {
                "type": "node",
                "data": {
                    "name": f"滥用过滤器日志",
                    "uin": qq_account,
                    "content": [{"type": "text", "data": {"text": x}}],
                }
            })
    print(nodelist)
    return nodelist
