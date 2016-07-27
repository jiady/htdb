PENDING_QUEUE = "crawler/pending/queue/"
PENDING_SET = "crawler/pending/set/"
TYPE_HAS_ACCOUNT = "withAccount"
TYPE_NO_ACCOUNT = "noAccount"

PENDING_QUEUE_NO_ACCOUNT = PENDING_QUEUE + TYPE_NO_ACCOUNT
PENDING_SET_NO_ACCOUNT = PENDING_SET + TYPE_NO_ACCOUNT
PENDING_QUEUE_HAS_ACCOUNT = PENDING_QUEUE + TYPE_HAS_ACCOUNT
PENDING_SET_HAS_ACCOUNT = PENDING_SET + TYPE_HAS_ACCOUNT
SET_SEEN = "crawler/requests-seen/"
SET_SUCCESS = "crawler/requests-success/"

SET_SEEN_NO_ACCOUNT = SET_SEEN + TYPE_NO_ACCOUNT
SET_SEEN_HAS_ACCOUNT = SET_SEEN + TYPE_HAS_ACCOUNT
SET_SUCCESS_NO_ACCOUNT = SET_SUCCESS + TYPE_NO_ACCOUNT
SET_SUCCESS_HAS_ACCOUNT = SET_SUCCESS + TYPE_HAS_ACCOUNT


def getOppsite(s):
    if s == TYPE_HAS_ACCOUNT:
        return TYPE_NO_ACCOUNT
    if s == TYPE_NO_ACCOUNT:
        return TYPE_HAS_ACCOUNT
    return s