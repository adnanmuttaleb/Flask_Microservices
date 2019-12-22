from auth import create_app
from .massenger import PikaMassenger
from multiprocessing import Pool
from .models import User


def start_consumer(app):
  
    def callback(ch, method, properties, body):
        try:
            print("Event recieved %r" % body)
            with app.app_context():

                if method.routing_key == 'user.created':
                    User.save_from_json(body)
                elif method.routing_key == 'user.updated':
                    User.update_from_json(body)
                elif method.routing_key == 'user.deleted':
                    User.delete_from_json(body)
                print(" [x] %r:%r consumed" % (method.routing_key, body))
                
        except Exception as e:
            print("Consuming event %s failed: %s" % (method.routing_key, str(e)))

    with PikaMassenger() as consumer:
        consumer.consume(keys=['user.*', ], callback=callback)


app = create_app()

pool = Pool(processes=1)
result = pool.apply_async(start_consumer, [app])

# consumer_thread = threading.Thread(target=start_consumer, kwargs={"app": app})
# consumer_thread.start()