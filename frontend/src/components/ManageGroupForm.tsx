import {useState} from 'react';
import './ManageGroupForm.css'
import UserService from '../services/UserService';
import Group from '../models/Group';
import Encryption from '../services/Encryption';

interface ManageGroupFormProps {
  group: Group,
}

const ManageGroupForm: React.FC<ManageGroupFormProps> = ({group}) => {

  const [formData, setFormData] = useState({
    new_name: group.name,
    user_email: '',
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
      if (formData.new_name !== group.name && formData.new_name !== "") {
        UserService.receiveGroupChange(group.id, formData.new_name);
      }    
      if (formData.user_email !== "") {
        UserService.receiveGroupGrow(group.id, formData.user_email);
        Encryption.createKey(group.id, UserService.currentUser!.id);
      }    
    } catch (error) {
      if (error instanceof Error) {
        setErrorMessage(error.message)
      }
    }
  };

  return (
    <div className="manage-group form">
      <h1>Manage your discussion groups</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-field">
          <label>New name: </label>
          <input
            type="text"
            name="new_name"
            placeholder={group.name}
            value={formData.new_name}
            onChange={handleChange}
          />
        </div>
        <div className="form-field">
          <label>Email of user to add: </label>
          <input
            type="email"
            name="user_email"
            placeholder="User to add"
            value={formData.user_email}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      {errorMessage && <div className="toast">{ errorMessage }</div>}
    </div>
  );

}

export default ManageGroupForm;
