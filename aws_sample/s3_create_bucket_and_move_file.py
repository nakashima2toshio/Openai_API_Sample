# s3_create_bucket_and_move_file.py
import boto3
from botocore.exceptions import ClientError

def create_s3_resource(region):
    """S3リソースオブジェクトを作成する"""
    return boto3.resource('s3', region_name=region)

def create_bucket(s3_resource, bucket_name, region):
    """バケットを作成する"""
    try:
        if region == 'us-east-1':
            s3_resource.create_bucket(Bucket=bucket_name)
        else:
            s3_resource.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"バケット '{bucket_name}' が正常に作成されました。")
    except ClientError as e:
        print(f"バケット作成エラー: {e}")

def upload_file_to_bucket(s3_resource, bucket_name, file_name, object_name):
    """ファイルをバケットにアップロードする"""
    try:
        s3_resource.Bucket(bucket_name).upload_file(file_name, object_name)
        print(f"ファイル '{file_name}' をバケット '{bucket_name}' にアップロードしました。")
    except ClientError as e:
        print(f"ファイルアップロードエラー: {e}")

def main():
    # リージョンとバケット名の設定
    region_tokyo = 'ap-northeast-1'  # 東京リージョン
    bucket_name = 'sample-bucket-002'  # 一意のバケット名を指定

    region = region_tokyo

    # S3リソースオブジェクトの作成
    s3 = create_s3_resource(region)

    # バケットの作成
    create_bucket(s3, bucket_name, region)

    # ファイルのアップロード
    file_name = 'sample1.txt'  # ローカルのファイルパス
    object_name = 'sample1.txt'  # S3 でのオブジェクト名

    upload_file_to_bucket(s3, bucket_name, file_name, object_name)

if __name__ == '__main__':
    main()

