scripts_file_name = "scripts_repo.json"
SESSION_MEM_PER_WORKER = 200000

STATUS_CODE_MSG = {
    0: "OK",
    1: "ERROR_SESSION_NOT_EXIST",
    2: "SESSION_VERIFY_ERROR",
    3: "BODY_JSON_DECODE_ERROR",
    4: "DM ERROR"
}

STATUS_MSG_CODE = {
    "OK": 0,
    "ERROR_SESSION_NOT_EXIST": 1,
    "SESSION_VERIFY_ERROR": 2,
    "BODY_JSON_DECODE_ERROR": 3,
    "DM ERROR": 4
}

filter_jaccard_above=0.6

WORKER_NUM=2
WORKER_PORT_BEGIN=10811
SERVER_PORT=10810

SIMI_ABOVE=0.78