interface User {
  id: string,
  name: string,
  first_name: string,
  email: string,
  join_date: number,
  auth_id: string
}

class UserService {

  private static testUser: User = {
    id: '1',
    name: 'doe',
    first_name: 'john',
    email: 'e@mail.com',
    join_date: 1000,
    auth_id: '0',
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

  static receiveGroupChange(old_name: string, new_name: string) {
    throw new Error('Method not implemented.');
  }

  static receiveGroupCreation(new_name: string) {
    throw new Error('Method not implemented.');
  }
  
}

export default UserService;
