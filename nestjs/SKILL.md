---
name: nestjs
description: NestJS framework — modules, controllers, DI, TypeORM, JWT auth, RBAC guards, DTOs with class-validator, and testing. Use when building server-side Node.js APIs or services with the NestJS framework.
license: Complete terms in LICENSE.txt
---



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`


Expert guidance for building scalable, maintainable NestJS applications using TypeScript, decorators, dependency injection, and modern Node.js patterns.

## When to Use This Skill

- Building NestJS server-side applications
- Implementing dependency injection and modular architecture
- Creating REST APIs with controllers, services, and DTOs
- Configuring TypeORM entities, repositories, and migrations
- Setting up JWT authentication and role-based access control
- Writing exception filters, interceptors, pipes, and guards
- Testing NestJS services (unit, integration, e2e)


---

## Core Principles

### Dependency Injection
- Use `@Injectable()` for services, repositories, and providers
- Inject through constructor parameters with proper typing
- Prefer interface-based DI for testability
- Use custom providers for specific instantiation logic

### Modular Architecture
- Create feature modules with `@Module()`
- Import only necessary modules, avoid circular dependencies
- Use `forRoot()` and `forFeature()` for configurable modules
- Shared modules for common functionality

### Decorators and Metadata
- Use appropriate decorators: `@Controller()`, `@Get()`, `@Post()`, `@Injectable()`
- Apply validation decorators from `class-validator`
- Custom decorators for cross-cutting concerns

---

## Project Structure

```
src/
├── app.module.ts
├── main.ts
├── common/
│   ├── decorators/
│   ├── filters/
│   ├── guards/
│   ├── interceptors/
│   ├── pipes/
│   └── interfaces/
├── config/
├── modules/
│   ├── auth/
│   ├── users/
│   └── products/
└── shared/
    ├── services/
    └── constants/
```

### File Naming
- Controllers: `*.controller.ts`
- Services: `*.service.ts`
- Modules: `*.module.ts`
- DTOs: `*.dto.ts`
- Entities: `*.entity.ts`
- Guards: `*.guard.ts`
- Interceptors: `*.interceptor.ts`
- Pipes: `*.pipe.ts`
- Filters: `*.filter.ts`

---

## API Development Patterns

### Controllers
- Keep thin — delegate business logic to services
- Use proper HTTP methods and status codes
- Validate input with DTOs
- Apply guards/interceptors at appropriate level

```typescript
@Controller('users')
@UseGuards(AuthGuard)
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  @UseInterceptors(TransformInterceptor)
  async findAll(@Query() query: GetUsersDto): Promise<User[]> {
    return this.usersService.findAll(query);
  }

  @Post()
  @UsePipes(ValidationPipe)
  async create(@Body() createUserDto: CreateUserDto): Promise<User> {
    return this.usersService.create(createUserDto);
  }
}
```

### Services
```typescript
@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private readonly userRepository: Repository<User>,
    private readonly emailService: EmailService,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<User> {
    const user = this.userRepository.create(createUserDto);
    const savedUser = await this.userRepository.save(user);
    await this.emailService.sendWelcomeEmail(savedUser.email);
    return savedUser;
  }
}
```

### DTOs and Validation
```typescript
export class CreateUserDto {
  @IsString()
  @IsNotEmpty()
  @Length(2, 50)
  name: string;

  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, {
    message: 'Password must contain uppercase, lowercase and number',
  })
  password: string;
}
```

---

## Database Integration (TypeORM)

```typescript
@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ unique: true })
  email: string;

  @Column()
  name: string;

  @Column({ select: false })
  password: string;

  @OneToMany(() => Post, post => post.author)
  posts: Post[];

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

- Use migrations for schema changes
- Extend base repository for complex queries
- Use query builders for dynamic queries

---

## Authentication & Authorization

### JWT Authentication
- Implement with Passport
- Use guards to protect routes
- Custom decorators for user context

```typescript
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  handleRequest(err: any, user: any) {
    if (err || !user) throw err || new UnauthorizedException();
    return user;
  }
}
```

### Role-Based Access Control
```typescript
@SetMetadata('roles', ['admin'])
@UseGuards(JwtAuthGuard, RolesGuard)
@Delete(':id')
async remove(@Param('id') id: string): Promise<void> {
  return this.usersService.remove(id);
}
```

---

## Error Handling

```typescript
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger(AllExceptionsFilter.name);

  catch(exception: unknown, host: ArgumentsHost): void {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    const status = exception instanceof HttpException
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;

    this.logger.error(`${request.method} ${request.url}`, exception);

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message: exception instanceof HttpException
        ? exception.message
        : 'Internal server error',
    });
  }
}
```

---

## Testing

### Unit Testing
```typescript
describe('UsersService', () => {
  let service: UsersService;
  let repository: Repository<User>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: getRepositoryToken(User),
          useValue: { create: jest.fn(), save: jest.fn(), find: jest.fn() },
        },
      ],
    }).compile();

    service = module.get<UsersService>(UsersService);
    repository = module.get<Repository<User>>(getRepositoryToken(User));
  });

  it('should create a user', async () => {
    const dto = { name: 'John', email: 'john@example.com' };
    const user = { id: '1', ...dto };
    jest.spyOn(repository, 'create').mockReturnValue(user as User);
    jest.spyOn(repository, 'save').mockResolvedValue(user as User);
    expect(await service.create(dto)).toEqual(user);
  });
});
```

### E2E Testing
- Test complete request/response cycles with supertest
- Test authentication and authorization flows

---

## Performance & Security

### Performance
- Caching with Redis
- Interceptors for response transformation
- Database indexing and pagination

### Security
- Validate all inputs with class-validator
- Rate limiting to prevent abuse
- Proper CORS configuration
- Sanitize outputs to prevent XSS
- Environment variables for sensitive config

```typescript
@Controller('auth')
@UseGuards(ThrottlerGuard)
export class AuthController {
  @Post('login')
  @Throttle(5, 60)
  async login(@Body() loginDto: LoginDto) {
    return this.authService.login(loginDto);
  }
}
```

---

## Common Pitfalls
- **Circular Dependencies**: Avoid circular module imports
- **Heavy Controllers**: Don't put business logic in controllers
- **Missing Error Handling**: Always handle errors appropriately
- **Improper DI**: Don't create instances manually when DI can handle it
- **Missing Validation**: Always validate input data
- **Synchronous Operations**: Use async/await for DB and API calls
- **Memory Leaks**: Properly dispose subscriptions and event listeners

## Development Workflow
1. Use NestJS CLI: `nest generate module users`
2. Follow consistent file organization
3. TypeScript strict mode
4. ESLint + Prettier for code quality

## Code Review Checklist
- [ ] Proper decorators and dependency injection
- [ ] Input validation with DTOs and class-validator
- [ ] Appropriate error handling and exception filters
- [ ] Consistent naming conventions
- [ ] Proper module organization
- [ ] Security considerations
- [ ] Performance considerations
- [ ] Comprehensive test coverage

---

## References & Resources

### Documentation
- [Decorators Reference](./references/decorators-reference.md) — Complete NestJS decorators catalog by category with usage examples
- [Testing Patterns](./references/testing-patterns.md) — Unit, integration, and e2e testing patterns with mocking strategies

### Scripts
- [Module Scaffold](./scripts/nest-module-scaffold.ps1) — PowerShell script to generate a NestJS feature module structure

### Examples
- [CRUD Module Example](./examples/crud-module-example.md) — Complete Products CRUD module with controller, service, DTOs, entity, and tests

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [mongodb-mongoose](../mongodb-mongoose/SKILL.md) | MongoDB integration with NestJS |
| [javascript-development](../javascript-development/SKILL.md) | Core JS/TS patterns for NestJS |
| [sql-development](../sql-development/SKILL.md) | SQL/TypeORM database integration |
| [php-development](../php-development/SKILL.md) | Alternative backend framework comparison |
