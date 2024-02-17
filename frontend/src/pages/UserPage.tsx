import {useEffect} from 'react';
import './UserPage.css'
import { VscDebugDisconnect } from "react-icons/vsc";
import UserService from '../services/UserService';
import {useNavigate} from 'react-router-dom';
import ChangeForm from '../components/ChangeForm';

const UserPage: React.FC = () => {

  const navigate = useNavigate();
  const isConnected = UserService.isConnected();

  useEffect(() => {
    const isConnected = UserService.isConnected();
    if (!isConnected) {
      navigate('/connection');
    }
  }, [navigate]);

  function handleDisconnect(): void {
    UserService.disconnect();
    navigate('/');
  }

  return isConnected ? (
    <div className="container">
      <ChangeForm />
      <button onClick={handleDisconnect} className="disconnect">Disconnect <VscDebugDisconnect /></button>
    </div>
    ): null;
}

export default UserPage;

