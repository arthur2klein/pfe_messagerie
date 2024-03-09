import {ToastContainer} from "react-toastify"
import 'react-toastify/dist/ReactToastify.css';

const NotificationComponent: React.FC = () => {
  return <ToastContainer
    position="bottom-center"
    autoClose={5000}
    hideProgressBar={false}
    newestOnTop={false}
    closeOnClick={true}
    rtl={false}
    pauseOnFocusLoss={true}
    draggable={true}
    pauseOnHover={true}
  />
}

export default NotificationComponent;
