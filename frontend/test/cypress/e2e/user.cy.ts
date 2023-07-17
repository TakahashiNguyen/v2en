describe('Landing', () => {
  beforeEach(() => {
    cy.visit('/');
  });
  it('check title', () => {
    cy.title().should('include', 'v2enWeb');
  });
  it('check login', () => {
    cy.get('[data-cy="leftDrawer"]').click();
    cy.get('[data-cy="LoginButton"]').click();
  });
});
export {};
