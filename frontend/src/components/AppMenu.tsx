import {FaHome, FaUser} from "react-icons/fa";
import {GoCommentDiscussion} from "react-icons/go";
import {IoSettingsSharp} from "react-icons/io5";
import MenuIcon from './MenuIcon';
import './AppMenu.css'

export const AppMenu: React.FC = () => {
  return (
    <nav className="app-menus">
        <MenuIcon icon={IoSettingsSharp} name="Manage" to="/manage" />
        <MenuIcon icon={GoCommentDiscussion} name="Conv." to="/messages" />
        <MenuIcon icon={FaUser} name="Profile" to="/user" />
        <MenuIcon icon={FaHome} name="Home" to="/" />
    </nav>
  );
};

