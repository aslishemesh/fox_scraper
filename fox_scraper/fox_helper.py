import pika
import json


class FoxItem(object):
    """
    The FoxItem class
    """
    def __init__(self, item_img_id, item_main_category, item_type, item_name, item_price):
        self.item_img_id = item_img_id
        self.item_main_category = item_main_category
        self.item_type = item_type
        self.item_name = item_name
        self.item_price = item_price

    def to_json(self):
        """
        convert the FoxItem into json supported type
        :return: a dictionary to support json dumps
        """
        return {'item_main_category': self.item_main_category,
                'item_type': self.item_type,
                'item_img_id': self.item_img_id,
                'item_price': self.item_price,
                'item_name': self.item_name
                }

    def __eq__(self, other):
        """Override the default Equals behavior to support assert-equal"""
        if isinstance(other, self.__class__):
            return (self.item_img_id == other.item_img_id
                    and self.item_price == other.item_price
                    and self.item_name == other.item_name
                    and self.item_main_category == other.item_main_category
                    and self.item_type == other.item_type)
            # return self.__dict__ == other.__dict__
        return TypeError


class FoxSender(object):
    """
    The FoxSender class will be used for creating and send messages to fox exchange server.
    """

    def __enter__(self):
        """
        creation of FoxSender (using the 'with' statement)
        note - the reasons we used'fanout' exchange server:
         1. There is no need to separate the messages (all traffic belong to one server)
         2. We do not want to have any obligations from the consumer side (any number of consumers)
         3. Basically we have an dedicated exchange server and we like it to broadcast all messages to all queues.
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='fox_scrap', type='fanout')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


    def close_connection(self):
        self.connection.close()

    def send_message(self, message):
        body = json.dumps(message.to_json())
        self.channel.basic_publish(exchange='fox_scrap', routing_key='', body=body,
                                   properties=pika.BasicProperties(delivery_mode=2))
