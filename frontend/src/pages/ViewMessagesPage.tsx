import {useEffect} from 'react';
import UserService from '../services/UserService';
import './ViewMessagesPage.css'
import {useNavigate} from 'react-router-dom';

const ViewMessagesPage: React.FC = () => {

  const navigate = useNavigate();

  useEffect(() => {
    const isConnected = UserService.isConnected();
    if (!isConnected) {
      navigate('/connection')
    }
  }, [navigate]);

  return (
    <div className="container">
      <h1>This page will allow the user to select the discussion group and see the discussion.</h1>
    </div>
  );
}

export default ViewMessagesPage;
