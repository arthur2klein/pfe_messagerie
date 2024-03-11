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

  const [groups, setGroups] = useState<Record<string, Group>>({});
  const fetchData = async () => {
    const groupsData = await UserService.getGroups();
    setGroups(groupsData);
  }
  useEffect(() => {
    fetchData();
  }, []);

  const [selectedGroup, setSelectedGroup] = useState<Group>({
    id: '',
    name: '',
  });
  const handleGroupChange = (selectedGroupId: string) => {
    setSelectedGroup(groups[selectedGroupId]);
  };

  const addGroup = (newGroup: Group) => {
    setGroups((prevGroups) => {
      const group_id = newGroup.id;
      const updatedGroups = {...prevGroups, [group_id]: newGroup};
      return updatedGroups;
    });
  }


  useEffect(() => {
    const isConnected = UserService.isConnected();
    if (!isConnected) {
      navigate('/connection')
    }
  }, [navigate]);

  return (
    <div className="container manage-page">
      <SelectGroupComponent
        groups={groups}
        selectedGroup={selectedGroup}
        onGroupGhange={handleGroupChange}
      />
      {selectedGroup.id?
        <ManageGroupForm group={selectedGroup} />
        :<h1>Select a group to edit it</h1>
      }
      <AddGroupForm onGroupAdd={addGroup} />
    </div>
  );
}

export default ManagePage;
