# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import tempfile

from google.cloud import storage, vision
from googleapiclient.discovery import build
from wand.image import Image
from PIL import Image, ImageDraw

storage_client = storage.Client()
vision_service = build("vision", "v1p3beta1", cache_discovery=False)


def run(event, context):
    object_images(event)

def object_images(data):
    file_data = data

    file_name = file_data["name"]
    bucket_name = file_data["bucket"]

    blob = storage_client.bucket(bucket_name).get_blob(file_name)
    blob_uri = f"gs://{bucket_name}/{file_name}"
    blob_source = {"source": {"image_uri": blob_uri}}

    print(f"Analyzing {file_name}.")

    _, temp_local_filename = tempfile.mkstemp()
    blob.download_to_filename(temp_local_filename)

    print(f"Image {file_name} was downloaded to {temp_local_filename}.")

    from base64 import b64encode

    with open(temp_local_filename, "rb") as image_file:
        my_image = {"content": b64encode(image_file.read()).decode("utf-8")}
    my_features = [{"type": "OBJECT_LOCALIZATION", "model": "builtin/stable"}]
    my_body = {"requests": [{"image": my_image, "features": my_features}]}
    response = vision_service.images().annotate(body=my_body).execute()
    print(response)

    print(f"The image {file_name} was detected as inappropriate.")
    return __highlight_objects(
        temp_local_filename,
        file_name,
        response["responses"][0]["localizedObjectAnnotations"],
    )


def __highlight_objects(temp_local_filename, file_name, objects):
    image = Image.open(temp_local_filename)
    draw = ImageDraw.Draw(image, "RGBA")

    width = image.getbbox()[-2]
    height = image.getbbox()[-1]

    print("Before a for object loop")
    for object in objects:
        n_vertex_lt = tuple(object["boundingPoly"]["normalizedVertices"][0].values())
        n_vertex_rb = tuple(object["boundingPoly"]["normalizedVertices"][2].values())

        vertex_lt = (int(n_vertex_lt[0] * width), int(n_vertex_lt[1] * height))
        vertex_rb = (int(n_vertex_rb[0] * width), int(n_vertex_rb[1] * height))

        # bounding box
        draw.rectangle(xy=(vertex_lt, vertex_rb), outline="red")

        # probability
        object["name"]
        draw.text(
            xy=(vertex_lt[0], vertex_lt[1] - 10),
            text=object["name"] + ":" + str(format(object["score"], ".3f")),
            fill="red",
        )
    new_file_name = temp_local_filename + "-new.jpg"
    image.save(new_file_name)

    convert_bucket_name = os.getenv("OUTPUT_BUCKET")
    convert_bucket = storage_client.bucket(convert_bucket_name)
    new_blob = convert_bucket.blob(file_name)
    print(f"set new_blob {new_file_name} >> {file_name}")
    new_blob.upload_from_filename(new_file_name)
    os.remove(temp_local_filename)
    os.remove(new_file_name)
