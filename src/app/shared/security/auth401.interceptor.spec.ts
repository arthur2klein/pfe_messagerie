import { TestBed } from '@angular/core/testing';

import { Auth401Interceptor } from './auth401.interceptor';

describe('Auth401Interceptor', () => {
  beforeEach(() => TestBed.configureTestingModule({
    providers: [
      Auth401Interceptor
      ]
  }));

  it('should be created', () => {
    const interceptor: Auth401Interceptor = TestBed.inject(Auth401Interceptor);
    expect(interceptor).toBeTruthy();
  });
});