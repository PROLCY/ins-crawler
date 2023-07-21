import os, sys

from dotenv import load_dotenv

from crawler import crawler

load_dotenv()
ACCOUNT_USERNAME = os.environ.get('ACCOUNT_USERNAME')
ACCOUNT_PASSWORD = os.environ.get('ACCOUNT_PASSWORD')  

configuration = {
    'USERNAME': ACCOUNT_USERNAME,
    'PASSWORD': ACCOUNT_PASSWORD,
    'HASHTAG': 'solotravel',
    'AMOUNT': 60,
    'ITERATION_CNT': 5,
    'TIME_DELAY_FROM': 30,
    'TIME_DELAY_TO': 180 
}

def main(argv):
    option = argv[1]

    if option == '-i':
        crawler(configuration)

if __name__ == '__main__':
    main(sys.argv)