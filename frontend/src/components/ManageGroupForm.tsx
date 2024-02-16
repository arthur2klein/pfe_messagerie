import {useState} from 'react';
import './ManageGroupForm.css'
import UserService from '../services/UserService';

const ConnectionForm: React.FC = () => {

  const [formData, setFormData] = useState({
    old_name: '',
    new_name: '',
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
      if (formData.old_name == "") {
        UserService.receiveGroupCreation(formData.new_name);
      } else {
        UserService.receiveGroupChange(formData.old_name, formData.new_name);
      }
    } catch (error) {
      if (error instanceof Error) {
        setErrorMessage(error.message)
      }
    }
  };

  return (
    <div className="form">
      <h1>Manage your discussion groups</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-field">
          <label>Old name (left blank for new): </label>
          <input
            type="text"
            name="old_name"
            value={formData.old_name}
            onChange={handleChange}
          />
        </div>
        <div className="form-field">
          <label>New name: </label>
          <input
            type="text"
            name="new_name"
            value={formData.new_name}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      {errorMessage && <div className="toast">{ errorMessage }</div>}
    </div>
  );

}

export default ConnectionForm;
