import {useEffect, useState} from 'react';
import UserService from '../services/UserService';
import './ViewMessagesPage.css'
import {useNavigate} from 'react-router-dom';
import Group from '../models/Group';
import Message from '../models/Message';
import MessageComponent from '../components/MessageComponent';
import SelectGroupComponent from '../components/SelectGroupComponent';
import CreateMessageComponent from '../components/CreateMessageComponent';
import {Socket} from 'socket.io-client';

const ViewMessagesPage: React.FC = () => {
  const [socket, setSocket] = useState<Socket|null>(null);

  const [groups, setGroups] = useState<Record<string, Group>>({});
  const fetchData = async () => {
    const groupsData = await UserService.getGroups();
    setGroups(groupsData);
  }
  useEffect(() => {
    fetchData();
  }, []);

  const navigate = useNavigate();

  useEffect(() => {
      const isConnected = UserService.isConnected();
      if (!isConnected) {
      navigate('/connection')
      }
      }, [navigate]);

  const [selectedGroup, setSelectedGroup] = useState<Group>({
    id: '',
    name: '',
  });

  const [messages, setMessages] = useState<Message[]>([]);

  const changeSocket = (selectedGroupId: string) => {
    console.log(`Creating socket for ${selectedGroupId}`);
    socket?.disconnect();
    const new_socket = UserService.create_socket(selectedGroupId);
    new_socket.on('message', (data) => {
      console.log(`Received message ${data}`);
      messages.push(data.json as Message);
    });
    setSocket(new_socket);
  }

  const handleGroupChange = async (selectedGroupId: string) => {
    if (selectedGroupId !== "") {
      setSelectedGroup(groups[selectedGroupId]);
    } else {
      setSelectedGroup({id: '', name: ''});
    }
    setMessages(await UserService.getAllMessages(selectedGroupId));
    changeSocket(selectedGroupId);
  };

  const receiveMessage = (messageContent: string): void => {
    const new_message = UserService.sendMessage(
      messageContent,
      selectedGroup.id
    );
    if (socket) {
      socket.send(new_message);
    } 
  };

  return (
    <div className="container messages-page">
      <SelectGroupComponent groups={groups} selectedGroup={selectedGroup} onGroupGhange={handleGroupChange} />
    <div className="view-message">
      {selectedGroup.id === ""?
        <h1>Please chose a group to display the messages</h1>
        :messages.map(m => (
          <MessageComponent message={m} />
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
