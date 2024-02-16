import {useEffect} from 'react';
import './ManagePage.css'
import UserService from '../services/UserService';
import {useNavigate} from 'react-router-dom';

const UserPage: React.FC = () => {

  const navigate = useNavigate();

  useEffect(() => {
    const isConnected = UserService.isConnected();
    if (!isConnected) {
      navigate('/connection')
    }
  }, [navigate]);

  return (
    <div className="container">
      <h1>This page will allow the user to modify its account and disconnect.</h1>
    </div>
  );
}

export default UserPage;
