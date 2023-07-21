export class userFunc {
  public randomUserName;
  public firstName;
  public lastName;
  public password;
  public isSignUp;

  constructor() {
    const { randomUserName, firstName, lastName, password } =
      this.initValueUser();
    this.randomUserName = randomUserName;
    this.firstName = firstName;
    this.lastName = lastName;
    this.password = password;
    this.isSignUp = false;
    console.log('inited');
  }

  public obj(ctx: string) {
    return `[data-cy="${ctx}"]`;
  }

  private initValueUser() {
    const randomUserName = Math.random().toString(36).substring(2, 8);
    const firstName = Math.random().toString(36).substring(2, 8);
    const lastName = Math.random().toString(36).substring(2, 8);
    const password = 'Vanh3006';

    return { randomUserName, firstName, lastName, password };
  }

  public userSignupFunc() {
    if (this.isSignUp) return false;
    cy.get(this.obj('leftDrawer')).click();
    cy.get(this.obj('SignupButton')).click();
    cy.get(this.obj('firstName')).type(this.firstName);
    cy.get(this.obj('lastName')).type(this.lastName);
    cy.get(this.obj('birthDay')).type('2000-01-01');
    cy.get(this.obj('genderSelect')).select('other');
    cy.get(this.obj('username')).type(this.randomUserName);
    cy.get(this.obj('password')).type(this.password);
    cy.get(this.obj('termAgreement')).click();
    cy.get(this.obj('userSignup')).click();
    cy.url().should('include', '/profile');
    cy.contains(this.obj('userName'), this.randomUserName).should('exist');
    this.isSignUp = true;
    return true;
  }

  public userLoginFunc() {
    if (!this.isSignUp) this.userSignupFunc();
    cy.get(this.obj('leftDrawer')).click();
    cy.get(this.obj('LoginButton')).click();
    cy.get(this.obj('username')).type(this.randomUserName);
    cy.get(this.obj('password')).type(this.password);
    cy.get(this.obj('userLogin')).click();
    cy.url().should('include', '/profile');
    cy.contains(this.obj('userName'), this.randomUserName).should('exist');
    return true;
  }

  public userLogoutFunc() {
    this.userLoginFunc();
    cy.get(this.obj('leftDrawer')).click();
    cy.get(this.obj('LogOutButton')).click();
    cy.url();
    cy.get(this.obj('leftDrawer')).click();
    cy.get(this.obj('ProfileButton')).should('not.exist');
  }
}

const user = new userFunc();

describe('User', () => {
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
