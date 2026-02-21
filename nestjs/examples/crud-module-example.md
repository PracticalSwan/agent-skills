# Complete NestJS CRUD Module: Products

A full-featured Products module demonstrating NestJS patterns including TypeORM entity, DTOs with class-validator, pagination, custom exception filter, auth guard, and unit tests.

## Directory Structure

```
src/products/
  product.entity.ts
  products.module.ts
  products.controller.ts
  products.service.ts
  dto/
    create-product.dto.ts
    update-product.dto.ts
    product-query.dto.ts
  filters/
    product-exception.filter.ts
  guards/
    product-owner.guard.ts
  interceptors/
    pagination.interceptor.ts
  products.controller.spec.ts
  products.service.spec.ts
```

---

## Entity

```typescript
// product.entity.ts
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  JoinColumn,
} from 'typeorm';

export enum ProductStatus {
  DRAFT = 'draft',
  ACTIVE = 'active',
  ARCHIVED = 'archived',
}

@Entity('products')
export class Product {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ length: 200 })
  name: string;

  @Column({ type: 'text', nullable: true })
  description: string;

  @Column({ type: 'decimal', precision: 10, scale: 2 })
  price: number;

  @Column({ type: 'enum', enum: ProductStatus, default: ProductStatus.DRAFT })
  status: ProductStatus;

  @Column({ default: 0 })
  stock: number;

  @Column({ nullable: true })
  imageUrl: string;

  @Column()
  ownerId: number;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

---

## DTOs

### Create DTO

```typescript
// dto/create-product.dto.ts
import {
  IsString,
  IsNotEmpty,
  IsNumber,
  IsOptional,
  IsEnum,
  IsUrl,
  Min,
  MaxLength,
} from 'class-validator';
import { ProductStatus } from '../product.entity';

export class CreateProductDto {
  @IsString()
  @IsNotEmpty()
  @MaxLength(200)
  name: string;

  @IsString()
  @IsOptional()
  description?: string;

  @IsNumber({ maxDecimalPlaces: 2 })
  @Min(0)
  price: number;

  @IsEnum(ProductStatus)
  @IsOptional()
  status?: ProductStatus;

  @IsNumber()
  @Min(0)
  @IsOptional()
  stock?: number;

  @IsUrl()
  @IsOptional()
  imageUrl?: string;
}
```

### Update DTO

```typescript
// dto/update-product.dto.ts
import { PartialType } from '@nestjs/mapped-types';
import { CreateProductDto } from './create-product.dto';

export class UpdateProductDto extends PartialType(CreateProductDto) {}
```

### Query DTO (for pagination + filtering)

```typescript
// dto/product-query.dto.ts
import { IsOptional, IsInt, Min, Max, IsEnum, IsString } from 'class-validator';
import { Type } from 'class-transformer';
import { ProductStatus } from '../product.entity';

export class ProductQueryDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page?: number = 1;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number = 10;

  @IsOptional()
  @IsString()
  search?: string;

  @IsOptional()
  @IsEnum(ProductStatus)
  status?: ProductStatus;

  @IsOptional()
  @IsString()
  sortBy?: string = 'createdAt';

  @IsOptional()
  @IsEnum(['ASC', 'DESC'])
  sortOrder?: 'ASC' | 'DESC' = 'DESC';
}
```

---

## Service

```typescript
// products.service.ts
import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Product } from './product.entity';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
import { ProductQueryDto } from './dto/product-query.dto';

export interface PaginatedResult<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

@Injectable()
export class ProductsService {
  constructor(
    @InjectRepository(Product)
    private readonly productRepository: Repository<Product>,
  ) {}

  async findAll(query: ProductQueryDto): Promise<PaginatedResult<Product>> {
    const { page, limit, search, status, sortBy, sortOrder } = query;

    const qb = this.productRepository.createQueryBuilder('product');

    if (search) {
      qb.andWhere(
        '(product.name ILIKE :search OR product.description ILIKE :search)',
        { search: `%${search}%` },
      );
    }

    if (status) {
      qb.andWhere('product.status = :status', { status });
    }

    qb.orderBy(`product.${sortBy}`, sortOrder);
    qb.skip((page - 1) * limit).take(limit);

    const [data, total] = await qb.getManyAndCount();

    return {
      data,
      total,
      page,
      limit,
      totalPages: Math.ceil(total / limit),
    };
  }

  async findOne(id: number): Promise<Product> {
    const product = await this.productRepository.findOneBy({ id });
    if (!product) {
      throw new NotFoundException(`Product with id ${id} not found`);
    }
    return product;
  }

  async create(dto: CreateProductDto, ownerId: number): Promise<Product> {
    const product = this.productRepository.create({ ...dto, ownerId });
    return this.productRepository.save(product);
  }

  async update(id: number, dto: UpdateProductDto): Promise<Product> {
    const product = await this.findOne(id);
    Object.assign(product, dto);
    return this.productRepository.save(product);
  }

  async remove(id: number): Promise<void> {
    const result = await this.productRepository.delete(id);
    if (result.affected === 0) {
      throw new NotFoundException(`Product with id ${id} not found`);
    }
  }
}
```

---

## Controller

```typescript
// products.controller.ts
import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Body,
  Param,
  Query,
  ParseIntPipe,
  HttpCode,
  HttpStatus,
  UseGuards,
  UseFilters,
  UseInterceptors,
} from '@nestjs/common';
import { ProductsService } from './products.service';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
import { ProductQueryDto } from './dto/product-query.dto';
import { ProductExceptionFilter } from './filters/product-exception.filter';
import { ProductOwnerGuard } from './guards/product-owner.guard';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { CurrentUser } from '../auth/decorators/current-user.decorator';

@Controller('products')
@UseFilters(ProductExceptionFilter)
export class ProductsController {
  constructor(private readonly productsService: ProductsService) {}

  @Get()
  findAll(@Query() query: ProductQueryDto) {
    return this.productsService.findAll(query);
  }

  @Get(':id')
  findOne(@Param('id', ParseIntPipe) id: number) {
    return this.productsService.findOne(id);
  }

  @Post()
  @UseGuards(JwtAuthGuard)
  @HttpCode(HttpStatus.CREATED)
  create(
    @Body() dto: CreateProductDto,
    @CurrentUser('id') userId: number,
  ) {
    return this.productsService.create(dto, userId);
  }

  @Put(':id')
  @UseGuards(JwtAuthGuard, ProductOwnerGuard)
  update(
    @Param('id', ParseIntPipe) id: number,
    @Body() dto: UpdateProductDto,
  ) {
    return this.productsService.update(id, dto);
  }

  @Delete(':id')
  @UseGuards(JwtAuthGuard, ProductOwnerGuard)
  @HttpCode(HttpStatus.NO_CONTENT)
  remove(@Param('id', ParseIntPipe) id: number) {
    return this.productsService.remove(id);
  }
}
```

---

## Exception Filter

```typescript
// filters/product-exception.filter.ts
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
  Logger,
} from '@nestjs/common';
import { Request, Response } from 'express';

@Catch()
export class ProductExceptionFilter implements ExceptionFilter {
  private readonly logger = new Logger(ProductExceptionFilter.name);

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    const message =
      exception instanceof HttpException
        ? exception.getResponse()
        : 'Internal server error';

    const errorResponse = {
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      method: request.method,
      message:
        typeof message === 'string'
          ? message
          : (message as any).message || message,
    };

    if (status >= 500) {
      this.logger.error(
        `${request.method} ${request.url} ${status}`,
        exception instanceof Error ? exception.stack : undefined,
      );
    }

    response.status(status).json(errorResponse);
  }
}
```

---

## Auth Guard

```typescript
// guards/product-owner.guard.ts
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  ForbiddenException,
} from '@nestjs/common';
import { ProductsService } from '../products.service';

@Injectable()
export class ProductOwnerGuard implements CanActivate {
  constructor(private readonly productsService: ProductsService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const userId = request.user?.id;
    const productId = parseInt(request.params.id, 10);

    if (!userId || isNaN(productId)) {
      throw new ForbiddenException('Access denied');
    }

    const product = await this.productsService.findOne(productId);

    if (product.ownerId !== userId) {
      throw new ForbiddenException('You can only modify your own products');
    }

    return true;
  }
}
```

---

## Pagination Interceptor

```typescript
// interceptors/pagination.interceptor.ts
import {
  Injectable,
  NestInterceptor,
  ExecutionContext,
  CallHandler,
} from '@nestjs/common';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    limit: number;
    totalPages: number;
    hasNextPage: boolean;
    hasPreviousPage: boolean;
  };
}

@Injectable()
export class PaginationInterceptor<T> implements NestInterceptor {
  intercept(
    context: ExecutionContext,
    next: CallHandler,
  ): Observable<PaginatedResponse<T>> {
    return next.handle().pipe(
      map((result) => {
        if (result?.data && result?.total !== undefined) {
          return {
            data: result.data,
            meta: {
              total: result.total,
              page: result.page,
              limit: result.limit,
              totalPages: result.totalPages,
              hasNextPage: result.page < result.totalPages,
              hasPreviousPage: result.page > 1,
            },
          };
        }
        return result;
      }),
    );
  }
}
```

---

## Module

```typescript
// products.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ProductsController } from './products.controller';
import { ProductsService } from './products.service';
import { Product } from './product.entity';

@Module({
  imports: [TypeOrmModule.forFeature([Product])],
  controllers: [ProductsController],
  providers: [ProductsService],
  exports: [ProductsService],
})
export class ProductsModule {}
```

---

## Unit Tests

### Service Tests

```typescript
// products.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { NotFoundException } from '@nestjs/common';
import { ProductsService } from './products.service';
import { Product, ProductStatus } from './product.entity';

describe('ProductsService', () => {
  let service: ProductsService;

  const mockQueryBuilder = {
    andWhere: jest.fn().mockReturnThis(),
    orderBy: jest.fn().mockReturnThis(),
    skip: jest.fn().mockReturnThis(),
    take: jest.fn().mockReturnThis(),
    getManyAndCount: jest.fn(),
  };

  const mockRepository = {
    find: jest.fn(),
    findOneBy: jest.fn(),
    create: jest.fn(),
    save: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
    createQueryBuilder: jest.fn().mockReturnValue(mockQueryBuilder),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ProductsService,
        { provide: getRepositoryToken(Product), useValue: mockRepository },
      ],
    }).compile();

    service = module.get<ProductsService>(ProductsService);
  });

  afterEach(() => jest.clearAllMocks());

  describe('findAll', () => {
    it('should return paginated products', async () => {
      const products = [
        { id: 1, name: 'Widget', price: 9.99 },
        { id: 2, name: 'Gadget', price: 19.99 },
      ];
      mockQueryBuilder.getManyAndCount.mockResolvedValue([products, 2]);

      const result = await service.findAll({
        page: 1,
        limit: 10,
        sortBy: 'createdAt',
        sortOrder: 'DESC',
      });

      expect(result.data).toEqual(products);
      expect(result.total).toBe(2);
      expect(result.totalPages).toBe(1);
    });

    it('should filter by search term', async () => {
      mockQueryBuilder.getManyAndCount.mockResolvedValue([[], 0]);

      await service.findAll({
        page: 1,
        limit: 10,
        search: 'widget',
        sortBy: 'createdAt',
        sortOrder: 'DESC',
      });

      expect(mockQueryBuilder.andWhere).toHaveBeenCalledWith(
        '(product.name ILIKE :search OR product.description ILIKE :search)',
        { search: '%widget%' },
      );
    });

    it('should filter by status', async () => {
      mockQueryBuilder.getManyAndCount.mockResolvedValue([[], 0]);

      await service.findAll({
        page: 1,
        limit: 10,
        status: ProductStatus.ACTIVE,
        sortBy: 'createdAt',
        sortOrder: 'DESC',
      });

      expect(mockQueryBuilder.andWhere).toHaveBeenCalledWith(
        'product.status = :status',
        { status: ProductStatus.ACTIVE },
      );
    });
  });

  describe('findOne', () => {
    it('should return a product', async () => {
      const product = { id: 1, name: 'Widget', price: 9.99 };
      mockRepository.findOneBy.mockResolvedValue(product);

      expect(await service.findOne(1)).toEqual(product);
      expect(mockRepository.findOneBy).toHaveBeenCalledWith({ id: 1 });
    });

    it('should throw NotFoundException', async () => {
      mockRepository.findOneBy.mockResolvedValue(null);

      await expect(service.findOne(999)).rejects.toThrow(NotFoundException);
    });
  });

  describe('create', () => {
    it('should create and save a product', async () => {
      const dto = { name: 'Widget', price: 9.99 };
      const product = { id: 1, ...dto, ownerId: 1 };

      mockRepository.create.mockReturnValue(product);
      mockRepository.save.mockResolvedValue(product);

      const result = await service.create(dto as any, 1);

      expect(mockRepository.create).toHaveBeenCalledWith({ ...dto, ownerId: 1 });
      expect(mockRepository.save).toHaveBeenCalledWith(product);
      expect(result).toEqual(product);
    });
  });

  describe('update', () => {
    it('should update an existing product', async () => {
      const existing = { id: 1, name: 'Widget', price: 9.99, ownerId: 1 };
      const dto = { name: 'Updated Widget' };
      const updated = { ...existing, ...dto };

      mockRepository.findOneBy
        .mockResolvedValueOnce(existing)
        .mockResolvedValueOnce(updated);
      mockRepository.save.mockResolvedValue(updated);

      const result = await service.update(1, dto as any);

      expect(result.name).toBe('Updated Widget');
    });

    it('should throw NotFoundException for missing product', async () => {
      mockRepository.findOneBy.mockResolvedValue(null);

      await expect(service.update(999, {} as any)).rejects.toThrow(
        NotFoundException,
      );
    });
  });

  describe('remove', () => {
    it('should delete a product', async () => {
      mockRepository.delete.mockResolvedValue({ affected: 1 });

      await expect(service.remove(1)).resolves.toBeUndefined();
    });

    it('should throw NotFoundException', async () => {
      mockRepository.delete.mockResolvedValue({ affected: 0 });

      await expect(service.remove(999)).rejects.toThrow(NotFoundException);
    });
  });
});
```

### Controller Tests

```typescript
// products.controller.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { ProductsController } from './products.controller';
import { ProductsService } from './products.service';
import { ProductStatus } from './product.entity';

describe('ProductsController', () => {
  let controller: ProductsController;

  const mockService = {
    findAll: jest.fn(),
    findOne: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    remove: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ProductsController],
      providers: [{ provide: ProductsService, useValue: mockService }],
    }).compile();

    controller = module.get<ProductsController>(ProductsController);
  });

  afterEach(() => jest.clearAllMocks());

  describe('findAll', () => {
    it('should return paginated products', async () => {
      const query = { page: 1, limit: 10, sortBy: 'createdAt', sortOrder: 'DESC' as const };
      const expected = {
        data: [{ id: 1, name: 'Widget' }],
        total: 1,
        page: 1,
        limit: 10,
        totalPages: 1,
      };
      mockService.findAll.mockResolvedValue(expected);

      expect(await controller.findAll(query)).toEqual(expected);
      expect(mockService.findAll).toHaveBeenCalledWith(query);
    });
  });

  describe('findOne', () => {
    it('should return a product', async () => {
      const product = { id: 1, name: 'Widget', price: 9.99 };
      mockService.findOne.mockResolvedValue(product);

      expect(await controller.findOne(1)).toEqual(product);
    });
  });

  describe('create', () => {
    it('should create a product with owner', async () => {
      const dto = { name: 'Widget', price: 9.99 };
      const created = { id: 1, ...dto, ownerId: 42 };
      mockService.create.mockResolvedValue(created);

      const result = await controller.create(dto as any, 42);

      expect(mockService.create).toHaveBeenCalledWith(dto, 42);
      expect(result).toEqual(created);
    });
  });

  describe('update', () => {
    it('should update a product', async () => {
      const dto = { name: 'Updated' };
      const updated = { id: 1, name: 'Updated', price: 9.99 };
      mockService.update.mockResolvedValue(updated);

      expect(await controller.update(1, dto as any)).toEqual(updated);
    });
  });

  describe('remove', () => {
    it('should remove a product', async () => {
      mockService.remove.mockResolvedValue(undefined);

      await controller.remove(1);

      expect(mockService.remove).toHaveBeenCalledWith(1);
    });
  });
});
```

### Guard Tests

```typescript
// guards/product-owner.guard.spec.ts
import { ExecutionContext, ForbiddenException } from '@nestjs/common';
import { ProductOwnerGuard } from './product-owner.guard';
import { ProductsService } from '../products.service';

describe('ProductOwnerGuard', () => {
  let guard: ProductOwnerGuard;

  const mockService = {
    findOne: jest.fn(),
  };

  beforeEach(() => {
    guard = new ProductOwnerGuard(mockService as unknown as ProductsService);
  });

  afterEach(() => jest.clearAllMocks());

  const createContext = (userId: number | undefined, productId: string): ExecutionContext =>
    ({
      switchToHttp: () => ({
        getRequest: () => ({
          user: userId ? { id: userId } : undefined,
          params: { id: productId },
        }),
      }),
    }) as unknown as ExecutionContext;

  it('should allow owner access', async () => {
    mockService.findOne.mockResolvedValue({ id: 1, ownerId: 42 });

    expect(await guard.canActivate(createContext(42, '1'))).toBe(true);
  });

  it('should deny non-owner access', async () => {
    mockService.findOne.mockResolvedValue({ id: 1, ownerId: 42 });

    await expect(guard.canActivate(createContext(99, '1'))).rejects.toThrow(
      ForbiddenException,
    );
  });

  it('should deny unauthenticated access', async () => {
    await expect(
      guard.canActivate(createContext(undefined, '1')),
    ).rejects.toThrow(ForbiddenException);
  });
});
```

### Exception Filter Tests

```typescript
// filters/product-exception.filter.spec.ts
import { ArgumentsHost, HttpException, HttpStatus } from '@nestjs/common';
import { ProductExceptionFilter } from './product-exception.filter';

describe('ProductExceptionFilter', () => {
  let filter: ProductExceptionFilter;

  beforeEach(() => {
    filter = new ProductExceptionFilter();
  });

  const createHost = () => {
    const json = jest.fn();
    const status = jest.fn().mockReturnValue({ json });

    const host = {
      switchToHttp: () => ({
        getResponse: () => ({ status }),
        getRequest: () => ({ url: '/products/1', method: 'GET' }),
      }),
    } as unknown as ArgumentsHost;

    return { host, status, json };
  };

  it('should handle HttpException', () => {
    const { host, status, json } = createHost();

    filter.catch(new HttpException('Not Found', HttpStatus.NOT_FOUND), host);

    expect(status).toHaveBeenCalledWith(404);
    expect(json).toHaveBeenCalledWith(
      expect.objectContaining({
        statusCode: 404,
        message: 'Not Found',
        path: '/products/1',
        method: 'GET',
      }),
    );
  });

  it('should handle unknown exceptions as 500', () => {
    const { host, status, json } = createHost();

    filter.catch(new Error('Unexpected'), host);

    expect(status).toHaveBeenCalledWith(500);
    expect(json).toHaveBeenCalledWith(
      expect.objectContaining({
        statusCode: 500,
        message: 'Internal server error',
      }),
    );
  });
});
```

---

## Registering the Module

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ProductsModule } from './products/products.module';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT, 10) || 5432,
      username: process.env.DB_USER || 'postgres',
      password: process.env.DB_PASS || 'postgres',
      database: process.env.DB_NAME || 'mydb',
      autoLoadEntities: true,
      synchronize: process.env.NODE_ENV !== 'production',
    }),
    ProductsModule,
  ],
})
export class AppModule {}
```

## API Endpoints Summary

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/products` | No | List products (paginated, filterable) |
| GET | `/products/:id` | No | Get single product |
| POST | `/products` | JWT | Create product (sets owner) |
| PUT | `/products/:id` | JWT + Owner | Update product |
| DELETE | `/products/:id` | JWT + Owner | Delete product |

### Query Parameters for GET /products

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | number | 1 | Page number |
| `limit` | number | 10 | Items per page (max 100) |
| `search` | string | — | Search in name and description |
| `status` | enum | — | Filter by status (draft/active/archived) |
| `sortBy` | string | createdAt | Column to sort by |
| `sortOrder` | ASC/DESC | DESC | Sort direction |
