## [追加] 画像のオブジェクト検出

Vision APIを使って画像のオブジェクトを検出、加工した画像をCloud Storageに保存します。

## 環境を準備します

### もとの画像を配置するバケットを用意します
```bash
INPUT={{project-id}}-input
gsutil mb gs://$INPUT
```

### 加工後の画像を配置するバケットを用意します
```bash
OUTPUT={{project-id}}-output
gsutil mb gs://$OUTPUT
```

### イベントを処理するpubsubを用意します
トピック名を決めます。
```bash
TOPIC=object-detection-pubsub
```

pubsubのトピックを作成します。
```bash
gcloud pubsub topics create $TOPIC
```

## 権限設定を実施します

### pubsubが利用するサービスアカウントに以下の権限を付与します

プロジェクト番号を取得します。
```bash
PROJECT_NUMBER=$(gcloud projects describe {{project-id}} --format=json | jq .projectNumber -r)
echo $PROJECT_NUMBER
```

サービスアカウントのトークン作成権限を付与します。

```bash
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com --role=roles/iam.serviceAccountTokenCreator
```

### サービスアカウントを作成します
```bash
gcloud iam service-accounts create cloud-run-pubsub-invoker --display-name "Cloud Run Pub/Sub Invoker"
```


## コンテナイメージを作成します
### コンテナイメージの名前をセットします
```bash
export GCR_IMAGE=gcr.io/$GOOGLE_CLOUD_PROJECT/pubsub:v1
```

### コンテナイメージをビルド、プッシュします
```bash
cd ~/gcp-handson/cloud-run-basic/object-detection
gcloud builds submit -t $GCR_IMAGE
```

### Cloud Runをデプロイします
```bash
gcloud run deploy --platform=managed --allow-unauthenticated object-detection-runner --image gcr.io/$GOOGLE_CLOUD_PROJECT/pubsub:v1 --region asia-northeast1 --set-env-vars=CONVERT_BUCKET_NAME=$OUTPUT
```

### 呼び出し元のサービスアカウントにCloud Runを呼び出せるように権限を付与します
```bash
gcloud run services add-iam-policy-binding object-detection-runner --member=serviceAccount:cloud-run-pubsub-invoker@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com --role=roles/run.invoker --platform=managed --region asia-northeast1
```

## pubsubのトリガーとサブスクリプションの設定をします

### まず、Cloud RunのエンドポイントのURLを取得します
```bash
ENDPOINT=$(gcloud run services describe object-detection-runner --platform=managed --region=asia-northeast1 --format=json | jq -r .status.url)
```

### サブスクリプションを作成します
```bash
gcloud pubsub subscriptions create subsc1 --topic $TOPIC --push-endpoint=$ENDPOINT/ --push-auth-service-account=cloud-run-pubsub-invoker@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com
```

### トリガーの設定をします
```bash
gsutil notification create -t $TOPIC -f json gs://$INPUT
```

## 動作確認

### 画像をアップロードします
```bash
cd ~/gcp-handson
gsutil cp sample.jpg gs://$INPUT/
```

### 10秒くらい待って、バケットを出力先の確認します
```bash
gsutil ls gs://$OUTPUT
```


## Congraturations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

これにて Cloud Runの入門ハンズオンは全て完了です！！

次の手順でクリーンアップを行って下さい。
## クリーンアップ（プロジェクトを削除）

作成したリソースを個別に削除する場合は、こちらのページの手順を実施せずに次のページに進んで下さい。

### GCP のデフォルトプロジェクト設定の削除

```bash
gcloud config unset project
```
### プロジェクトの削除

```bash
gcloud projects delete {{project-id}}
```
プロジェクトの削除には適切な権限が必要です。
削除できない場合は、オーナー権限のアカウントをお持ちの方に依頼してください。