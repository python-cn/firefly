# coding=utf-8

# Available error code
OK = 0
ERROR = 1
EPERM = 2
EACCESS = 3
ENOEXIST = 4
NOTFOUND = 5
EXISTING = 6
UNKNOWN = 127

# status maps
STATUS_MAPS = {
    OK: 'ok',
    NOTFOUND: 'not found',
    EXISTING: 'already exists',
    UNKNOWN: 'unknown'
}
