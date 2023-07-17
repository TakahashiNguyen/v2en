const obj = (ctx: string) => {
  return `[data-cy="${ctx}"]`;
};

export class userFunc {
  private randomUserName;
  private firstName;
  private lastName;
  private password;

  constructor() {
    const { randomUserName, firstName, lastName, password } = this.initValue();
    this.randomUserName = randomUserName;
    this.firstName = firstName;
    this.lastName = lastName;
    this.password = password;
    console.log('inited');
  }

  private initValue() {
    const randomUserName = Math.random().toString(36).substring(2, 8);
    const firstName = Math.random().toString(36).substring(2, 8);
    const lastName = Math.random().toString(36).substring(2, 8);
    const password = 'Vanh3006';

    return { randomUserName, firstName, lastName, password };
  }

  public userSignupFunc() {
    cy.get(obj('leftDrawer')).click();
    cy.get(obj('SignupButton')).click();
    cy.get(obj('firstName')).type(this.firstName);
    cy.get(obj('lastName')).type(this.lastName);
    cy.get(obj('birthDay')).type('1999-12-31');
    cy.get(obj('genderSelect')).select('other');
    cy.get(obj('username')).type(this.randomUserName);
    cy.get(obj('password')).type(this.password);
    cy.get(obj('termAgreement')).click();
    cy.get(obj('userSignup')).click();
    cy.url().should('include', '/profile');
    cy.contains(obj('userName'), this.randomUserName).should('exist');
  }

  public userLoginFunc() {
    cy.get(obj('leftDrawer')).click();
    cy.get(obj('LoginButton')).click();
    cy.get(obj('username')).type(this.randomUserName);
    cy.get(obj('password')).type(this.password);
    cy.get(obj('userLogin')).click();
    cy.url().should('include', '/profile');
    cy.contains(obj('userName'), this.randomUserName).should('exist');
  }

  public userLogoutFunc() {
    this.userLoginFunc();
    cy.get(obj('leftDrawer')).click();
    cy.get(obj('LogOutButton')).click();
    cy.url();
    cy.get(obj('leftDrawer')).click();
    cy.get(obj('ProfileButton')).should('not.exist');
  }
}

const user = new userFunc();

describe('Landing', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('check title', () => {
    cy.title().should('include', 'v2enWeb');
  });

  it('check signup', () => {
    user.userSignupFunc();
  });

  it('check login', () => {
    user.userLoginFunc();
  });

  it('check logout', () => {
    user.userLogoutFunc();
  });
});

export {};
