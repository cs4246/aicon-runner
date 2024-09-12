from .celery import app
import argparse

parser = argparse.ArgumentParser(description='aiVLE Runner')
parser.add_argument('-c', '--concurrency', type=int, default=None)
args = parser.parse_args()

worker = app.Worker(concurrency=args.concurrency)
worker.start()
