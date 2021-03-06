import pika

class PikaMassenger():

    exchange_name = 'users_events'

    def __init__(self, *args, **kwargs):
        
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.channel = self.conn.channel()
        self.channel.exchange_declare(
            exchange=self.exchange_name, 
            exchange_type='topic')
        print('Successfully connected to AMPQ')
    
    def consume(self, keys, callback):
        print('started consuming')
        result = self.channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        for key in keys:
            self.channel.queue_bind(
                exchange=self.exchange_name, 
                queue=queue_name, 
                routing_key=key)
        
        self.channel.basic_consume(
            queue=queue_name, 
            on_message_callback=callback, 
            auto_ack=True)

        self.channel.start_consuming()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

