import {useEffect, useState} from 'react';
import UserService from '../services/UserService';
import './ViewMessagesPage.css'
import {useNavigate} from 'react-router-dom';
import Group from '../models/Group';
import Message from '../models/Message';
import MessageComponent from '../components/MessageComponent';
import SelectGroupComponent from '../components/SelectGroupComponent';

const ViewMessagesPage: React.FC = () => {

  const groups: Record<string, Group> = UserService.getGroups();

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

  const handleGroupChange = (selectedGroupId: string) => {
    if (selectedGroupId != "") {
      setSelectedGroup(groups[selectedGroupId]);
    } else {
      setSelectedGroup({id: '', name: ''});
    }
    setMessages(UserService.getAllMessages(selectedGroupId));
  };

  return (
    <div className="container messages-page">
      <SelectGroupComponent groups={groups} selectedGroup={selectedGroup} onGroupGhange={handleGroupChange} />
      <div className="view-message">
        {selectedGroup.id == ""?
          <h1>Please chose a group to display the messages</h1>
          :messages.map(m => (
            <MessageComponent message={m} />
          ))
        }
        {selectedGroup.id != ""?
          <div className="create-message">
            <h1>This will allow users to add messages</h1>
          </div>
          :null
        }
      </div>
    </div>
  );
}

export default ViewMessagesPage;
