from auth import create_app
from .massenger import PikaMassenger
import asyncio
import threading 
from .models import User

def start_consumer(app):
    def callback(ch, method, properties, body):
        try:
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
        consumer.consume(keys=['user.*',], callback=callback)



app = create_app()
consumer_thread = threading.Thread(target=start_consumer, kwargs={"app": app})
consumer_thread.start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000")
    

