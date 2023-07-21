import { userFunc } from './user.cy';

export class todoFunc extends userFunc {
  private job = Math.random().toString(36).substring(2, 24);
  constructor() {
    super();
  }

  private initTodo() {
    if (!this.userSignupFunc()) this.userLoginFunc();
  }

  public addJob() {
    this.initTodo();

    cy.get(this.obj('leftDrawer')).click();
    cy.get(this.obj('TodosButton')).click();
    cy.get(this.obj('todoTextField')).type(this.job);
    cy.get(this.obj('todoSubmitButton')).click();
    cy.get(this.obj(this.job + 'Field')).should('exist');
  }

  public removeJob() {
    this.initTodo();

    cy.get(this.obj('leftDrawer')).click();
    cy.get(this.obj('TodosButton')).click();
    cy.get(this.obj(this.job + 'DeleteButton')).click();
    cy.get(this.obj(this.job + 'Field')).should('not.exist');
  }
}

const todo = new todoFunc();

describe('Todo', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('add job', () => {
    todo.addJob();
  });

  it('delete job', () => {
    todo.removeJob();
  });
});
