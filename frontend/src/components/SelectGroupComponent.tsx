import Group from '../models/Group';
import './SelectGroupComponent.css'

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
  return (
    <div className="select-group">
      <select
        value={selectedGroup.id || ''}
        onChange={
          (e: React.ChangeEvent<HTMLSelectElement>) =>
            onGroupGhange(e.target.value)
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
