import Message from '../models/Message';
import UserService from '../services/UserService';
import './MessageComponent.css';

interface MessageComponentProps {
  message: Message,
}

const MessageComponent: React.FC<MessageComponentProps> = (
  props
) => {
  const sender = UserService.getUserFromId(props.message.sender_id)
  const isSender = UserService.getUser()?.id === sender?.id;
  const receiver = UserService.getGroupFromId(props.message.receiver_group_id)
  const date = new Date(props.message.date * 1000);
  return (
    <div className={`message ${isSender? "sender": "receiver"}`}>
      <div className="message-content">{ props.message.content }</div>
      <div className="message-sender">{ sender?.name || '' } { sender?.first_name || '' }</div>
      <div className="message-receiver">{ receiver?.name || '' }</div>
      <div className="message-date">{ date.toLocaleString() }</div>
    </div>
  );
}

export default MessageComponent;
