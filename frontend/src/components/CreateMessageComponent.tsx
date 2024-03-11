import {FaPaperPlane} from 'react-icons/fa';
import './CreateMessageComponent.css'
import {useState} from 'react';

interface CreateMessageComponentProps {
  onSendMessage: (messageContent: string) => void;
}

const CreateMessageComponent: React.FC<CreateMessageComponentProps> = ({
  onSendMessage
}) => {
  const [messageContent, setMessageContent] = useState('');
  
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessageContent(e.target.value);
    adjustTextArea(e.target);
  }

  const handleKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const handleSendMessage = () => {
    if (messageContent.trim() !== '') {
      onSendMessage(messageContent);
      setMessageContent('');
    }
  }

  const adjustTextArea = (textarea: HTMLTextAreaElement) => {
    textarea.style.height = 'auto';
    textarea.style.height = `calc(${textarea.scrollHeight}px - 1rem`;
  }

  return (
    <div className="create-message">
      <textarea 
        className="message-input"
        placeholder="Type your message..."
        value={messageContent}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
      />
      <button className="send-message" onClick={handleSendMessage}>
        <FaPaperPlane />
      </button>
    </div>
  );
};

export default CreateMessageComponent;
