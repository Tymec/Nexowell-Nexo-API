from .NexoVisionClient import NexoVisionClient
import ujson as json
import asyncio


class NexoWrapper:
    def __init__(self, host, password):
        self.nexo_client = NexoVisionClient(host)
        self.nexo_client.initialize_connection(password)
        self.nexo_client.clear_server_buffer_queue()
        
        self.loop = asyncio.get_event_loop()
        cors = asyncio.wait([self.check_connection()])
        self.loop.run_until_complete(cors)
        
    async def check_connection(self):
        while True:
            await asyncio.sleep(1)
            alive = self.nexo_client.check_connection()
            print(alive)
            # return alive
     
    def process_queue(self, queue):
        states = {}
        
        for item in queue:
            states[item] = self.get_state(item)
            
        return states
     
    def disconnect(self):
        self.nexo_client.disconnect()
     
    def get_state(self, name):
        state = self.nexo_client.system_c(name, '?')
        if not state:
            state = self.get_state(name)
        return int(state)
    
    def set_state(self, name, state):
        if state is not 1 and state is not 0:
            self.nexo_client.log("Wrong value", 'error')
            return
        self.nexo_client.system_c(name, state)
        new_state = self.get_state(name)
        return new_state
    
    def import_resource(self, resource):
        res = self.nexo_client.import_resource(resource)
        return res
        
    def import_resources(self):
        res = self.nexo_client.import_resources()
        return res
