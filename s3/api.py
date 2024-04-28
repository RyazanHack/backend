from fastapi import HTTPException
from starlette.datastructures import UploadFile
import aiohttp
from aiohttp import FormData
from config import MINIO_ADDRESS, S3_WORKER_API


class S3Worker:
    @staticmethod
    async def new_bucket(name: str, ignore_existing=False):
        async with aiohttp.ClientSession() as session:
            url = f"{S3_WORKER_API}/new_bucket"
            params = {"name": name}
            async with session.post(url, params=params) as resp:
                resp_json = await resp.json()
                if not resp.ok:
                    if resp.status == 400 and ignore_existing:
                        return
                    raise HTTPException(resp.status, resp_json)

    @staticmethod
    async def remove_bucket(name: str):
        async with aiohttp.ClientSession() as session:
            url = f"{S3_WORKER_API}/remove_bucket"
            params = {"name": name}
            async with session.delete(url, params=params) as resp:
                resp_json = await resp.json()
                if not resp.ok:
                    raise HTTPException(resp.status, resp_json)

    @staticmethod
    async def list_files(bucket: str):
        async with aiohttp.ClientSession() as session:
            url = f"{S3_WORKER_API}/files/{bucket}"
            async with session.get(url) as resp:
                resp_json = await resp.json()
                if not resp.ok:
                    raise HTTPException(resp.status, resp_json)
                return resp_json

    @staticmethod
    async def upload_file(
        bucket: str,
        file: UploadFile | bytes,
        filename: str | None = None,
        mimetype: str | None = None,
    ):
        async with aiohttp.ClientSession() as session:
            url = f"{S3_WORKER_API}/upload_file"

            params = {
                "bucket": bucket,
            }

            if filename is not None:
                params.update({"filename": filename})
            if mimetype is not None:
                params.update({"mimetype": mimetype})

            data = FormData()

            if isinstance(file, UploadFile):
                data.add_field(
                    "file",
                    file.file.read(),
                    filename=file.filename,
                    content_type=file.content_type,
                )
            else:
                data.add_field("file", file)

            async with session.post(url, params=params, data=data) as resp:
                resp_json = await resp.json()
                if not resp.ok:
                    raise HTTPException(resp.status, resp_json)
                return resp_json

    @staticmethod
    async def remove_file(bucket: str, filename: str):
        async with aiohttp.ClientSession() as session:
            url = f"{S3_WORKER_API}/remove_file"
            params = {"bucket": bucket, "filename": filename}
            async with session.delete(url, params=params) as resp:
                resp_json = await resp.json()
                if not resp.ok:
                    raise HTTPException(resp.status, resp_json)

    @staticmethod
    async def get_file_url(bucket: str, filename: str):
        async with aiohttp.ClientSession() as session:
            url = f"{S3_WORKER_API}/file/{bucket}/{filename}"
            async with session.get(url) as resp:
                resp_json = await resp.json()
                if not resp.ok:
                    raise HTTPException(resp.status, resp_json)
                return resp_json.replace(
                    "http://host.docker.internal:9000", MINIO_ADDRESS
                )
