const obj = (ctx: string) => {
  return `[data-cy="${ctx}"]`;
};

const randomUserName = Math.random().toString(36).substring(2, 8);
const firstName = Math.random().toString(36).substring(2, 8);
const lastName = Math.random().toString(36).substring(2, 8);
const password = 'Vanh3006';

const userSignupFunc = () => {
  cy.get(obj('leftDrawer')).click();
  cy.get(obj('SignupButton')).click();
  cy.get(obj('firstName')).type(firstName);
  cy.get(obj('lastName')).type(lastName);
  cy.get(obj('birthDay')).type('1999-12-31');
  cy.get(obj('genderSelect')).select('other');
  cy.get(obj('username')).type(randomUserName);
  cy.get(obj('password')).type(password);
  cy.get(obj('termAgreement')).click();
  cy.get(obj('userSignup')).click();
  cy.url().should('include', '/profile');
  cy.contains(obj('userName'), randomUserName).should('exist');
};

const userLoginFunc = () => {
  cy.get(obj('leftDrawer')).click();
  cy.get(obj('LoginButton')).click();
  cy.get(obj('username')).type(randomUserName);
  cy.get(obj('password')).type(password);
  cy.get(obj('userLogin')).click();
  cy.url().should('include', '/profile');
  cy.contains(obj('userName'), randomUserName).should('exist');
};

const userLogoutFunc = () => {
  userLoginFunc();
  cy.get(obj('leftDrawer')).click();
  cy.get(obj('LogOutButton')).click();
  cy.url();
  cy.get(obj('leftDrawer')).click();
  cy.get(obj('ProfileButton')).should('not.exist');
};

describe('Landing', () => {
  beforeEach(() => {
    cy.visit('/');
  });
  it('check title', () => {
    cy.title().should('include', 'v2enWeb');
  });
  it('check signup', userSignupFunc);
  it('check login', userLoginFunc);
  it('check logout', userLogoutFunc);
});
export {};
