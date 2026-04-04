import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, to_timestamp, explode
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

args = getResolvedOptions(sys.argv, ["JOB_NAME", "SOURCE_BUCKET", "TARGET_BUCKET"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

SOURCE_BUCKET = args["SOURCE_BUCKET"]
TARGET_BUCKET = args["TARGET_BUCKET"]

print(f"Reading JSON from s3://{SOURCE_BUCKET}/raw/")

df_raw = spark.read.option("multiline", "true").json(f"s3://{SOURCE_BUCKET}/raw/")

df = df_raw.select(explode(col("value")).alias("record")).select(
    col("record.line_id"),
    col("record.line_name"),
    col("record.status"),
    col("record.severity"),
    col("record.recorded_at")
)

df = df.withColumn("recorded_at", to_timestamp(col("recorded_at")))

output_path = f"s3://{TARGET_BUCKET}/processed/"

df.write.mode("append").partitionBy("line_id").parquet(output_path)

print(f"Written {df.count()} records to {output_path}")

job.commit()
