import {useState} from 'react';
import './InscriptionForm.css'
import UserService from '../services/UserService';
import {useNavigate} from 'react-router-dom';

const InscriptionForm: React.FC = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: '',
    first_name: '',
    email: '',
    password: '',
    validate_password: '',
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
      const success = await UserService.receiveInscription(formData);
      if (success) {
        navigate('/');
      }
    } catch (error) {
      if (error instanceof Error) {
        setErrorMessage(error.message)
      }
    }
  };

  return (
    <div className="inscription-form">
      <h1>Create your account</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-field">
          <label>Name: </label>
          <input
            type="text"
            name="name"
            placeholder="name"
            value={formData.name}
            onChange={handleChange}
          />
        </div>
        <div className="form-field">
          <label>First name: </label>
          <input
            type="text"
            name="first_name"
            placeholder="first name"
            value={formData.first_name}
            onChange={handleChange}
          />
        </div>
        <div className="form-field">
          <label>E-mail: </label>
          <input
            type="email"
            name="email"
            placeholder="email"
            value={formData.email}
            onChange={handleChange}
          />
        </div>
        <div className="form-field">
          <label>Password: </label>
          <input
            type="password"
            name="password"
            placeholder="password"
            value={formData.password}
            onChange={handleChange}
          />
        </div>
        <div className="form-field">
          <label>Validate your password: </label>
          <input
            type="password"
            name="validate_password"
            placeholder="password confirmation"
            value={formData.validate_password}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      {errorMessage && <div className="toast">{ errorMessage }</div>}
    </div>
  );

}

export default InscriptionForm;
