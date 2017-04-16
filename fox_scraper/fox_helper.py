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
        return self.__dict__

    def print_item(self):
        """
        temp for testing - will be decrypt
        """
        print "item image id:", self.item_img_id
        print "item main category:", self.item_main_category
        print "item type:", self.item_type
        print "item name:", self.item_name
        print "item price: %.2f " %self.item_price

    def __eq__(self, other):
        """Override the default Equals behavior to support assert-equal"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test (also - supporting assert-functions"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented


class FoxSender(object):
    """
    The FoxSender class will be used for creating and send messages to fox exchange server.
    """
    def __init__(self):
        """
        creation of FoxSender
        note - the reasons we used'fanout' exchange server:
         1. There is no need to separate the messages (all traffic belong to one server)
         2. We do not want to have any obligations from the consumer side (any number of consumers)
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='fox_scrap', type='fanout')

    def close_connection(self):
        self.connection.close()

    def send_message(self, message):
        body = json.dumps(message.to_json())
        self.channel.basic_publish(exchange='fox_scrap', routing_key='', body=body,  properties=pika.BasicProperties(delivery_mode=2))
