import {useNavigate} from 'react-router-dom';
import './ManagePage.css'
import UserService from '../services/UserService';
import {useEffect} from 'react';
import ManageGroupForm from '../components/ManageGroupForm';

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
      <ManageGroupForm />
    </div>
  );
}

export default ManagePage;
