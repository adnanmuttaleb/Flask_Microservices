import pika


class PikaMassenger():

    exchange_name = 'users_events'

    def __init__(self, *args, **kwargs):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.channel = self.conn.channel()
        self.channel.exchange_declare(
            exchange=self.exchange_name, 
            exchange_type='topic')
    
    def send(self, massege, keys):
        self.channel.basic_publish(
            exchange=self.exchange_name, 
            routing_key=keys, 
            body=massege)
        print("Message {} has been sent".format(massege))

    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
