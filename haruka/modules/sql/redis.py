#    Haruka Aya (A telegram bot project)
#    Copyright (C) 2017-2019 Paul Larsen
#    Copyright (C) 2019-2020 Akito Mizukito (Haruka Network Development)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pickle

from telegram import Update, Bot
from haruka import REDIS
from haruka.modules.sql.locales_sql import switch_to_locale, prev_locale


# AFK
def is_user_afk(userid):
    rget = REDIS.get(f'is_afk_{userid}')
    if rget:
        return True
    else:
        return False


def start_afk(userid, reason):
    REDIS.set(f'is_afk_{userid}', reason)


def afk_reason(userid):
    return strb(REDIS.get(f'is_afk_{userid}'))


def end_afk(userid):
    REDIS.delete(f'is_afk_{userid}')
    return True


# Languages
# These code doesn't make much sense, trust me, It will in the future.
def get_lang_chat(chatid):
    rget = REDIS.get(f'chatlang_{chatid}')

    if rget:
        locale = strb(REDIS.get(f'chatlang_{chatid}'))
        return locale
    else:
        try:
            curr_lang = prev_locale(chatid)
            locale = curr_lang.locale_name
            chat_lang_set(f'chatlang_{chatid}', locale)
            return locale
        except Exception:  # Every chat must have LANGUAGES!!!!
            locale = "en-US"
            # Both SQL and Redis
            switch_to_locale(chatid, locale)
            chat_lang_set(f'chatlang_{chatid}', locale)
            return locale


def chat_lang_set(chatid, locale):
    REDIS.set(f'chat_admin_{chatid}', locale)


# Admin
def get_chat_admin(chatid):
    try:
        rget = pickle.loads(REDIS.get(f'chat_admin_{chatid}'))
    except Exception:
        return "false"

    if rget:
        chat_admin = pickle.loads(REDIS.get(f'chat_admin_{chatid}'))
        return chat_admin
    else:
        return "false"


def update_chat_admin(chatid, adminlist):
    REDIS.set(f'chat_admin_{chatid}', adminlist)
    REDIS.expire(f'chat_admin_{chatid}', 1800)


# Helpers
def strb(redis_string):
    return str(redis_string)[2:-1]
