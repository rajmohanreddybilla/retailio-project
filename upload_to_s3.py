import boto3
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS config
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = os.getenv("AWS_DEFAULT_REGION")
bucket_name = os.getenv("BUCKET_NAME")

# Create S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region
)

# Local CSV → S3 Parquet mapping (NO DATE FOLDER)
files = {
    "data/sales.csv": "raw/sales/sales.parquet",
    "data/customers.csv": "raw/customers/customers.parquet",
    "data/products.csv": "raw/products/products.parquet"
}

for local_csv, s3_path in files.items():
    try:
        # Read CSV
        df = pd.read_csv(local_csv)

        # Convert to parquet
        parquet_file = local_csv.replace(".csv", ".parquet")
        df.to_parquet(parquet_file, index=False)

        # Upload to S3 (will overwrite existing file)
        s3.upload_file(parquet_file, bucket_name, s3_path)

        print(f"✅ Uploaded {parquet_file} → s3://{bucket_name}/{s3_path}")

        # Delete temp file
        os.remove(parquet_file)

    except Exception as e:
        print(f"❌ Error processing {local_csv}: {e}")

print("Finished uploading Parquet files.")