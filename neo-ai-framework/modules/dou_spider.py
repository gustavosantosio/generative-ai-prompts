from datetime import datetime
import scrapy
import json, requests
import boto3, time

class DouSpider(scrapy.Spider):
    name = 'dou_spider'
    start_urls = ['https://www.in.gov.br/leiturajournal?secao=dou3&data=26-02-2025']

    def parse(self, response):
        script_data = response.xpath("//script[@id='params']/text()").get()
        json_data = json.loads(script_data)
        for item in json_data['jsonArray']:
            yield {
                'titulo': item['title'],
                'url': f"https://www.in.gov.br/en/web/dou/-/{item['urlTitle']}",
                'conteudo': item['content']
            }


response = requests.get("https://queridodiario.ok.org.br/api/gazettes?query=licitação&published_since=2025-02-20")
print(response.json())
response.close()

bucket_name = 'neo-ai-framework'
object_key = 'state'

def save_to_s3(data, bucket_name, object_key, region_name='us-east-2'):

    try:
        # Create S3 client
        s3_client = boto3.client('s3', region_name=region_name)

        # Convert data to JSON string
        json_data = json.dumps(data, ensure_ascii=False, indent=4)

        # Upload to S3
        s3_client.put_object(
            Body=json_data,
            Bucket=bucket_name,
            Key=object_key,
            ContentType='application/json'
            )

        print(f"Successfully uploaded data to {bucket_name}/{object_key}")
        return True
    except Exception as e:
        print(f"Error saving to S3: {str(e)}")
        return False


# Example usage in your spider
# Assuming you have a list of items from your spider
items = []  # This would be your scraped items


# For the DouSpider example:
def process_results(items, bucket_name=bucket_name):
    # Save to S3
    bucket_name = bucket_name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_to_s3(
        data=items,
        bucket_name=bucket_name,
        object_key=f'dou_data/{timestamp}_dou_results.json'
        )

