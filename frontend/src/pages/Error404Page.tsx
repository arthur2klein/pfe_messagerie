import {Link} from 'react-router-dom';
import './Error404Page.css'

const Error404Page: React.FC = () => {
  return (
    <div className="container">
      <h1>Error 404</h1>
      <span>It seems that you are trying to access a page that does not exist.</span>
      <span><Link to={"/"}>Here is a link to our home page if you are lost.</Link></span>
    </div>
  );
}

export default Error404Page;
