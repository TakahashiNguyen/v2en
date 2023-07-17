import { userFunc } from './user.cy';

export class dataFunc extends userFunc {
  public origin;
  public translated;
  constructor() {
    super();
  }

  public initDataAddFunc() {
    if (!this.userSignupFunc()) this.userLoginFunc();
  }

  private initValueData() {
    this.origin = Math.random().toString(36).substring(2, 24);
    this.translated = Math.random().toString(36).substring(2, 27);
  }

  public addData() {
    this.initDataAddFunc();
    this.initValueData();
    cy.get(this.obj('leftDrawer')).click();
    cy.get(this.obj('DatasButton')).click();
    cy.get(this.obj('addDataButton')).click();
    cy.get(this.obj('originField')).type(this.origin);
    cy.get(this.obj('translatedField')).type(this.translated);
    cy.get(this.obj('dataSummit')).click();
    cy.url();
    cy.contains(this.obj('originField'), `Origin: ${this.origin}`).should(
      'exist'
    );
    cy.contains(
      this.obj('translatedField'),
      `Translated: ${this.translated}`
    ).should('exist');
  }

  public deleteData() {
    this.addData();
    cy.get(this.obj('deleteButton')).click();
  }

  public modifyData() {
    this.addData();
    cy.get(this.obj('modifyButton')).click();
    const oldorigin = this.origin;
    const oldtranslated = this.translated;
    this.initValueData();
    cy.get(this.obj('originField')).type(this.origin);
    cy.get(this.obj('translatedField')).type(this.translated);
    cy.get(this.obj('dataSummit')).click();
    cy.url();
    cy.contains(
      this.obj('originField'),
      `Origin: ${oldorigin + this.origin}`
    ).should('exist');
    cy.contains(
      this.obj('translatedField'),
      `Translated: ${oldtranslated + this.translated}`
    ).should('exist');
  }
}

const data = new dataFunc();

describe('Data', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('add Data', () => {
    data.addData();
  });

  it('delete Data', () => {
    data.deleteData();
  });

  it('modify Data', () => {
    data.modifyData();
  });
});
