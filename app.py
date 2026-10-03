import os
from io import BytesIO

import boto3
from botocore.exceptions import ClientError
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)

app = Flask(__name__)

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "change-this-secret"
)

S3_BUCKET = os.environ.get("S3_BUCKET")
S3_PREFIX = os.environ.get(
    "S3_PREFIX",
    "documents/"
)

s3 = boto3.client("s3")

ALLOWED_EXTENSIONS = {
    "pdf",
    "doc",
    "docx",
    "txt",
    "csv",
    "xlsx",
    "xls",
    "png",
    "jpg",
    "jpeg",
    "zip"
}

MAX_FILE_SIZE = 10 * 1024 * 1024


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def create_s3_key(filename):

    filename = os.path.basename(filename)

    filename = filename.replace(
        " ",
        "_"
    )

    return (
        f"{S3_PREFIX.rstrip('/')}/"
        f"{filename}"
    )


@app.route("/")
def index():

    files = []

    try:

        response = s3.list_objects_v2(
            Bucket=S3_BUCKET,
            Prefix=S3_PREFIX
        )

        for item in response.get(
            "Contents",
            []
        ):

            key = item["Key"]

            if key.endswith("/"):
                continue

            files.append(
                {
                    "key": key,
                    "name": key.split("/")[-1],
                    "size": item["Size"],
                    "modified":
                        item["LastModified"]
                        .strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                }
            )

    except ClientError as e:

        flash(
            "S3 error: "
            + e.response["Error"]["Message"],
            "error"
        )

    return render_template(
        "index.html",
        files=files,
        bucket=S3_BUCKET
    )


@app.route(
    "/upload",
    methods=["POST"]
)
def upload():

    file = request.files.get("file")

    if not file:

        flash(
            "Please select a file.",
            "error"
        )

        return redirect(
            url_for("index")
        )

    if not file.filename:

        flash(
            "Invalid filename.",
            "error"
        )

        return redirect(
            url_for("index")
        )

    if not allowed_file(
        file.filename
    ):

        flash(
            "File type is not allowed.",
            "error"
        )

        return redirect(
            url_for("index")
        )

    data = file.read()

    if len(data) > MAX_FILE_SIZE:

        flash(
            "Maximum file size is 10 MB.",
            "error"
        )

        return redirect(
            url_for("index")
        )

    key = create_s3_key(
        file.filename
    )

    try:

        s3.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=data,
            ServerSideEncryption="AES256"
        )

        flash(
            "File uploaded successfully.",
            "success"
        )

    except ClientError as e:

        flash(
            "Upload failed: "
            + e.response["Error"]["Message"],
            "error"
        )

    return redirect(
        url_for("index")
    )


@app.route("/download")
def download():

    key = request.args.get(
        "key",
        ""
    )

    if not key.startswith(
        S3_PREFIX
    ):

        flash(
            "Invalid file path.",
            "error"
        )

        return redirect(
            url_for("index")
        )

    try:

        response = s3.get_object(
            Bucket=S3_BUCKET,
            Key=key
        )

        data = response["Body"].read()

        filename = os.path.basename(
            key
        )

        return send_file(
            BytesIO(data),
            as_attachment=True,
            download_name=filename
        )

    except ClientError as e:

        flash(
            "Download failed: "
            + e.response["Error"]["Message"],
            "error"
        )

        return redirect(
            url_for("index")
        )


@app.route(
    "/delete",
    methods=["POST"]
)
def delete():

    key = request.form.get(
        "key",
        ""
    )

    if not key.startswith(
        S3_PREFIX
    ):

        flash(
            "Invalid file path.",
            "error"
        )

        return redirect(
            url_for("index")
        )

    try:

        s3.delete_object(
            Bucket=S3_BUCKET,
            Key=key
        )

        flash(
            "File deleted successfully.",
            "success"
        )

    except ClientError as e:

        flash(
            "Delete failed: "
            + e.response["Error"]["Message"],
            "error"
        )

    return redirect(
        url_for("index")
    )


@app.route("/health")
def health():

    return {
        "status": "ok"
    }


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
