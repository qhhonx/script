#!/usr/bin/python
# encoding: utf-8
import sys

from workflow import Workflow
from workflow import web
from workflow.notify import notify

TOKEN = 'YY02tKajmTDz86wZO34mkNEIsK4lBL'
DELIMITER = ' '
BASE_URL = 'https://api.shanbay.com/bdc/'
QUERY_URL = BASE_URL + 'search/?word='
ADD_URL = BASE_URL + 'learning/'
NOTE_URL = BASE_URL + 'note/'


def main(wf):
    """
    TODO:
    apply for token
    definition exceed one line
    avoid command mode called directly
    """

    # The Workflow instance will be passed to the function
    # you call from `Workflow.run`. Not so useful, as
    # the `wf` object created in `if __name__ ...` below is global.
    #
    # Your imports go here if you want to catch import errors (not a bad idea)

    # Get args from Workflow, already in normalized Unicode
    if len(wf.args):
        logger.info("called " + DELIMITER.join(wf.args) + " length " + str(len(wf.args)))
        q = wf.args[0]
    else:
        q = "test "

    # Do stuff here ...
    mode_q = True
    try:
        args = q.strip().split(DELIMITER)
        if len(args) == 1:
            # query mode
            if not q.endswith(' '):
                wf.add_item(u"Ending with space to query...")
            else:
                query(args[0])
        else:
            # command mode
            mode_q = False
            cmd = args[0]
            if cmd.lower() == "add" and len(args) == 2:
                add(args[1])
            elif cmd.lower() == "notify" and len(args) == 2:
                notify(cmd, args[1])
            elif cmd.lower() == "note" and len(args) >= 3:
                note(args[1], args[2:])
            else:
                logger.warn("illegal command: " + str(cmd))
    except RuntimeError as e:
        if mode_q:
            wf.add_item(u"ERROR", str(e.message))
        else:
            notify("ERROR", str(e.message))

    # Add an item to Alfred feedback

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but Alfred won't be listening
    # any more...
    wf.send_feedback()


def query(word):
    data = get_word_json(word)
    en_definitions = data['data']['en_definitions']
    cn_definition = data['data']['definition']
    if cn_definition:
        wf.add_item(title=cn_definition, arg=unicode(data['data']['id']), valid=True,
                    modifier_subtitles={'cmd': 'add to wordbook', 'shift': 'test notify', 'alt': 'add note'})
    for en_type in en_definitions:
        for en_definition in en_definitions[en_type]:
            wf.add_item(" " + en_type + ". " + en_definition)


def add(word_id):
    data = {'access_token': TOKEN, 'id': word_id}
    r = web.post(ADD_URL, data=data)
    check_status(r)
    notify("Added to wordbook", word_id)


def note(word, notes):
    data = {'access_token': TOKEN, 'vocabulary': get_word_id(word), 'note': DELIMITER.join(notes).strip()}
    r = web.post(NOTE_URL, data=data)
    check_status(r)
    notify("Note added", word)


def get_word_json(word):
    r = web.get(QUERY_URL + word)
    check_status(r)
    return r.json()


def get_word_id(word):
    return get_word_json(word)['data']['id']


def check_status(msg):
    """
    status code
    0        success
    1        failed
    400      bad request        （请求数据有问题）
    401      forbidden          （权限不够）
    404      not found          （请求资源不存在）
    409      duplicated         （重复创建资源）
    HTTP status
    200       ok                （请求成功返回）
    401       unauthorized      （用户未登录，或者token过期）
    429       too many requests （请求次数过多）
    """
    status_error_map = {1: "failed", 400: "bad request", 401: "forbidden", 404: "not found", 409: "duplicated"}
    http_error_map = {401: "unauthorized", 429: "too many requests"}
    err_msg = "common error"

    if msg.status_code != 200:
        if msg.status_code in http_error_map:
            err_msg = http_error_map[msg.status_code]
        raise RuntimeError(err_msg + " : " + str(msg.status_code))

    api_status_code = msg.json()['status_code']
    if api_status_code != 0:
        if api_status_code in status_error_map:
            err_msg = status_error_map[api_status_code]
        raise RuntimeError(err_msg + " : code " + str(api_status_code))


if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow()
    logger = wf.logger
    # Call your entry function via `Workflow.run()` to enable its helper
    # functions, like exception catching, ARGV normalization, magic
    # arguments etc.
    sys.exit(wf.run(main))
