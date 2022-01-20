import os
import traceback

from config import Config
from core.elements import Plain
from core.logger import Logger
from core.utils.bot import get_url

assets_path = os.path.abspath('./assets/arcaea')
apiurl = Config('arcapi_official_url')
headers = {'Authorization': Config('arcapi_official_token')}
headers_botarcapi = {"User-Agent": Config('botarcapi_agent')}
botarcapi_url = Config('botarcapi_url')


async def get_songinfo(songid):
    try:
        get_songinfo_from_botarcapi = await get_url(f'{botarcapi_url}song/info?songid={songid}',
                                                    headers=headers_botarcapi, status_code=200, fmt='json')
        return get_songinfo_from_botarcapi['content']
    except Exception:
        traceback.print_exc()
        return False


async def get_info_official(usercode):
    try:
        getuserinfo_json = await get_url(f'{apiurl}user/{usercode}', headers=headers, status_code=200, fmt='json')
    except ValueError as e:
        Logger.info(f'[{usercode}] {e}')
        return {'success': False, 'msg': '查询失败。'}
    except Exception:
        traceback.print_exc()
        return {'success': False, 'msg': '查询失败。'}
    getuserinfo = getuserinfo_json['data']
    username = getuserinfo['display_name']
    potential = getuserinfo['potential'] / 100
    recent = getuserinfo["last_played_song"]
    if recent is None:
        return [Plain('此用户无游玩记录。')]
    difficulty = '???'
    if recent['difficulty'] == 0:
        difficulty = 'PST'
    elif recent['difficulty'] == 1:
        difficulty = 'PRS'
    elif recent['difficulty'] == 2:
        difficulty = 'FTR'
    elif recent['difficulty'] == 3:
        difficulty = 'BYD'
    score = recent['score']
    ptt = realptt = '???'
    trackname = recent['song_id']
    songinfo = await get_songinfo(recent['song_id'])
    if songinfo:
        trackname = songinfo['title_localized']['en']
        realptt = songinfo['difficulties'][recent['difficulty']]['realrating'] / 10
        ptt = realptt
        if score >= 10000000:
            ptt += 2
        elif score >= 9800000:
            ptt += 1 + (score - 9800000) / 200000
        elif score <= 9500000:
            ptt += (score - 9500000) / 300000
        if ptt <= 0:
            realptt = "???(can't calc since score is too low)"

    shiny_pure = recent['shiny_pure_count']
    pure = recent['pure_count']
    far = recent['far_count']
    lost = recent['lost_count']
    result = {'success': True, 'msg': f'{username} (Ptt: {potential})的最近游玩记录：\n'
                                      f'{trackname} ({difficulty})\n'
                                      f'Score: {score}\n'
                                      f'Pure: {pure} ({shiny_pure})\n'
                                      f'Far: {far}\n'
                                      f'Lost: {lost}\n'
                                      f'Potential: {realptt} -> {ptt}'}
    return result