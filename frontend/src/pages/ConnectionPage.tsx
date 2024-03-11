import ConnectionForm from '../components/ConnectionForm';
import InscriptionForm from '../components/InscriptionForm';
import './ConnectionPage.css'

const ConnectionPage: React.FC = () => {
  return (
    <div className="container share-two">
      <InscriptionForm />
      <ConnectionForm />
    </div>
  );
}

export default ConnectionPage;
