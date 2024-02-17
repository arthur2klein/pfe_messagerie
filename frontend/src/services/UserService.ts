import User from "../models/User";
import Group from "../models/Group";
import Message from "../models/Message";

class UserService {
  static receiveGroupAdd(name: string) {
    throw new Error('Method not implemented.');
  }
  static receiveGroupGrow(group_id: string, user_email: string) {
    throw new Error('Method not implemented.');
  }

  static getUserFromId(id: string): User | null {
    if (id == '1') {
      return this.testUser;
    }
    return null;
  }

  static getGroupFromId(id: string): Group | null {
    return this.testGroups[id];
  }

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

  static getGroups(): Record<string, Group> {
    return this.testGroups;
  }

  static getAllMessages(groupId: string): Message[] {
    if (groupId != '1') return [];
    return [
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
  }

  private static currentUser: User | undefined = this.testUser;

  static isConnected(): boolean {
    return this.currentUser !== undefined;
  }

  static getUser(): User | undefined {
    return this.currentUser;
  }

  static addUser(data: {
    name: string;
    first_name: string;
    email: string;
    password: string;
    join_date: number;
  }) {
    throw new Error("Method not implemented.");
  }

  static receiveInscription(formData: {
    name: string;
    first_name: string;
    email: string;
    password: string;
    validate_password: string;
  }) {
    const formValidation = this.validateInscriptionForm(formData)
    if (formValidation != "") {
      throw new Error(formValidation);
    }
    else {
      const { validate_password, ...dataWithout } = formData;
      this.addUser({
        ...dataWithout,
        join_date: Date.now(),
      })
    }
  }

  static receiveConnection(formData: {
    email: string;
    password: string;
  }) {
    if (
      formData.email == this.testUser.email &&
      formData.password == "password"
    ) {
      this.currentUser = this.testUser;
    }
    throw new Error("User not found");
  }

  static receiveChange(formData: {
    name: string;
    first_name: string;
    password: string;
    validate_password: string;
  }) {
    const formValidation = this.validateChange(formData)
    if (formValidation != "") {
      throw new Error(formValidation);
    }
    this.currentUser!.name = formData.name;
    this.currentUser!.first_name = formData.first_name;
  }

  static validateInscriptionForm(formData: {
    name: string;
    first_name: string;
    email: string;
    password: string;
    validate_password: string;
  }): string {
    if (formData.password != formData.validate_password)
      return 'Passwords don\'t match.';
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      return 'Invalid email format.';
    }
    if (formData.first_name == "") {
      return 'Empty first name forbidden';
    }
    if (formData.name == "") {
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
    if (formData.password != formData.validate_password)
      return 'Passwords don\'t match.';
    if (formData.first_name == "") {
      return 'Empty first name forbidden';
    }
    if (formData.name == "") {
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

  static getUserEmail(email: string) {
    if (email == this.testUser.email) {
      return this.testUser;
    }
  }

  static disconnect() {
    this.currentUser = undefined;
  }

  static receiveGroupChange(id: string, new_name: string) {
    throw new Error('Method not implemented.');
  }

  static receiveGroupCreation(new_name: string) {
    throw new Error('Method not implemented.');
  }
  
}

export default UserService;
