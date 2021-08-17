---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: php-app-deployment
spec:
  selector:
    matchLabels:
      app: php-app
  replicas: 1
  template:
    metadata:
      labels:
        app: php-app
    spec:
      containers:
      - name: myapp
        image: gcr.io/$GOOGLE_CLOUD_PROJECT/php-app:v1
        readinessProbe:
          httpGet:
            port: 80
            path: /php/index.php?healthy=1
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: php-app
spec:
  type: NodePort
  selector:
    app: php-app
  ports:
  - protocol: TCP
    port: 80
