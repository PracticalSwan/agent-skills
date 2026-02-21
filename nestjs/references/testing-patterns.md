# NestJS Testing Patterns

## Setup & Configuration

### Test Module Builder

Every NestJS test starts with `Test.createTestingModule` to build an isolated module:

```typescript
import { Test, TestingModule } from '@nestjs/testing';

describe('UsersService', () => {
  let service: UsersService;
  let module: TestingModule;

  beforeEach(async () => {
    module = await Test.createTestingModule({
      providers: [UsersService],
    }).compile();

    service = module.get<UsersService>(UsersService);
  });

  afterEach(async () => {
    await module.close();
  });
});
```

---

## Unit Testing Services

### Basic Service Test

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { UsersService } from './users.service';

describe('UsersService', () => {
  let service: UsersService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [UsersService],
    }).compile();

    service = module.get<UsersService>(UsersService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
```

### Mocking TypeORM Repositories

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { ProductsService } from './products.service';
import { Product } from './product.entity';

const mockProductRepository = () => ({
  find: jest.fn(),
  findOne: jest.fn(),
  findOneBy: jest.fn(),
  create: jest.fn(),
  save: jest.fn(),
  update: jest.fn(),
  delete: jest.fn(),
  createQueryBuilder: jest.fn(),
});

type MockRepository<T = any> = Partial<Record<keyof Repository<T>, jest.Mock>>;

describe('ProductsService', () => {
  let service: ProductsService;
  let repository: MockRepository<Product>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ProductsService,
        {
          provide: getRepositoryToken(Product),
          useFactory: mockProductRepository,
        },
      ],
    }).compile();

    service = module.get<ProductsService>(ProductsService);
    repository = module.get<MockRepository<Product>>(getRepositoryToken(Product));
  });

  describe('findAll', () => {
    it('should return an array of products', async () => {
      const products = [
        { id: 1, name: 'Widget', price: 9.99 },
        { id: 2, name: 'Gadget', price: 19.99 },
      ];
      repository.find.mockResolvedValue(products);

      const result = await service.findAll();

      expect(repository.find).toHaveBeenCalled();
      expect(result).toEqual(products);
    });
  });

  describe('findOne', () => {
    it('should return a single product', async () => {
      const product = { id: 1, name: 'Widget', price: 9.99 };
      repository.findOneBy.mockResolvedValue(product);

      const result = await service.findOne(1);

      expect(repository.findOneBy).toHaveBeenCalledWith({ id: 1 });
      expect(result).toEqual(product);
    });

    it('should throw NotFoundException when product not found', async () => {
      repository.findOneBy.mockResolvedValue(null);

      await expect(service.findOne(999)).rejects.toThrow(NotFoundException);
    });
  });

  describe('create', () => {
    it('should create and return a product', async () => {
      const dto = { name: 'Widget', price: 9.99 };
      const product = { id: 1, ...dto };

      repository.create.mockReturnValue(product);
      repository.save.mockResolvedValue(product);

      const result = await service.create(dto);

      expect(repository.create).toHaveBeenCalledWith(dto);
      expect(repository.save).toHaveBeenCalledWith(product);
      expect(result).toEqual(product);
    });
  });

  describe('remove', () => {
    it('should delete a product', async () => {
      repository.delete.mockResolvedValue({ affected: 1, raw: [] });

      await service.remove(1);

      expect(repository.delete).toHaveBeenCalledWith(1);
    });

    it('should throw NotFoundException when deleting non-existent product', async () => {
      repository.delete.mockResolvedValue({ affected: 0, raw: [] });

      await expect(service.remove(999)).rejects.toThrow(NotFoundException);
    });
  });
});
```

### Mocking External Services

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { HttpService } from '@nestjs/axios';
import { of, throwError } from 'rxjs';
import { PaymentsService } from './payments.service';

describe('PaymentsService', () => {
  let service: PaymentsService;
  let httpService: HttpService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        PaymentsService,
        {
          provide: HttpService,
          useValue: {
            post: jest.fn(),
            get: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<PaymentsService>(PaymentsService);
    httpService = module.get<HttpService>(HttpService);
  });

  describe('processPayment', () => {
    it('should process a payment successfully', async () => {
      const paymentData = { amount: 100, currency: 'USD' };
      const apiResponse = { data: { id: 'txn_123', status: 'completed' } };

      jest.spyOn(httpService, 'post').mockReturnValue(
        of({ data: apiResponse.data, status: 200, statusText: 'OK', headers: {}, config: {} as any }),
      );

      const result = await service.processPayment(paymentData);

      expect(result.status).toBe('completed');
    });

    it('should throw on payment failure', async () => {
      jest.spyOn(httpService, 'post').mockReturnValue(
        throwError(() => new Error('Payment gateway error')),
      );

      await expect(
        service.processPayment({ amount: 100, currency: 'USD' }),
      ).rejects.toThrow('Payment gateway error');
    });
  });
});
```

### Mocking ConfigService

```typescript
const mockConfigService = {
  get: jest.fn((key: string) => {
    const config: Record<string, any> = {
      DATABASE_HOST: 'localhost',
      DATABASE_PORT: 5432,
      JWT_SECRET: 'test-secret',
      JWT_EXPIRES_IN: '1h',
    };
    return config[key];
  }),
};

const module: TestingModule = await Test.createTestingModule({
  providers: [
    AppService,
    { provide: ConfigService, useValue: mockConfigService },
  ],
}).compile();
```

---

## Unit Testing Controllers

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { ProductsController } from './products.controller';
import { ProductsService } from './products.service';

describe('ProductsController', () => {
  let controller: ProductsController;
  let service: ProductsService;

  const mockProductsService = {
    findAll: jest.fn(),
    findOne: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    remove: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ProductsController],
      providers: [
        { provide: ProductsService, useValue: mockProductsService },
      ],
    }).compile();

    controller = module.get<ProductsController>(ProductsController);
    service = module.get<ProductsService>(ProductsService);
  });

  afterEach(() => jest.clearAllMocks());

  describe('findAll', () => {
    it('should return paginated products', async () => {
      const products = [{ id: 1, name: 'Widget' }];
      mockProductsService.findAll.mockResolvedValue(products);

      const result = await controller.findAll({ page: 1, limit: 10 });

      expect(service.findAll).toHaveBeenCalledWith({ page: 1, limit: 10 });
      expect(result).toEqual(products);
    });
  });

  describe('findOne', () => {
    it('should return a product by id', async () => {
      const product = { id: 1, name: 'Widget', price: 9.99 };
      mockProductsService.findOne.mockResolvedValue(product);

      const result = await controller.findOne(1);

      expect(service.findOne).toHaveBeenCalledWith(1);
      expect(result).toEqual(product);
    });
  });

  describe('create', () => {
    it('should create a product', async () => {
      const dto = { name: 'Widget', price: 9.99 };
      const created = { id: 1, ...dto };
      mockProductsService.create.mockResolvedValue(created);

      const result = await controller.create(dto);

      expect(service.create).toHaveBeenCalledWith(dto);
      expect(result).toEqual(created);
    });
  });

  describe('remove', () => {
    it('should delete a product', async () => {
      mockProductsService.remove.mockResolvedValue(undefined);

      await controller.remove(1);

      expect(service.remove).toHaveBeenCalledWith(1);
    });
  });
});
```

---

## Testing Guards

```typescript
import { ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { RolesGuard } from './roles.guard';

describe('RolesGuard', () => {
  let guard: RolesGuard;
  let reflector: Reflector;

  beforeEach(() => {
    reflector = new Reflector();
    guard = new RolesGuard(reflector);
  });

  const mockExecutionContext = (user: any, roles?: string[]): ExecutionContext => {
    const context = {
      getHandler: jest.fn(),
      getClass: jest.fn(),
      switchToHttp: jest.fn().mockReturnValue({
        getRequest: jest.fn().mockReturnValue({ user }),
      }),
    } as unknown as ExecutionContext;

    jest.spyOn(reflector, 'getAllAndOverride').mockReturnValue(roles);
    return context;
  };

  it('should allow access when no roles are required', () => {
    const context = mockExecutionContext({ roles: ['user'] }, undefined);
    expect(guard.canActivate(context)).toBe(true);
  });

  it('should allow access when user has required role', () => {
    const context = mockExecutionContext({ roles: ['admin'] }, ['admin']);
    expect(guard.canActivate(context)).toBe(true);
  });

  it('should deny access when user lacks required role', () => {
    const context = mockExecutionContext({ roles: ['user'] }, ['admin']);
    expect(guard.canActivate(context)).toBe(false);
  });

  it('should deny access when user has no roles', () => {
    const context = mockExecutionContext({}, ['admin']);
    expect(guard.canActivate(context)).toBe(false);
  });
});
```

---

## Testing Interceptors

```typescript
import { CallHandler, ExecutionContext } from '@nestjs/common';
import { of } from 'rxjs';
import { TransformInterceptor } from './transform.interceptor';

describe('TransformInterceptor', () => {
  let interceptor: TransformInterceptor<any>;

  beforeEach(() => {
    interceptor = new TransformInterceptor();
  });

  it('should wrap response in data envelope', (done) => {
    const mockContext = {} as ExecutionContext;
    const mockHandler: CallHandler = {
      handle: () => of({ id: 1, name: 'Test' }),
    };

    interceptor.intercept(mockContext, mockHandler).subscribe({
      next: (value) => {
        expect(value).toEqual({
          data: { id: 1, name: 'Test' },
          statusCode: 200,
          timestamp: expect.any(String),
        });
      },
      complete: () => done(),
    });
  });
});
```

### Testing a Logging Interceptor

```typescript
import { CallHandler, ExecutionContext } from '@nestjs/common';
import { of } from 'rxjs';
import { LoggingInterceptor } from './logging.interceptor';

describe('LoggingInterceptor', () => {
  let interceptor: LoggingInterceptor;

  beforeEach(() => {
    interceptor = new LoggingInterceptor();
  });

  it('should log method, url, and execution time', (done) => {
    const logSpy = jest.spyOn(console, 'log').mockImplementation();
    const mockRequest = { method: 'GET', url: '/products' };

    const mockContext = {
      switchToHttp: () => ({
        getRequest: () => mockRequest,
      }),
    } as unknown as ExecutionContext;

    const mockHandler: CallHandler = {
      handle: () => of('response'),
    };

    interceptor.intercept(mockContext, mockHandler).subscribe({
      complete: () => {
        expect(logSpy).toHaveBeenCalledWith(
          expect.stringContaining('GET /products'),
        );
        logSpy.mockRestore();
        done();
      },
    });
  });
});
```

---

## Testing Pipes

```typescript
import { ArgumentMetadata, BadRequestException } from '@nestjs/common';
import { ParsePositiveIntPipe } from './parse-positive-int.pipe';

describe('ParsePositiveIntPipe', () => {
  let pipe: ParsePositiveIntPipe;

  beforeEach(() => {
    pipe = new ParsePositiveIntPipe();
  });

  const metadata: ArgumentMetadata = { type: 'param', metatype: Number, data: 'id' };

  it('should transform a valid positive integer string', () => {
    expect(pipe.transform('42', metadata)).toBe(42);
  });

  it('should throw on negative number', () => {
    expect(() => pipe.transform('-1', metadata)).toThrow(BadRequestException);
  });

  it('should throw on non-numeric string', () => {
    expect(() => pipe.transform('abc', metadata)).toThrow(BadRequestException);
  });

  it('should throw on zero', () => {
    expect(() => pipe.transform('0', metadata)).toThrow(BadRequestException);
  });
});
```

---

## Testing Exception Filters

```typescript
import { ArgumentsHost, HttpException, HttpStatus } from '@nestjs/common';
import { HttpExceptionFilter } from './http-exception.filter';

describe('HttpExceptionFilter', () => {
  let filter: HttpExceptionFilter;

  beforeEach(() => {
    filter = new HttpExceptionFilter();
  });

  it('should format error response correctly', () => {
    const mockJson = jest.fn();
    const mockStatus = jest.fn().mockReturnValue({ json: mockJson });

    const mockHost = {
      switchToHttp: () => ({
        getResponse: () => ({ status: mockStatus }),
        getRequest: () => ({ url: '/test', method: 'GET' }),
      }),
    } as unknown as ArgumentsHost;

    const exception = new HttpException('Not Found', HttpStatus.NOT_FOUND);

    filter.catch(exception, mockHost);

    expect(mockStatus).toHaveBeenCalledWith(404);
    expect(mockJson).toHaveBeenCalledWith(
      expect.objectContaining({
        statusCode: 404,
        message: 'Not Found',
        path: '/test',
        timestamp: expect.any(String),
      }),
    );
  });
});
```

---

## Integration Testing with Supertest (E2E)

### Basic E2E Setup

```typescript
// test/app.e2e-spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../src/app.module';

describe('AppController (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it('/ (GET)', () => {
    return request(app.getHttpServer())
      .get('/')
      .expect(200)
      .expect({ message: 'Hello World!' });
  });
});
```

### CRUD E2E Test

```typescript
// test/products.e2e-spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../src/app.module';
import { getRepositoryToken } from '@nestjs/typeorm';
import { Product } from '../src/products/product.entity';

describe('Products (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  let createdId: number;

  describe('POST /products', () => {
    it('should create a product', () => {
      return request(app.getHttpServer())
        .post('/products')
        .send({ name: 'Widget', price: 9.99, description: 'A widget' })
        .expect(201)
        .then((res) => {
          expect(res.body).toHaveProperty('id');
          expect(res.body.name).toBe('Widget');
          createdId = res.body.id;
        });
    });

    it('should reject invalid data', () => {
      return request(app.getHttpServer())
        .post('/products')
        .send({ name: '', price: -1 })
        .expect(400);
    });
  });

  describe('GET /products', () => {
    it('should return a list of products', () => {
      return request(app.getHttpServer())
        .get('/products')
        .expect(200)
        .then((res) => {
          expect(Array.isArray(res.body)).toBe(true);
        });
    });
  });

  describe('GET /products/:id', () => {
    it('should return a product', () => {
      return request(app.getHttpServer())
        .get(`/products/${createdId}`)
        .expect(200)
        .then((res) => {
          expect(res.body.id).toBe(createdId);
        });
    });

    it('should 404 for non-existent product', () => {
      return request(app.getHttpServer())
        .get('/products/99999')
        .expect(404);
    });
  });

  describe('PUT /products/:id', () => {
    it('should update a product', () => {
      return request(app.getHttpServer())
        .put(`/products/${createdId}`)
        .send({ name: 'Updated Widget', price: 12.99, description: 'Updated' })
        .expect(200)
        .then((res) => {
          expect(res.body.name).toBe('Updated Widget');
        });
    });
  });

  describe('DELETE /products/:id', () => {
    it('should delete a product', () => {
      return request(app.getHttpServer())
        .delete(`/products/${createdId}`)
        .expect(200);
    });
  });
});
```

### E2E with Authentication

```typescript
describe('Protected Routes (e2e)', () => {
  let app: INestApplication;
  let authToken: string;

  beforeAll(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
    await app.init();

    // Login to get token
    const loginRes = await request(app.getHttpServer())
      .post('/auth/login')
      .send({ email: 'admin@test.com', password: 'password123' });

    authToken = loginRes.body.access_token;
  });

  afterAll(async () => {
    await app.close();
  });

  it('should access protected route with token', () => {
    return request(app.getHttpServer())
      .get('/products')
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200);
  });

  it('should reject unauthenticated request', () => {
    return request(app.getHttpServer())
      .get('/products')
      .expect(401);
  });

  it('should reject expired/invalid token', () => {
    return request(app.getHttpServer())
      .get('/products')
      .set('Authorization', 'Bearer invalid-token')
      .expect(401);
  });
});
```

---

## Test Utilities

### Custom Test Helper

```typescript
// test/helpers.ts
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe, Type } from '@nestjs/common';

export async function createTestApp(
  modules: Type<any>[],
): Promise<INestApplication> {
  const moduleFixture: TestingModule = await Test.createTestingModule({
    imports: modules,
  }).compile();

  const app = moduleFixture.createNestApplication();
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  await app.init();
  return app;
}

export function createMockRepository<T>(): Record<string, jest.Mock> {
  return {
    find: jest.fn(),
    findOne: jest.fn(),
    findOneBy: jest.fn(),
    findAndCount: jest.fn(),
    create: jest.fn(),
    save: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
    remove: jest.fn(),
    count: jest.fn(),
    createQueryBuilder: jest.fn(() => ({
      where: jest.fn().mockReturnThis(),
      andWhere: jest.fn().mockReturnThis(),
      orWhere: jest.fn().mockReturnThis(),
      orderBy: jest.fn().mockReturnThis(),
      skip: jest.fn().mockReturnThis(),
      take: jest.fn().mockReturnThis(),
      leftJoinAndSelect: jest.fn().mockReturnThis(),
      getMany: jest.fn(),
      getOne: jest.fn(),
      getManyAndCount: jest.fn(),
    })),
  };
}
```

### Using the Helper

```typescript
import { createMockRepository } from '../../test/helpers';
import { getRepositoryToken } from '@nestjs/typeorm';
import { Product } from './product.entity';

describe('ProductsService', () => {
  let service: ProductsService;
  const mockRepo = createMockRepository<Product>();

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        ProductsService,
        { provide: getRepositoryToken(Product), useValue: mockRepo },
      ],
    }).compile();

    service = module.get(ProductsService);
  });
});
```

### Factory Functions for Test Data

```typescript
// test/factories.ts
import { Product } from '../src/products/product.entity';
import { CreateProductDto } from '../src/products/dto/create-product.dto';

let idCounter = 0;

export function buildProduct(overrides: Partial<Product> = {}): Product {
  idCounter++;
  return {
    id: idCounter,
    name: `Product ${idCounter}`,
    description: `Description for product ${idCounter}`,
    price: 9.99 + idCounter,
    isActive: true,
    createdAt: new Date(),
    updatedAt: new Date(),
    ...overrides,
  } as Product;
}

export function buildCreateProductDto(
  overrides: Partial<CreateProductDto> = {},
): CreateProductDto {
  return {
    name: 'Test Product',
    description: 'A test product',
    price: 19.99,
    ...overrides,
  };
}

export function buildProducts(count: number): Product[] {
  return Array.from({ length: count }, () => buildProduct());
}
```

---

## Jest Configuration for NestJS

```json
// package.json (jest section)
{
  "jest": {
    "moduleFileExtensions": ["js", "json", "ts"],
    "rootDir": "src",
    "testRegex": ".*\\.spec\\.ts$",
    "transform": {
      "^.+\\.(t|j)s$": "ts-jest"
    },
    "collectCoverageFrom": [
      "**/*.(t|j)s",
      "!**/*.module.ts",
      "!**/main.ts",
      "!**/*.dto.ts",
      "!**/*.entity.ts"
    ],
    "coverageDirectory": "../coverage",
    "testEnvironment": "node",
    "moduleNameMapper": {
      "^@app/(.*)$": "<rootDir>/$1",
      "^@common/(.*)$": "<rootDir>/common/$1"
    }
  }
}
```

### E2E Jest Config

```json
// test/jest-e2e.json
{
  "moduleFileExtensions": ["js", "json", "ts"],
  "rootDir": ".",
  "testEnvironment": "node",
  "testRegex": ".e2e-spec.ts$",
  "transform": {
    "^.+\\.(t|j)s$": "ts-jest"
  },
  "moduleNameMapper": {
    "^@app/(.*)$": "<rootDir>/../src/$1"
  }
}
```
