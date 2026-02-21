# NestJS Decorators Quick Reference

## Controllers

### @Controller

Marks a class as a NestJS controller that handles incoming requests.

```typescript
// Basic
@Controller('users')
export class UsersController {}

// Versioned
@Controller({ path: 'users', version: '1' })
export class UsersV1Controller {}

// Host-scoped
@Controller({ host: 'admin.example.com' })
export class AdminController {}
```

**Parameters:**
- `prefix?: string` — Route path prefix
- `options?: { path?: string; host?: string; version?: string | string[]; scope?: Scope }`

---

### @Get / @Post / @Put / @Delete / @Patch

HTTP method decorators that map handler methods to request methods and paths.

```typescript
@Controller('products')
export class ProductsController {
  @Get()
  findAll() { /* GET /products */ }

  @Get(':id')
  findOne(@Param('id') id: string) { /* GET /products/:id */ }

  @Post()
  create(@Body() dto: CreateProductDto) { /* POST /products */ }

  @Put(':id')
  update(@Param('id') id: string, @Body() dto: UpdateProductDto) { /* PUT /products/:id */ }

  @Patch(':id')
  partialUpdate(@Param('id') id: string, @Body() dto: Partial<UpdateProductDto>) { /* PATCH /products/:id */ }

  @Delete(':id')
  remove(@Param('id') id: string) { /* DELETE /products/:id */ }
}
```

**Parameters:**
- `path?: string | string[]` — Sub-route path appended to the controller prefix

---

### @Param

Extracts route parameters from the request path.

```typescript
// Single param
@Get(':id')
findOne(@Param('id') id: string) {}

// Parsed param with pipe
@Get(':id')
findOne(@Param('id', ParseIntPipe) id: number) {}

// All params as object
@Get(':category/:id')
find(@Param() params: { category: string; id: string }) {}
```

---

### @Query

Extracts query string parameters.

```typescript
// Single query param
@Get()
search(@Query('term') term: string) {}

// With default value via pipe
@Get()
findAll(@Query('page', new DefaultValuePipe(1), ParseIntPipe) page: number) {}

// All query params
@Get()
filter(@Query() query: FilterDto) {}
```

---

### @Body

Extracts the request body.

```typescript
// Full body
@Post()
create(@Body() dto: CreateUserDto) {}

// Specific property
@Post()
create(@Body('name') name: string) {}

// With validation pipe
@Post()
create(@Body(new ValidationPipe({ whitelist: true })) dto: CreateUserDto) {}
```

---

### @Headers

Extracts request headers.

```typescript
// Single header
@Get()
check(@Headers('authorization') auth: string) {}

// All headers
@Get()
debug(@Headers() headers: Record<string, string>) {}
```

---

### @HttpCode

Sets the response HTTP status code for a handler.

```typescript
@Post()
@HttpCode(201)
create(@Body() dto: CreateDto) {}

@Delete(':id')
@HttpCode(204)
remove(@Param('id') id: string) {}

@Post('login')
@HttpCode(200) // Override default 201 for POST
login(@Body() dto: LoginDto) {}
```

**Parameters:**
- `statusCode: number` — HTTP status code

---

### @Redirect

Redirects to a different URL.

```typescript
@Get('old-path')
@Redirect('https://example.com/new-path', 301)
redirectOld() {}

// Dynamic redirect (return object overrides decorator)
@Get('docs')
@Redirect('https://docs.example.com', 302)
getDocs(@Query('version') version: string) {
  if (version === 'v2') {
    return { url: 'https://docs.example.com/v2' };
  }
}
```

---

### @Res / @Req

Inject the underlying platform response/request object.

```typescript
import { Request, Response } from 'express';

@Get()
findAll(@Req() req: Request, @Res() res: Response) {
  res.status(200).json({ data: [] });
}

// Passthrough mode: lets NestJS still handle response
@Get()
findAll(@Res({ passthrough: true }) res: Response) {
  res.header('X-Custom', 'value');
  return { data: [] }; // NestJS serializes this
}
```

---

## Modules

### @Module

Defines a module — the basic organizational unit in NestJS.

```typescript
@Module({
  imports: [TypeOrmModule.forFeature([Product])],
  controllers: [ProductsController],
  providers: [ProductsService],
  exports: [ProductsService],
})
export class ProductsModule {}
```

**Properties:**
- `imports` — Modules whose exported providers are needed
- `controllers` — Controllers instantiated by this module
- `providers` — Providers instantiated and potentially shared
- `exports` — Providers available to other importing modules

---

### @Global

Makes a module global-scoped (available everywhere without importing).

```typescript
@Global()
@Module({
  providers: [ConfigService],
  exports: [ConfigService],
})
export class ConfigModule {}
```

---

### @Injectable

Marks a class as a provider that can be injected via DI.

```typescript
@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private readonly userRepo: Repository<User>,
  ) {}
}

// With scope
@Injectable({ scope: Scope.REQUEST })
export class RequestScopedService {}
```

**Parameters:**
- `options?: { scope?: Scope }` — `Scope.DEFAULT`, `Scope.REQUEST`, `Scope.TRANSIENT`

---

## Authentication & Authorization

### @UseGuards

Binds guard(s) to a controller or handler.

```typescript
// Single guard
@UseGuards(AuthGuard('jwt'))
@Controller('protected')
export class ProtectedController {}

// Multiple guards (executed in order)
@UseGuards(JwtAuthGuard, RolesGuard)
@Get('admin')
adminOnly() {}

// Inline guard instance
@UseGuards(new ThrottlerGuard())
@Post('login')
login() {}
```

---

### @SetMetadata

Attaches custom metadata to a handler (used with guards/interceptors).

```typescript
// Direct usage
@SetMetadata('roles', ['admin'])
@Get()
adminRoute() {}

// Custom decorator (preferred)
export const Roles = (...roles: string[]) => SetMetadata('roles', roles);

// Usage with custom decorator
@Roles('admin', 'moderator')
@Get()
modRoute() {}
```

Accessing metadata in a guard:

```typescript
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const roles = this.reflector.getAllAndOverride<string[]>('roles', [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!roles) return true;
    const request = context.switchToHttp().getRequest();
    return roles.some((role) => request.user?.roles?.includes(role));
  }
}
```

---

## Validation

### @UsePipes

Binds pipe(s) to a controller or handler for input transformation/validation.

```typescript
// Global validation pipe on a handler
@Post()
@UsePipes(new ValidationPipe({ whitelist: true, transform: true }))
create(@Body() dto: CreateUserDto) {}

// Controller-level
@UsePipes(ValidationPipe)
@Controller('users')
export class UsersController {}
```

---

### class-validator Decorators

Used in DTOs for declarative validation.

```typescript
import {
  IsString, IsEmail, IsNotEmpty, MinLength, MaxLength,
  IsInt, Min, Max, IsOptional, IsEnum, IsBoolean,
  IsArray, ArrayMinSize, ValidateNested, IsUUID,
  IsDateString, Matches, IsUrl, IsNumber,
} from 'class-validator';
import { Type } from 'class-transformer';

export class CreateUserDto {
  @IsString()
  @IsNotEmpty()
  @MinLength(2)
  @MaxLength(50)
  name: string;

  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  @Matches(/(?=.*\d)(?=.*[a-z])(?=.*[A-Z])/, {
    message: 'Password must contain uppercase, lowercase, and number',
  })
  password: string;

  @IsOptional()
  @IsInt()
  @Min(0)
  @Max(150)
  age?: number;

  @IsEnum(UserRole)
  role: UserRole;

  @IsBoolean()
  @IsOptional()
  isActive?: boolean;

  @IsArray()
  @ArrayMinSize(1)
  @IsString({ each: true })
  tags: string[];

  @ValidateNested()
  @Type(() => AddressDto)
  address: AddressDto;

  @IsUUID()
  organizationId: string;

  @IsDateString()
  birthDate: string;

  @IsUrl()
  @IsOptional()
  website?: string;

  @IsNumber({ maxDecimalPlaces: 2 })
  @Min(0)
  salary: number;
}
```

---

### class-transformer Decorators

Used alongside class-validator for request transformation.

```typescript
import { Type, Exclude, Expose, Transform } from 'class-transformer';

export class UserResponseDto {
  @Expose()
  id: number;

  @Expose()
  name: string;

  @Exclude()
  password: string;

  @Transform(({ value }) => value.toISOString())
  createdAt: Date;

  @Type(() => Number)
  age: number;
}
```

---

## WebSocket

### @WebSocketGateway

Marks a class as a WebSocket gateway.

```typescript
// Default options
@WebSocketGateway()
export class EventsGateway {}

// Custom port and namespace
@WebSocketGateway(8080, { namespace: 'events', cors: { origin: '*' } })
export class EventsGateway {}

// Extracting the server instance
@WebSocketGateway()
export class EventsGateway {
  @WebSocketServer()
  server: Server;
}
```

**Parameters:**
- `port?: number` — Port to listen on (defaults to HTTP server port)
- `options?: GatewayMetadata` — namespace, cors, transports, etc.

---

### @SubscribeMessage

Subscribes a handler to a specific WebSocket event.

```typescript
@WebSocketGateway()
export class ChatGateway {
  @WebSocketServer()
  server: Server;

  @SubscribeMessage('message')
  handleMessage(
    @MessageBody() data: { room: string; text: string },
    @ConnectedSocket() client: Socket,
  ): WsResponse<string> {
    this.server.to(data.room).emit('message', data.text);
    return { event: 'message', data: 'sent' };
  }

  @SubscribeMessage('join')
  handleJoin(
    @MessageBody('room') room: string,
    @ConnectedSocket() client: Socket,
  ) {
    client.join(room);
    return { event: 'joined', data: room };
  }
}
```

---

### @MessageBody / @ConnectedSocket

Extract the message payload or the client socket.

```typescript
@SubscribeMessage('event')
handle(
  @MessageBody() data: any,                    // full payload
  @MessageBody('field') field: string,         // specific field
  @ConnectedSocket() client: Socket,           // socket instance
) {}
```

---

## Interceptors & Pipes

### @UseInterceptors

Binds interceptor(s) to a controller or handler.

```typescript
@UseInterceptors(LoggingInterceptor)
@Controller('cats')
export class CatsController {}

@UseInterceptors(ClassSerializerInterceptor)
@Get(':id')
findOne(@Param('id') id: string) {}

@UseInterceptors(CacheInterceptor)
@Get()
findAll() {}
```

---

### @UseFilters

Binds exception filter(s) to a controller or handler.

```typescript
@UseFilters(HttpExceptionFilter)
@Controller('users')
export class UsersController {}

@UseFilters(new CustomExceptionFilter())
@Post()
create() {}
```

---

## Miscellaneous

### @Inject

Injects a provider by token (useful for non-class tokens).

```typescript
@Injectable()
export class AppService {
  constructor(
    @Inject('CONFIG') private config: AppConfig,
    @Inject(CACHE_MANAGER) private cacheManager: Cache,
  ) {}
}
```

### @Optional

Marks a dependency as optional (won't throw if not available).

```typescript
@Injectable()
export class NotificationService {
  constructor(
    @Optional() @Inject('MAILER') private mailer?: MailerService,
  ) {}
}
```

### Custom Decorator (createParamDecorator)

```typescript
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const CurrentUser = createParamDecorator(
  (data: string, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;
    return data ? user?.[data] : user;
  },
);

// Usage
@Get('me')
getProfile(@CurrentUser() user: User) {}

@Get('my-email')
getEmail(@CurrentUser('email') email: string) {}
```
