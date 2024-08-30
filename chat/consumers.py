import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("有人來連接")
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        print("room_group_name-->", self.room_group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        print("客戶端斷開")
        # Leave room group
        print("room_group_name-->", self.room_group_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("接收瀏覽器的訊息-->", text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        print("room_group_name-->", self.room_group_name)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        print("接收群組的訊息-->", event)
        message = event["message"]

        # Send message to WebSocket
        print("message-->", message)
        self.send(text_data=json.dumps({"message": message}))