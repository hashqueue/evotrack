import multiprocessing

wsgi_app = "evotrack.wsgi"
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = "logs/gunicorn-access.log"
errorlog = "logs/gunicorn-error.log"
