import {useEffect, useState} from "react";
import UserService from "../services/UserService";
import User from "../models/User";
import './AdminComponent.css';

const AdminComponent: React.FC  = () => {
  const [allUsers, setAllUsers] = useState<User[]>([]);
  const fetchData = async () => {
    const data = await UserService.getAllUsers();
    setAllUsers(data);
  }
  useEffect(() => {
    fetchData();
  }, []);

  const deleteUser = (user_id: string) => {
    UserService.deleteUser(user_id);
  }

  return (
    <div className="listUsers">
    {allUsers.map((user) => {
      return (
        <div className="user" key={user.id}>
          <p>{user.name}</p>
          <p>{user.first_name}</p>
          <p>{user.email}</p>
          <button>View Activity</button>
          <button onClick={() => deleteUser(user.id)}>Delete</button>
        </div>
      );
    })}
    </div>
  );
}

export default AdminComponent;
