interface Message {
  id: string,
  content: string,
  sender_id: string,
  receiver_group_id: string,
  date: number,
}

export default Message;
