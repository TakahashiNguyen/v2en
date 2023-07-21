import { userFunc } from './user.cy';

export class dataFunc extends userFunc {
  public origin = '';
  public translated = '';
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
    cy.get(this.obj('originFieldInput')).type(this.origin);
    cy.get(this.obj('translatedFieldInput')).type(this.translated);
    cy.get(this.obj('dataSummit')).click();
    cy.contains(this.obj('originField'), `Origin: ${this.origin}`).should(
      'exist'
    );
    cy.contains(
      this.obj('translatedField'),
      `Translated: ${this.translated}`
    ).should('exist');
  }

  public deleteData(allowAddData = true) {
    if (allowAddData) this.addData();

    cy.get(this.obj('leftDrawer')).click();
    cy.get(this.obj('DatasButton')).click();
    cy.get(this.obj(this.origin + this.translated + 'Button'))
      .should('exist')
      .click();

    cy.get(this.obj('deleteButton')).click();
    cy.get(this.obj('leftDrawer')).click();
    cy.get(this.obj('DatasButton')).click();

    cy.get(this.obj(this.origin + this.translated + 'Button')).should(
      'not.exist'
    );
  }

  public modifyData() {
    this.addData();

    cy.get(this.obj('leftDrawer')).click();
    cy.get(this.obj('DatasButton')).click();
    cy.get(this.obj(this.origin + this.translated + 'Button'))
      .should('exist')
      .click();

    cy.get(this.obj('modifyButton')).click();
    const oldorigin = this.origin;
    const oldtranslated = this.translated;
    this.initValueData();
    cy.get(this.obj('originFieldInput')).type(this.origin);
    cy.get(this.obj('translatedFieldInput')).type(this.translated);
    cy.get(this.obj('dataSummit')).click();
    cy.contains(
      this.obj('originField'),
      `Origin: ${oldorigin + this.origin}`
    ).should('exist');
    cy.contains(
      this.obj('translatedField'),
      `Translated: ${oldtranslated + this.translated}`
    ).should('exist');

    this.origin = oldorigin + this.origin;
    this.translated = oldtranslated + this.translated;

    this.deleteData(false);
  }

  public cleanup() {
    this.initDataAddFunc();
    cy.get(this.obj('leftDrawer')).click();
    cy.get(this.obj('DatasButton')).click();
    cy.get(this.obj('addDataButton'))
      .should('be.visible')
      .next()
      .find("[role='listitem']")
      .last()
      .click();
    cy.get(this.obj('deleteButton')).click();
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

  it('clean up', () => {
    data.cleanup();
  });
});
