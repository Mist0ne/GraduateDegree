from redis import Redis
from celery import Celery
from myquicksand.myquicksand import quicksand


celeryApp = Celery("celeryApp", broker="redis://redis:6379", backend='redis://redis:6379')
redis = Redis(host='redis', port=6379)
allowed_extensions = ['pdf']


@celeryApp.task(bind=True)
def check_files(self, filename, file_content):
    qs = quicksand(data=bytes(file_content, encoding='utf-8'), filename=filename, strings=False)
    qs.process()
    results = qs.results
    if results['type'] not in allowed_extensions:
        allowed = False
        redis.json().set(name=self.request.id, path='$', obj={'uuid': self.request.id, 'name': filename, 'allowed': allowed, 'results': 'unknown file extension'})
    else:
        if results['warning'] == 0 and results['exploit'] == 0 and results['execute'] == 0:
            allowed = True
        else:
            allowed = False
        redis.json().set(name=self.request.id, path='$', obj={'uuid': self.request.id, 'name': filename, 'allowed': allowed, 'results': str(results)})
    return allowed


if __name__ == '__main__':
    celeryApp.start()