import os

bind = '127.0.0.1:' + str(os.getenv('PORT', 5000))
proc_name = 'Infrastructure-Practice-Flask'
workers = 1