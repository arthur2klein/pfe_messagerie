import {useNavigate} from 'react-router-dom';
import './ManagePage.css'
import UserService from '../services/UserService';
import {useEffect, useState} from 'react';
import ManageGroupForm from '../components/ManageGroupForm';
import SelectGroupComponent from '../components/SelectGroupComponent';
import Group from '../models/Group';
import AddGroupForm from '../components/AddGroupForm';

const ManagePage: React.FC = () => {
  const navigate = useNavigate();
  const groups = UserService.getGroups();
  const [selectedGroup, setSelectedGroup] = useState<Group>({
    id: '',
    name: '',
  });
  const handleGroupChange = (selectedGroupId: string) => {
    setSelectedGroup(groups[selectedGroupId]);
  };

  useEffect(() => {
    const isConnected = UserService.isConnected();
    if (!isConnected) {
      navigate('/connection')
    }
  }, [navigate]);

  return (
    <div className="container manage-page">
      <SelectGroupComponent groups={groups} selectedGroup={selectedGroup} onGroupGhange={handleGroupChange} />
      <ManageGroupForm group={selectedGroup} />
      <AddGroupForm />
    </div>
  );
}

export default ManagePage;
