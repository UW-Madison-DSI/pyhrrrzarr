import s3fs

DEFAULT_FS: s3fs.S3FileSystem = s3fs.S3FileSystem(anon=True)
