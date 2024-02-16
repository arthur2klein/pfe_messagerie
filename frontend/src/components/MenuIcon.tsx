import {Link, Outlet} from "react-router-dom";
import "./MenuIcon.css"

interface MenuIconProps {
  icon: React.ElementType;
  name: string;
  to: string;
}

const MenuIcon: React.FC<MenuIconProps> = ({
  icon: Icon,
  name,
  to
}) => {
  return (
    <div className="menu-icon-container">
      <Link to={ to } >
        <Icon className="menu-icon" />
      </Link>
      <span className="menu-text">{ name }</span>
    </div>
  );
}

export default MenuIcon;
