import logging
import settings
from freeswitchESL import ESL

logger = logging.getLogger(__name__)

class EslListener:
    def __init__(self, on_event, event_filters):
        self.connection = None
        self.on_event = on_event
        self.event_filters = event_filters

    def listen_forever(self):
        while(True):
            try:
                event = self.receieve_event()
                if event:
                    self.on_event(event)
                else:
                    logger.info("no event")
            except:
                raise

    def reconnect_if_needed(self):
        if self.connection and self.connection.connected():
            return
        
        self.connection = ESL.ESLconnection(settings.ESL_HOST, settings.ESL_PORT, settings.ESL_SECRET)
        if self.connection.connected():
            if self.event_filters:
                self.connection.events("plain", " ".join(self.event_filters))
                return

        raise

    def receieve_event(self):
        self.reconnect_if_needed()
        return self.connection.recvEventTimed(2000)
