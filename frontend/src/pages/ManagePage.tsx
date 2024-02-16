import {useNavigate} from 'react-router-dom';
import './ManagePage.css'
import UserService from '../services/UserService';
import {useEffect} from 'react';

const ManagePage: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const isConnected = UserService.isConnected();
    if (!isConnected) {
      navigate('/connection')
    }
  }, [navigate]);

  return (
    <div className="container">
      <h1>This page will allow the user to create and modify its groups.</h1>
    </div>
  );
}

export default ManagePage;
