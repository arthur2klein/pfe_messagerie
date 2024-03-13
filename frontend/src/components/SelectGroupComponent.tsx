import {useState} from 'react';
import Group from '../models/Group';
import './SelectGroupComponent.css'
import User from '../models/User';
import UserService from '../services/UserService';

interface SelectGroupProps {
  groups: Record<string, Group>;
  selectedGroup: Group;
  onGroupGhange: (selectedGroupId: string) => void;
}

const SelectGroupComponent: React.FC<SelectGroupProps> = ({
  groups,
  selectedGroup,
  onGroupGhange
}) => {
  const [users, setUsers] = useState<User[]>([]);
  async function load_group_members(group_id: string) {
    setUsers(await UserService.getUserGroup(group_id));
  }

  return (
    <div className="select-group">
      <div className="members">
        {users.map((u) => (
          <div className="member">{u.name} {u.first_name}</div>
        ))}
      </div>
      <select
        value={selectedGroup.id || ''}
        onChange={
          (e: React.ChangeEvent<HTMLSelectElement>) => {
              const v = e.target.value;
              if (!v) return;
              load_group_members(v);
              onGroupGhange(v);
            }
        }
      >
        <option value="">Select a group</option>
        {Object.values(groups).map(g => (
          <option key={g.id} value={g.id}>{ g.name }</option>
        ))}
      </select>
    </div>
  );
};

export default SelectGroupComponent;
