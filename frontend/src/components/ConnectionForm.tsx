import {useState} from 'react';
import './ConnectionForm.css'
import UserService from '../services/UserService';

const ConnectionForm: React.FC = () => {

  const [formData, setFormData] = useState({
    email: '',
    password: '',
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
      UserService.receiveConnection(formData);
    } catch (error) {
      if (error instanceof Error) {
        setErrorMessage(error.message)
      }
    }
  };

  return (
    <div className="connection-form">
      <h1>Connect to your account</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-field">
          <label>E-mail: </label>
          <input
            type="email"
            name="email"
            placeholder="Email of your accound"
            value={formData.email}
            onChange={handleChange}
          />
        </div>
        <div className="form-field">
          <label>Password: </label>
          <input
            type="password"
            name="password"
            placeholder="Password of your account"
            value={formData.password}
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
