from proton import Message, Messenger
from proton.handlers import MessagingHandler
from proton.reactor import Container, Handler
import os, random



# Variables to recognize
#   - Is sender or receiver
#   - If sender:
#       - Address of broker
#       - Source of messages
#       - Target of messages
#       - Delay between messages
#       - Size of messages
#   - If receiver:
#       - Address of broker
#       - Target to listen to

class RecurringPublisher(Handler):
    def __init__(self, server, address, period, min_msg_chars, max_msg_chars):
        self.server = server
        self.address = address
        self.period = period
        self.min_msg_chars = min_msg_chars
        self.max_msg_chars = max_msg_chars
        self.chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def on_reactor_init(self, event):
        self.container = event.reactor
        self.container.schedule(self.period, self)
        conn = self.container.connect(self.server)
        self.sender = self.container.create_sender(conn, self.address)

    def on_timer_task(self, event):
        try:
            self.sender.send(Message(body=self.get_msg()))
        finally:
            self.container.schedule(self.period, self)

    def get_msg(self):
        msg_size = self.get_msg_size()
        return ''.join([self.chars[random.randint(0, len(self.chars) - 1)] for _ in range(msg_size)])


    def get_msg_size(self):
        if self.max_msg_chars == self.min_msg_chars:
            return self.max_msg_chars
        else:
            return random.randint(self.min_msg_chars, self.max_msg_chars)

class Consumer(MessagingHandler):
    def __init__(self, server, address):
        super(Consumer, self).__init__()
        self.server = server
        self.address = address

    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.address)

    def on_message(self, event):
        print(event.message.body)


server = os.getenv("AMQP_SERVER", "activemq:5672")
address = os.getenv("AMQP_ADDRESS", "examples")
recurring_publisher_period = float(os.getenv("RECURRING_PUBLISHER_PERIOD", "1.0"))
recurring_publisher_min_msg_len = int(os.getenv("RECURRING_PUBLISHER_MIN_MSG_LEN", "10"))
recurring_publisher_max_msg_len = int(os.getenv("RECURRING_PUBLISHER_MAX_MSG_LEN", "10"))

handler = RecurringPublisher(server, address, recurring_publisher_period, recurring_publisher_min_msg_len, recurring_publisher_max_msg_len) if os.getenv("TEST_ROLE", "publisher") == "publisher" else Consumer(server, address)
Container(handler).run()



