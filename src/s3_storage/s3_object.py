

from flask import make_response, jsonify, request
from flask_restful import Resource
from src.s3_storage.s3_utils import *
from src.auth.auth import token_required
from werkzeug.utils import secure_filename
import boto3
import requests



class S3(Resource):

    @token_required
    def get(self):
        '''
        s3 sign işlemi yapan metod
        :return:
        '''
        try:
            S3_BUCKET = "beasy"
            data = request.get_json(force=True)
            file_name = data["file_name"]
            file_type = data["file_type"]

            s3 = boto3.client(
                "s3",
                aws_access_key_id="AKIA5CHGUKFPBI5XIJOX",
                aws_secret_access_key="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",
                region_name="eu-central-1"
            )

            presigned_post = s3.generate_presigned_post(
                Bucket=S3_BUCKET,
                Key=file_name,
                Fields={"acl": "public-read", "Content-Type": file_type},
                Conditions=[
                    {"acl": "public-read"},
                    {"Content-Type": file_type}
                ],
                ExpiresIn=3600
            )
            return make_response(jsonify(
                status="ok",
                msg="File signed successfully",
                data=presigned_post,
                url=f'https://{S3_BUCKET}.s3.amazonaws.com/{file_name}'
            ))
        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=f'Error while signing the file to S3: {str(ex.args[0])}'
            ), 500)



    @token_required
    def post(self):
        '''
        amazon s3'e dosya yüklemek için kullanılır
        :return:
        '''
        try:
            files = request.files
            file = files["file"]
            file.filename = generate_secure_name(file)
            S3_BUCKET = "beasy"
            s3 = boto3.client(
                "s3",
                aws_access_key_id="AKIA5CHGUKFPBI5XIJOX",
                aws_secret_access_key="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",
                region_name="eu-central-1"
            )

            presigned_post = s3.generate_presigned_post(
                Bucket=S3_BUCKET,
                Key=file.filename,
                Fields={"acl": "public-read", "Content-Type": file.mimetype},
                Conditions=[
                    {"acl": "public-read"},
                    {"Content-Type": file.mimetype}
                ],
                ExpiresIn=3600
            )

            resp = requests.post(presigned_post["url"], data=presigned_post["fields"], files=request.files)

            return make_response(jsonify(
                status="ok",
                message="File uploaded successfully",
                file_url=resp.headers["Location"]
            ))


            #a = s3.upload_fileobj(
            #    file,
            #    S3_BUCKET,
            #    file.filename,
            #    ExtraArgs={
            #        "ACL": "public-read",
            #        "ContentType": file.content_type  # Set appropriate content type as per the file
            #    }
            #)

        except Exception as ex:
            return make_response(jsonify(
                status="fail",
                msg=f'Error while uploading the file to S3: {str(ex.args[0])}'
            ), 500)


