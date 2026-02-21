<#
.SYNOPSIS
    Scaffolds a NestJS feature module with controller, service, DTOs, entity, and spec files.

.DESCRIPTION
    Creates a complete NestJS feature module directory structure with proper
    boilerplate code including imports, decorators, and TypeORM integration.

.PARAMETER ModuleName
    The name of the module to scaffold (e.g., "products", "users").
    Used to derive class names via PascalCase conversion.

.PARAMETER OutputDir
    The directory where the module folder will be created.
    Defaults to the current directory.

.EXAMPLE
    .\nest-module-scaffold.ps1 -ModuleName "products" -OutputDir "src"
    Creates src/products/ with all module files.
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$ModuleName,

    [Parameter(Mandatory = $false)]
    [string]$OutputDir = "."
)

$ErrorActionPreference = "Stop"

function ConvertTo-PascalCase([string]$text) {
    return ($text -split '[-_\s]' | ForEach-Object {
        $_.Substring(0, 1).ToUpper() + $_.Substring(1).ToLower()
    }) -join ''
}

function ConvertTo-CamelCase([string]$text) {
    $pascal = ConvertTo-PascalCase $text
    return $pascal.Substring(0, 1).ToLower() + $pascal.Substring(1)
}

$kebab = $ModuleName.ToLower() -replace '[_\s]', '-'
$pascal = ConvertTo-PascalCase $ModuleName
$camel = ConvertTo-CamelCase $ModuleName
$singular = if ($kebab.EndsWith('s') -and $kebab.Length -gt 1) {
    $kebab.Substring(0, $kebab.Length - 1)
} else { $kebab }
$singularPascal = ConvertTo-PascalCase $singular
$singularCamel = ConvertTo-CamelCase $singular

$moduleDir = Join-Path $OutputDir $kebab
$dtoDir = Join-Path $moduleDir "dto"

New-Item -ItemType Directory -Path $dtoDir -Force | Out-Null

# --- Entity ---
$entityContent = @"
import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

@Entity('$kebab')
export class $singularPascal {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column({ type: 'text', nullable: true })
  description: string;

  @Column({ default: true })
  isActive: boolean;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
"@
$entityContent | Set-Content -Path (Join-Path $moduleDir "$singular.entity.ts") -Encoding UTF8

# --- Create DTO ---
$createDtoContent = @"
import { IsString, IsNotEmpty, IsOptional, IsBoolean } from 'class-validator';

export class Create${singularPascal}Dto {
  @IsString()
  @IsNotEmpty()
  name: string;

  @IsString()
  @IsOptional()
  description?: string;

  @IsBoolean()
  @IsOptional()
  isActive?: boolean;
}
"@
$createDtoContent | Set-Content -Path (Join-Path $dtoDir "create-$singular.dto.ts") -Encoding UTF8

# --- Update DTO ---
$updateDtoContent = @"
import { PartialType } from '@nestjs/mapped-types';
import { Create${singularPascal}Dto } from './create-$singular.dto';

export class Update${singularPascal}Dto extends PartialType(Create${singularPascal}Dto) {}
"@
$updateDtoContent | Set-Content -Path (Join-Path $dtoDir "update-$singular.dto.ts") -Encoding UTF8

# --- Service ---
$serviceContent = @"
import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { $singularPascal } from './$singular.entity';
import { Create${singularPascal}Dto } from './dto/create-$singular.dto';
import { Update${singularPascal}Dto } from './dto/update-$singular.dto';

@Injectable()
export class ${pascal}Service {
  constructor(
    @InjectRepository($singularPascal)
    private readonly ${singularCamel}Repository: Repository<$singularPascal>,
  ) {}

  async findAll(): Promise<${singularPascal}[]> {
    return this.${singularCamel}Repository.find();
  }

  async findOne(id: number): Promise<$singularPascal> {
    const ${singularCamel} = await this.${singularCamel}Repository.findOneBy({ id });
    if (!${singularCamel}) {
      throw new NotFoundException(``$singularPascal with id `${id} not found``);
    }
    return ${singularCamel};
  }

  async create(dto: Create${singularPascal}Dto): Promise<$singularPascal> {
    const ${singularCamel} = this.${singularCamel}Repository.create(dto);
    return this.${singularCamel}Repository.save(${singularCamel});
  }

  async update(id: number, dto: Update${singularPascal}Dto): Promise<$singularPascal> {
    await this.findOne(id);
    await this.${singularCamel}Repository.update(id, dto);
    return this.findOne(id);
  }

  async remove(id: number): Promise<void> {
    const result = await this.${singularCamel}Repository.delete(id);
    if (result.affected === 0) {
      throw new NotFoundException(``$singularPascal with id `${id} not found``);
    }
  }
}
"@
$serviceContent | Set-Content -Path (Join-Path $moduleDir "$kebab.service.ts") -Encoding UTF8

# --- Controller ---
$controllerContent = @"
import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Body,
  Param,
  ParseIntPipe,
  HttpCode,
  HttpStatus,
} from '@nestjs/common';
import { ${pascal}Service } from './$kebab.service';
import { Create${singularPascal}Dto } from './dto/create-$singular.dto';
import { Update${singularPascal}Dto } from './dto/update-$singular.dto';

@Controller('$kebab')
export class ${pascal}Controller {
  constructor(private readonly ${camel}Service: ${pascal}Service) {}

  @Get()
  findAll() {
    return this.${camel}Service.findAll();
  }

  @Get(':id')
  findOne(@Param('id', ParseIntPipe) id: number) {
    return this.${camel}Service.findOne(id);
  }

  @Post()
  @HttpCode(HttpStatus.CREATED)
  create(@Body() dto: Create${singularPascal}Dto) {
    return this.${camel}Service.create(dto);
  }

  @Put(':id')
  update(
    @Param('id', ParseIntPipe) id: number,
    @Body() dto: Update${singularPascal}Dto,
  ) {
    return this.${camel}Service.update(id, dto);
  }

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  remove(@Param('id', ParseIntPipe) id: number) {
    return this.${camel}Service.remove(id);
  }
}
"@
$controllerContent | Set-Content -Path (Join-Path $moduleDir "$kebab.controller.ts") -Encoding UTF8

# --- Module ---
$moduleContent = @"
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ${pascal}Controller } from './$kebab.controller';
import { ${pascal}Service } from './$kebab.service';
import { $singularPascal } from './$singular.entity';

@Module({
  imports: [TypeOrmModule.forFeature([$singularPascal])],
  controllers: [${pascal}Controller],
  providers: [${pascal}Service],
  exports: [${pascal}Service],
})
export class ${pascal}Module {}
"@
$moduleContent | Set-Content -Path (Join-Path $moduleDir "$kebab.module.ts") -Encoding UTF8

# --- Service Spec ---
$serviceSpecContent = @"
import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { NotFoundException } from '@nestjs/common';
import { ${pascal}Service } from './$kebab.service';
import { $singularPascal } from './$singular.entity';

describe('${pascal}Service', () => {
  let service: ${pascal}Service;

  const mockRepository = {
    find: jest.fn(),
    findOneBy: jest.fn(),
    create: jest.fn(),
    save: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ${pascal}Service,
        {
          provide: getRepositoryToken($singularPascal),
          useValue: mockRepository,
        },
      ],
    }).compile();

    service = module.get<${pascal}Service>(${pascal}Service);
  });

  afterEach(() => jest.clearAllMocks());

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('findAll', () => {
    it('should return all ${kebab}', async () => {
      const items = [{ id: 1, name: 'Test' }];
      mockRepository.find.mockResolvedValue(items);

      const result = await service.findAll();
      expect(result).toEqual(items);
    });
  });

  describe('findOne', () => {
    it('should return a $singular by id', async () => {
      const item = { id: 1, name: 'Test' };
      mockRepository.findOneBy.mockResolvedValue(item);

      const result = await service.findOne(1);
      expect(result).toEqual(item);
    });

    it('should throw NotFoundException', async () => {
      mockRepository.findOneBy.mockResolvedValue(null);
      await expect(service.findOne(999)).rejects.toThrow(NotFoundException);
    });
  });

  describe('create', () => {
    it('should create a $singular', async () => {
      const dto = { name: 'New' };
      const created = { id: 1, ...dto };
      mockRepository.create.mockReturnValue(created);
      mockRepository.save.mockResolvedValue(created);

      const result = await service.create(dto as any);
      expect(result).toEqual(created);
    });
  });

  describe('remove', () => {
    it('should delete a $singular', async () => {
      mockRepository.delete.mockResolvedValue({ affected: 1 });
      await expect(service.remove(1)).resolves.toBeUndefined();
    });

    it('should throw NotFoundException for missing $singular', async () => {
      mockRepository.delete.mockResolvedValue({ affected: 0 });
      await expect(service.remove(999)).rejects.toThrow(NotFoundException);
    });
  });
});
"@
$serviceSpecContent | Set-Content -Path (Join-Path $moduleDir "$kebab.service.spec.ts") -Encoding UTF8

# --- Controller Spec ---
$controllerSpecContent = @"
import { Test, TestingModule } from '@nestjs/testing';
import { ${pascal}Controller } from './$kebab.controller';
import { ${pascal}Service } from './$kebab.service';

describe('${pascal}Controller', () => {
  let controller: ${pascal}Controller;

  const mockService = {
    findAll: jest.fn(),
    findOne: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    remove: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [${pascal}Controller],
      providers: [{ provide: ${pascal}Service, useValue: mockService }],
    }).compile();

    controller = module.get<${pascal}Controller>(${pascal}Controller);
  });

  afterEach(() => jest.clearAllMocks());

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  describe('findAll', () => {
    it('should return all ${kebab}', async () => {
      const items = [{ id: 1, name: 'Test' }];
      mockService.findAll.mockResolvedValue(items);

      expect(await controller.findAll()).toEqual(items);
    });
  });

  describe('findOne', () => {
    it('should return a $singular', async () => {
      const item = { id: 1, name: 'Test' };
      mockService.findOne.mockResolvedValue(item);

      expect(await controller.findOne(1)).toEqual(item);
    });
  });

  describe('create', () => {
    it('should create a $singular', async () => {
      const dto = { name: 'New' };
      const created = { id: 1, ...dto };
      mockService.create.mockResolvedValue(created);

      expect(await controller.create(dto as any)).toEqual(created);
    });
  });
});
"@
$controllerSpecContent | Set-Content -Path (Join-Path $moduleDir "$kebab.controller.spec.ts") -Encoding UTF8

Write-Host ""
Write-Host "NestJS module '$pascal' scaffolded at: $moduleDir" -ForegroundColor Green
Write-Host ""
Write-Host "Files created:" -ForegroundColor Cyan
Get-ChildItem -Path $moduleDir -Recurse -File | ForEach-Object {
    Write-Host "  $($_.FullName.Replace($moduleDir, $kebab))" -ForegroundColor Gray
}
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Import ${pascal}Module in your AppModule"
Write-Host "  2. Add the $singularPascal entity to your TypeOrm configuration"
Write-Host "  3. Customize the entity columns and DTO validations"
Write-Host "  4. Run tests:  npm run test -- --testPathPattern=$kebab"
