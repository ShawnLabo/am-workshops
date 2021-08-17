# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: container-handson-deployment
spec:
  selector:
    matchLabels:
      app: container-handson
  replicas: 1
  template:
    metadata:
      labels:
        app: container-handson
    spec:
      containers:
      - name: myapp
        image: gcr.io/$GOOGLE_CLOUD_PROJECT/container-handson:v1
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: container-handson
spec:
  type: NodePort
  selector:
    app: container-handson
  ports:
  - protocol: TCP
    port: 8080
    targetPort: 8080
