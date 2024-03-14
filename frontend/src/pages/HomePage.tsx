import AdminComponent from '../components/AdminComponent';
import UserService from '../services/UserService';
import './HomePage.css'

const HomePage: React.FC = () => {
  if (UserService.isAdmin()) {
    return <div className='container'><AdminComponent /></div>;
  }
  return (
    <div className="container">
      <h1>Welcome to our Messaging app !!!</h1>
      <span>Every icon will redirect you to the Connection/Inscription page if you are not connected.</span>
      <span>You can use the manage icon to manage the current conversation.</span>
      <span>The Conv. icon directs you to the selected conversation.</span>
      <span>The Profile icon to the user management if connected.</span>
      <span>The Home icon directs you to this page.</span>
    </div>
  );
}

export default HomePage;

