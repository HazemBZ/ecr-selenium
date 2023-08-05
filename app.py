import logging
import os
import sys
from datetime import datetime

import boto3
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

from selenium import webdriver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

error = ''
saved_file = "screen.png"
website = os.environ.get('WEBSITE', "https://example.com/")

try:

    chrome_options = ChromeOptions()

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--no-zygote")

    with Display(visible=False):
        logger.info(f"#=== DISPLAY: {os.environ['DISPLAY']}")
        logger.info('#=== Starting chrome Driver')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(website)
        # text = driver.find_element(by=By.XPATH, value="//html").text
        body = driver.find_element(by=By.TAG_NAME, value='body')
        body.screenshot(saved_file)
        logger.info('#=== Stopping emu display')

    # Upload to S3 
    s3 = boto3.resource(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )

    s3_file_name = f"{str(datetime.now().timestamp())}.png"
    s3.Bucket(os.environ['S3_BUCKET_NAME']).upload_file(
        saved_file,
        s3_file_name
    )


except Exception as e:
    error = e
    logger.info(e)
    sys.exit(1)

else:
    sys.exit(0)
