import logging

host = '192.168.1.111'
port = 3306
user = 'root'
password = 'Mojie2718'
db = 'mojie_zz'

# host = 'localhost'
# port = 3306
# user = 'root'
# password = 'root'
# db = 'mojie_zz'

logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)
