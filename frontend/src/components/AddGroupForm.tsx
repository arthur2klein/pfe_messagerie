import {useState} from 'react';
import './AddGroupForm.css'
import UserService from '../services/UserService';
import Group from '../models/Group';
import Encryption from '../services/Encryption';

interface GroupAddComponentProps {
  onGroupAdd: (newGroup: Group) => void;
} 

const AddGroupForm: React.FC<GroupAddComponentProps> = ({ onGroupAdd }) => {

  const [formData, setFormData] = useState({
    name: '',
  });
  
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const group = await UserService.receiveGroupAdd(formData.name);
      if (group !== null && UserService.currentUser !== undefined) {
        UserService.receiveGroupGrow(group.id, UserService.currentUser.email);
        Encryption.createKey(group.id, UserService.currentUser!.id);
        onGroupAdd(group);
      }
    } catch (error) {
      if (error instanceof Error) {
        setErrorMessage(error.message)
      }
    }
  };

  return (
    <div className="add-group form">
      <h1>Add your new discussion groups</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-field">
          <label>Name of my new group: </label>
          <input
            type="text"
            name="name"
            placeholder="Name of the group"
            value={formData.name}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      {errorMessage && <div className="toast">{ errorMessage }</div>}
    </div>
  );

}

export default AddGroupForm;
