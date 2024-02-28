import User from "../models/User";
import Group from "../models/Group";
import Message from "../models/Message";

const apiUrl: string = "api"
const apiPort: string = "8000"

class UserService {
  static currentUser: User|undefined = undefined;

  // Test data
  static test_messages: Array<Message> = [
    {
      id: '0',
      content: 'test',
      sender_id: '1',
      receiver_group_id: '1',
      date: 0,
    },
    {
      id: '1',
      content: 'This is a test message',
      sender_id: '2',
      receiver_group_id: '1',
      date: 1,
    },
    {
      id: '2',
      content: 'This is an other one',
      sender_id: '1',
      receiver_group_id: '1',
      date: 2,
    },
    {
      id: '3',
      content: 'tE5!',
      sender_id: '1',
      receiver_group_id: '1',
      date: 3,
    },
    {
      id: '4',
      content: 'abcdefg',
      sender_id: '1',
      receiver_group_id: '1',
      date: 4,
    },
  ];

  private static testUser: User = {
    id: '1',
    name: 'doe',
    first_name: 'john',
    email: 'e@mail.com',
    join_date: 1000,
    auth_id: '0',
  }

  private static testGroups: Record<string, Group> = {
    '1':  {id: '1',  name: 'groupe1',  },
    '2':  {id: '2',  name: 'groupe2',  },
    '3':  {id: '3',  name: 'groupe3',  },
    '4':  {id: '4',  name: 'groupe4',  },
    '5':  {id: '5',  name: 'groupe5',  },
    '6':  {id: '6',  name: 'groupe6',  },
    '7':  {id: '7',  name: 'groupe7',  },
    '8':  {id: '8',  name: 'groupe8',  },
    '9':  {id: '9',  name: 'groupe9',  },
    '10': {id: '10', name: 'groupe10', },
  };

  static async getUserFromId(id: string): Promise<User | null> {
    try {
      const response = await fetch(`${apiUrl}:${apiPort}/user/get/${id}`);
      const json = await response.json();
      if (json['error'] !== undefined) {
        console.error(
          `Error while fetching user for id ${id}: ${json['error']}`,
        );
        return null;
      }
      return json['user'] as User;
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  static async getGroupFromId(id: string): Promise<Group | null> {
    try {
      const response = await fetch(`${apiUrl}:${apiPort}/group/${id}`);
      const json = await response.json();
      if (json['error'] !== undefined) {
        console.error(
          `Error while fetching group for id ${id}: ${json['error']}`,
        );
        return null;
      }
      return json['group'] as Group;
    } catch (error) {
      console.error(error);
      return null;
    }
  }


  static async getGroups(): Promise<Record<string, Group>> {
    if (UserService.currentUser === undefined) {
      console.error(
        `Error while fetching groups for user: currentUser undefined`,
      );
    return {};
    }
    try {
      const user_id = UserService.currentUser.id;
      const response = await fetch(
        `${apiUrl}:${apiPort}/group/get_by_user/${user_id}`
      );
      const json = await response.json();
      if (json['error'] !== undefined) {
        console.error(
          `Error while fetching groups for user_id ${user_id}: ${json['error']}`,
        );
        return {};
      }
      return json['groups'];
    } catch (error) {
      console.error(error);
      return {};
    }
  }

  static async getAllMessages(groupId: string): Promise<Message[]> {
    try {
      const response = await fetch(
        `${apiUrl}:${apiPort}/message/get/group/${groupId}`
      );
      const json = await response.json();
      if (json['error'] !== undefined) {
        console.error(
          `Error while fetching groups for user_id ${groupId}: ${json['error']}`,
        );
        return [];
      }
      return json['message'];
    } catch (error) {
      console.error(error);
      return [];
    }
  }

  static isConnected(): boolean {
    return this.currentUser !== undefined;
  }

  static getUser(): User | undefined {
    return this.currentUser;
  }

  static async addUser(user: User): Promise<User|null> {
    try {
      const response = await fetch(
        `${apiUrl}:${apiPort}/user/new`,
        {
          method: 'POST',
          headers: { 'Content-type': 'application/json' },
          body: JSON.stringify({
            name: user.name,
            first_name: user.first_name,
            email: user.email,
            join_date: user.join_date,
            auth_id: user.auth_id
          }),
        },
      );
      const json = await response.json();
      if (json['error'] !== undefined) {
        console.error(
          `Error while creating the user $user: ${json['error']}`,
        );
        return null;
      } 
      return json['user'] as User;
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  static async receiveInscription(formData: {
    name: string;
    first_name: string;
    email: string;
    password: string;
    validate_password: string;
  }) {
    const formValidation = this.validateInscriptionForm(formData)
    if (formValidation !== "") {
      throw new Error(formValidation);
    }
    else {
      const { password, validate_password, ...dataWithout } = formData;
      const auth_id = this.createAuth({
        'login': formData.email,
        'password': password,
      });
      const user = await this.addUser({
        id: '',
        auth_id: auth_id,
        ...dataWithout,
        join_date: Date.now(),
      })
      if (user !== null) {
        UserService.currentUser = user;
      }
    }
  }

  static createAuth(auth_info: {login: string; password: string;}): string {
    throw new Error("Method not implemented.");
  }

  static changePassword(new_password: string) {
    throw new Error("Method not implemented.");
  }

  static receiveConnection(formData: {
    email: string;
    password: string;
  }) {
    if (
      formData.email === this.testUser.email &&
      formData.password === "password"
    ) {
      this.currentUser = this.testUser;
    } else {
      throw new Error("User not found");
    }
  }

  static receiveChange(formData: {
    name: string;
    first_name: string;
    password: string;
    validate_password: string;
  }) {
    const formValidation = this.validateChange(formData)
    if (formValidation !== "") {
      throw new Error(formValidation);
    }
    UserService.changeUser(formData.name, formData.first_name);
    UserService.changePassword(formData.password);
  }

  static async changeUser(name: string, first_name: string) {
    if (UserService.currentUser === undefined) {
      console.error('No current user when changing infos');
      return;
    }
    const user: User = UserService.currentUser;
    try {
      const response = await fetch(
        `${apiUrl}:${apiPort}/user/modify/${user.id}`,
        {
          method: 'PUT',
          headers: { 'Content-type': 'application/json' },
          body: JSON.stringify({
            new_id: user.id,
            new_name: name,
            new_first_name: first_name,
            new_email: user.email,
          }),
        },
      );
      const json = await response.json();
      if (json['error'] !== undefined) {
        console.error(
          `Error while creating the user $user: ${json['error']}`,
        );
      } 
      UserService.currentUser = json['user'] as User;
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  static validateInscriptionForm(formData: {
    name: string;
    first_name: string;
    email: string;
    password: string;
    validate_password: string;
  }): string {
    if (formData.password !== formData.validate_password)
      return 'Passwords don\'t match.';
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      return 'Invalid email format.';
    }
    if (formData.first_name === "") {
      return 'Empty first name forbidden';
    }
    if (formData.name === "") {
      return 'Empty name forbidden';
    }
    if (this.isWeakPassword(formData.password)) {
      return 'Password too weak';
    }
    if (this.getUserEmail(formData.email) !== undefined) {
      return 'Email already in use';
    }
    return '';
  }

  static validateChange(formData: {
    name: string;
    first_name: string;
    password: string;
    validate_password: string;
  }): string {
    if (formData.password !== formData.validate_password)
      return 'Passwords don\'t match.';
    if (formData.first_name === "") {
      return 'Empty first name forbidden';
    }
    if (formData.name === "") {
      return 'Empty name forbidden';
    }
    if (this.isWeakPassword(formData.password)) {
      return 'Password too weak';
    }
    return '';
  }

  static isWeakPassword = (password: string): boolean => {
    const hasMinimumLength = password.length >= 6;
    const hasUppercase = /[A-Z]/.test(password);
    const hasSpecialCharacter = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    const hasNumber = /\d/.test(password);
    return !(
      hasMinimumLength &&
        hasUppercase &&
        hasSpecialCharacter &&
        hasNumber
    );
  };

  static async getUserEmail(email: string): Promise<User|null> {
    try {
      const response = await fetch(
        `${apiUrl}:${apiPort}/user/get_by_email/${email}`
      );
      const json = await response.json();
      if (json['error'] !== undefined) {
        console.error(
          `Error while fetching user for email ${email}: ${json['error']}`,
        );
        return null;
      }
      return json['user'] as User;
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  static disconnect() {
    this.currentUser = undefined;
  }

  static async receiveGroupChange(id: string, new_name: string) {
    try {
      const response = await fetch(
        `${apiUrl}:${apiPort}/user/new`,
        {
          method: 'POST',
          headers: { 'Content-type': 'application/json' },
          body: JSON.stringify({
            group_id: id,
            new_name: new_name,
          }),
        },
      );
      const json = await response.json();
      if (json['error'] !== undefined) {
        console.error(
          `Error while renaming the group ${id}: ${json['error']}`,
        );
      } 
    } catch (error) {
      console.error(error);
    }
  }

  static async receiveGroupCreation(new_name: string): Promise<Group|null> {
    try {
      const response = await fetch(
        `${apiUrl}:${apiPort}/user/new`,
        {
          method: 'POST',
          headers: { 'Content-type': 'application/json' },
          body: JSON.stringify({
            name: new_name,
          }),
        },
      );
      const json = await response.json();
      if (json['error'] !== undefined) {
        console.error(
          `Error while creating the group ${new_name}: ${json['error']}`,
        );
        return null;
      } 
      return json['group'] as Group;
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  static async sendMessage(messageContent: string, group_id: string) {
    try {
      const response = await fetch(
        `${apiUrl}:${apiPort}/message/create`,
        {
          method: 'POST',
          headers: { 'Content-type': 'application/json' },
          body: JSON.stringify({
            content: messageContent,
            sender_id: UserService.currentUser!.id,
            receiver_group_id: group_id,
            date: Date.now()
          }),
        },
      );
      const json = await response.json();
      if (json['error'] !== undefined) {
        console.error(
          `Error while creating a message: ${json['error']}`,
        );
      } 
    } catch (error) {
      console.error(error);
    }
  }

  static async receiveGroupAdd(name: string): Promise<Group|null> {
    try {
      const response = await fetch(
        `${apiUrl}:${apiPort}/group/new`,
        {
          method: 'POST',
          headers: { 'Content-type': 'application/json' },
          body: JSON.stringify({
            name: name
          }),
        },
      );
      const json = await response.json();
      if (json['error'] !== undefined) {
        console.error(
          `Error while adding the group ${name}: ${json['error']}`,
        );
        return null;
      } 
      return json['group'] as Group;
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  static async receiveGroupGrow(group_id: string, user_email: string) {
    try {
      const user = await UserService.getUserEmail(user_email);
      if (user === null) {
        console.error(`No user with email ${user_email}`)
      }
      const user_id: string = user!.id;
      const response = await fetch(
        `${apiUrl}:${apiPort}/add_user/${group_id}/${user_id}`,
        {
          method: 'POST',
          headers: { 'Content-type': 'application/json' },
          body: JSON.stringify({
          }),
        },
      );
      const json = await response.json();
      if (json['error'] !== undefined) {
        console.error(
          `Error while adding the user ${user_email} to ${group_id}: ${json['error']}`,
        );
      } 
    } catch (error) {
      console.error(error);
    }
  }

}

export default UserService;
