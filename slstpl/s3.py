import boto3
import os
import time
import json
import time
from slstpl.util.logger import logger
from botocore.exceptions import ClientError


class StorageError(Exception):
    """An unexpected error occurred while accessing storage."""
    pass


class StorageItemNotFound(StorageError):
    """The requested item was not found in the storage."""
    pass


class StorageItemChangedOnServer(StorageError):
    """The requested item could not be stored because the value on the server has changed."""
    pass


class S3Storage(object):
    """A storage class that provides access to documents stored in S3.

    Data can be loaded from or saved to S3 by reading from or writing to
    dict keys on an S3Storage instance.

    > s3 = S3Storage()
    > s3['key'] = 'value'
    > val = s3['key']
    > del s3['key']

    Structured data can be written to the json attribute of an S3Storage
    instance in order to write the json-encoded representation of the data
    to the underlying storage.

    > s3 = S3Storage()
    > s3.json('key') = [1, 2, 3]

    Reading from the json attribute of an S3Storage instance  will json-decode
    the data that was read before returning it.

    > s3 = S3Storage()
    > list = s3.json('key')

    The following environmental variables are used to control the behaviour of the
    S3Storage class:
      S3_BUCKET -- The bucket all S3Storage instances will be associated with (defaults to test).
    """
    S3_BUCKET = os.environ.get('S3_BUCKET', 'test')
    s3 = boto3.client('s3')

    def __init__(self):
        """Create a new S3Storage instance."""
        self.json = _JsonStorage(self)

    def __getitem__(self, key):
        """Load a string from the given S3 key.

        Raises a StorageItemNotFound exception if the key was not found.
        """
        logger.info("read s3 %s %s" % (self.S3_BUCKET, key))
        get_start = time.time()
        try:
            obj = self.s3.get_object(Bucket=self.S3_BUCKET, Key=key)
            result = obj['Body'].read().decode('utf-8')
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise StorageItemNotFound('No such key exists')
            raise e
        get_end = time.time()
        logger.info("FUNC %s %s", "S3Storage.get", get_end - get_start)
        return result

    def __setitem__(self, key, value):
        """Save a string to the specified S3 key."""
        logger.info("S3 put item %s %s %s" % (self.S3_BUCKET, key, value))
        self.s3.put_object(Bucket=self.S3_BUCKET, Key=key, Body=value)
        logger.info("S3 put item SUCCESS")

    def __delitem__(self, key):
        """Delete the object at the specified S3 key."""
        return self.s3.delete_object(Bucket=self.S3_BUCKET, Key=key)

    def download_file(self, key, filepath):
        """Download the contents of a given S3 key into a file."""
        logger.info("download s3 %s %s %s" % (self.S3_BUCKET, key, filepath))
        get_start = time.time()
        self.s3.download_file(self.S3_BUCKET, key, filepath)
        get_end = time.time()
        logger.info("FUNC %s %s", "S3Storage.download", get_end - get_start)

    def upload_file(self, filepath, key):
        """Upload the contents of a file to the given S3 key."""
        logger.info("upload s3 %s %s %s" % (self.S3_BUCKET, key, filepath))
        get_start = time.time()
        self.s3.upload_file(filepath, self.S3_BUCKET, key)
        get_end = time.time()
        logger.info("FUNC %s %s", "S3Storage.upload", get_end - get_start)

    def clear_all(self):
        """Clear all documents currently stored in the S3 bucket."""
        for key in self.clear_all_keys():
            pass

    def clear_all_keys(self):
        """Clear all documents currently stored in the S3 bucket."""
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(self.S3_BUCKET)
        for s3obj in bucket.objects.all():
            yield s3obj.key
            s3obj.delete()


class _JsonStorage(object):
    """Provides structured access to json-encoded data in the underlying storage."""

    def __init__(self, store):
        self.store = store

    def __getitem__(self, key):
        """Decode the JSON string at the given key and return the resulting data."""
        data = self.store[key]
        return json.loads(data)

    def raw_get(self, key):
        """Decode the JSON string at the given key and return the resulting data using the underlying raw_get method.

        If the underlying storage does not have a raw_get method, raises an AttributeError exception just like if the
        non-existant raw_get method had been called directly.
        """
        data = self.store.raw_get(key)
        return json.loads(data)

    def __setitem__(self, key, value):
        """Encode the provided data as JSON, and save it to the given key."""
        data = json.dumps(value)
        self.store[key] = data
