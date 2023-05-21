import time

from redis import Redis
from celery import Celery
from myquicksand.myquicksand import quicksand


celeryApp = Celery("celeryApp", broker="redis://redis:6379", backend='redis://redis:6379')
redis = Redis(host='redis', port=6379)
allowed_extensions = ['pdf']


@celeryApp.task(bind=True)
def check_files(self, filename, file_content):
    time.sleep(200)
    qs = quicksand(data=bytes(file_content, encoding='utf-8'), filename=filename, strings=False)
    qs.process()
    results = qs.results
    if results['type'] not in allowed_extensions:
        redis.set(f'{self.request.id}_results', 'unknown file extension')
        return False
    redis.set(f'{self.request.id}_results', str(results))
    if results['warning'] == 0 and results['exploit'] == 0 and results['execute'] == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    celeryApp.start()