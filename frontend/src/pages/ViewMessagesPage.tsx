import {useEffect, useRef, useState} from 'react';
import UserService from '../services/UserService';
import './ViewMessagesPage.css'
import {useNavigate} from 'react-router-dom';
import Group from '../models/Group';
import Message from '../models/Message';
import MessageComponent from '../components/MessageComponent';
import SelectGroupComponent from '../components/SelectGroupComponent';
import CreateMessageComponent from '../components/CreateMessageComponent';
import Encryption from '../services/Encryption';

const ViewMessagesPage: React.FC = () => {
  const [socket, setSocket] = useState<WebSocket|null>(null);

  const [groups, setGroups] = useState<Record<string, Group>>({});
  const fetchData = async () => {
    const groupsData = await UserService.getGroups();
    setGroups(groupsData);
  }
  useEffect(() => {
    fetchData();
  }, []);

  const [messages, setMessages] = useState<Message[]>([]);

  const navigate = useNavigate();
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
      const isConnected = UserService.isConnected();
      if (!isConnected) {
      navigate('/connection')
      }
      }, [navigate]);

  // Scroll to the bottom of the container when messages are updated
  useEffect(() => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop =
        messagesContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const [selectedGroup, setSelectedGroup] = useState<Group>({
    id: '',
    name: '',
  });

  const changeSocket = (selectedGroupId: string) => {
    console.log(`Creating socket for ${selectedGroupId}`);
    socket?.close();
    const new_socket = UserService.create_socket(selectedGroupId);
    new_socket.addEventListener('message', (event) => {
      console.log(`Received message ${event.data}`);
      const messageData = JSON.parse(event.data) as Message;
      addMessage(messageData);
    });
    setSocket(new_socket);
  }

  const addMessage = (messageData: Message) => {
    setMessages((prevMessages) => {
      const updatedMessages = [...prevMessages, messageData];
      return updatedMessages;
    });
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop =
        messagesContainerRef.current.scrollHeight;
    }
  }

  const handleGroupChange = async (selectedGroupId: string) => {
    if (selectedGroupId !== "") {
      setSelectedGroup(groups[selectedGroupId]);
    } else {
      setSelectedGroup({id: '', name: ''});
    }
    setMessages(await UserService.getAllMessages(selectedGroupId));
    console.log(`onGroupChange: ${messages}`);
    changeSocket(selectedGroupId);
  };

  const receiveMessage = async (messageContent: string): Promise<void> => {
    // const encrypted = await Encryption.encrypt(
    //   messageContent,
    //   UserService.currentUser!.id,
    //   selectedGroup.id
    // );
    const new_message = await UserService.sendMessage(
      messageContent,
      selectedGroup.id
    );
    console.log(`Sent ${new_message} via socket`);
    socket?.send(JSON.stringify(new_message));
  };

  return (
    <div className="container messages-page">
      <SelectGroupComponent groups={groups} selectedGroup={selectedGroup} onGroupGhange={handleGroupChange} />
    <div className="view-message" ref={messagesContainerRef}>
      {selectedGroup.id === ""?
        <h1>Please chose a group to display the messages</h1>
        :messages.map(m => (
          <MessageComponent message={m} group_id={selectedGroup.id} />
        ))
      }
      {selectedGroup.id !== ""?
        <CreateMessageComponent onSendMessage={receiveMessage} />
        :null
      }
    </div>
  </div>
  );
}

export default ViewMessagesPage;
