import time
from functools import wraps
from contextlib import contextmanager
import boto3


@contextmanager
def s3bucket(name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(name)
    yield bucket, s3


def upload_file(project_id, filename, data, name='servicebook'):
    key = '%s-%s' % (project_id, filename)
    with s3bucket(name) as (bucket, s3):
        data.seek(0)
        bucket.upload_fileobj(data, key)
        acl = s3.ObjectAcl(name, key)
        acl.put(ACL='public-read')


_C = {}


def cached(name, max_age=60):
    def _cached(func):
        @wraps(func)
        def __cached(*args, **kw):
            if name in _C:
                when, val = _C[name]
                if time.time() - when < max_age:
                    return val
            val = func(*args, **kw)
            _C[name] = time.time(), val
            return val
        return __cached
    return _cached


# XXX cache -- need a "has bucket changed?"
@cached('list')
def get_list(project_id, name='servicebook'):
    keys = []
    filter = str(project_id) + '-'
    with s3bucket(name) as (bucket, s3):
        for ob in bucket.objects.filter(Prefix=filter):
            keys.append(ob.key)
    return keys
