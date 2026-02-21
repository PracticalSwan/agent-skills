<#
.SYNOPSIS
    Scaffolds React components with TypeScript, Tailwind CSS, and accessibility.

.DESCRIPTION
    Generates a React component file (.tsx), optional test file (.test.tsx),
    optional Storybook story (.stories.tsx), and an index barrel file.

.PARAMETER Name
    Component name in PascalCase (e.g., UserCard, LoginForm).

.PARAMETER Type
    Component type: functional, page, form, modal, context.

.PARAMETER OutputDir
    Output directory. Defaults to current directory.

.PARAMETER WithTest
    Generate a test file alongside the component.

.PARAMETER WithStory
    Generate a Storybook story file alongside the component.

.EXAMPLE
    .\component-generator.ps1 -Name UserCard -Type functional -OutputDir ./src/components -WithTest -WithStory

.EXAMPLE
    .\component-generator.ps1 -Name AuthContext -Type context -OutputDir ./src/context
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, HelpMessage = "Component name in PascalCase")]
    [ValidatePattern('^[A-Z][a-zA-Z0-9]+$')]
    [string]$Name,

    [Parameter(Mandatory = $false, HelpMessage = "Component type")]
    [ValidateSet('functional', 'page', 'form', 'modal', 'context')]
    [string]$Type = 'functional',

    [Parameter(Mandatory = $false, HelpMessage = "Output directory")]
    [string]$OutputDir = '.',

    [Parameter(Mandatory = $false, HelpMessage = "Generate test file")]
    [switch]$WithTest,

    [Parameter(Mandatory = $false, HelpMessage = "Generate Storybook story")]
    [switch]$WithStory
)

$ErrorActionPreference = 'Stop'

# --- Helpers ---

function ConvertTo-KebabCase([string]$text) {
    return ($text -creplace '([a-z])([A-Z])', '$1-$2').ToLower()
}

$kebabName = ConvertTo-KebabCase $Name
$componentDir = Join-Path $OutputDir $Name

if (Test-Path $componentDir) {
    Write-Warning "Directory '$componentDir' already exists. Files may be overwritten."
} else {
    New-Item -ItemType Directory -Path $componentDir -Force | Out-Null
}

# --- Component Templates ---

function Get-FunctionalTemplate {
    return @"
import { type HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

export interface ${Name}Props extends HTMLAttributes<HTMLDivElement> {
  /** Add component-specific props here */
}

export function ${Name}({ className, ...props }: ${Name}Props) {
  return (
    <div
      className={cn('', className)}
      role="region"
      aria-label="${Name}"
      {...props}
    >
      <p>${Name} component</p>
    </div>
  );
}

export default ${Name};
"@
}

function Get-PageTemplate {
    return @"
import { type HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

export interface ${Name}Props extends HTMLAttributes<HTMLElement> {
  /** Add page-specific props here */
}

export function ${Name}({ className, ...props }: ${Name}Props) {
  return (
    <main
      className={cn('mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8', className)}
      {...props}
    >
      <header className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900">
          ${Name}
        </h1>
      </header>
      <section>
        <p>Page content goes here.</p>
      </section>
    </main>
  );
}

export default ${Name};
"@
}

function Get-FormTemplate {
    return @"
'use client';

import { useState, type FormEvent } from 'react';
import { cn } from '@/lib/utils';

export interface ${Name}Data {
  /** Define form field types here */
  email: string;
  message: string;
}

export interface ${Name}Props {
  onSubmit: (data: ${Name}Data) => void | Promise<void>;
  className?: string;
  defaultValues?: Partial<${Name}Data>;
}

const INITIAL_STATE: ${Name}Data = {
  email: '',
  message: '',
};

export function ${Name}({ onSubmit, className, defaultValues }: ${Name}Props) {
  const [formData, setFormData] = useState<${Name}Data>({
    ...INITIAL_STATE,
    ...defaultValues,
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<Partial<Record<keyof ${Name}Data, string>>>({});

  function validate(data: ${Name}Data): boolean {
    const newErrors: Partial<Record<keyof ${Name}Data, string>> = {};
    if (!data.email.trim()) newErrors.email = 'Email is required';
    if (!data.message.trim()) newErrors.message = 'Message is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!validate(formData)) return;

    setIsSubmitting(true);
    try {
      await onSubmit(formData);
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleChange(field: keyof ${Name}Data, value: string) {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) setErrors((prev) => ({ ...prev, [field]: undefined }));
  }

  return (
    <form
      onSubmit={handleSubmit}
      className={cn('space-y-4', className)}
      noValidate
      aria-label="${Name}"
    >
      <div>
        <label htmlFor="${kebabName}-email" className="block text-sm font-medium text-gray-700">
          Email
        </label>
        <input
          id="${kebabName}-email"
          type="email"
          value={formData.email}
          onChange={(e) => handleChange('email', e.target.value)}
          className={cn(
            'mt-1 block w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-2',
            errors.email ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'
          )}
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? '${kebabName}-email-error' : undefined}
          disabled={isSubmitting}
        />
        {errors.email && (
          <p id="${kebabName}-email-error" className="mt-1 text-sm text-red-600" role="alert">
            {errors.email}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="${kebabName}-message" className="block text-sm font-medium text-gray-700">
          Message
        </label>
        <textarea
          id="${kebabName}-message"
          value={formData.message}
          onChange={(e) => handleChange('message', e.target.value)}
          rows={4}
          className={cn(
            'mt-1 block w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-2',
            errors.message ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'
          )}
          aria-invalid={!!errors.message}
          aria-describedby={errors.message ? '${kebabName}-message-error' : undefined}
          disabled={isSubmitting}
        />
        {errors.message && (
          <p id="${kebabName}-message-error" className="mt-1 text-sm text-red-600" role="alert">
            {errors.message}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="rounded-md bg-blue-600 px-4 py-2 text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}

export default ${Name};
"@
}

function Get-ModalTemplate {
    return @"
'use client';

import { useEffect, useRef, type ReactNode, type KeyboardEvent } from 'react';
import { cn } from '@/lib/utils';

export interface ${Name}Props {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

export function ${Name}({ isOpen, onClose, title, children, className, size = 'md' }: ${Name}Props) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  const sizes = {
    sm: 'max-w-sm',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
  };

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;

    if (isOpen) {
      previousFocusRef.current = document.activeElement as HTMLElement;
      dialog.showModal();
    } else {
      dialog.close();
      previousFocusRef.current?.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    function handleEscape(e: globalThis.KeyboardEvent) {
      if (e.key === 'Escape' && isOpen) onClose();
    }
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  function handleBackdropClick(e: React.MouseEvent<HTMLDialogElement>) {
    if (e.target === dialogRef.current) onClose();
  }

  if (!isOpen) return null;

  return (
    <dialog
      ref={dialogRef}
      onClick={handleBackdropClick}
      className="fixed inset-0 z-50 backdrop:bg-black/50"
      aria-labelledby="${kebabName}-title"
    >
      <div className={cn('mx-auto mt-20 w-full rounded-lg bg-white p-6 shadow-xl', sizes[size], className)}>
        <header className="mb-4 flex items-center justify-between">
          <h2 id="${kebabName}-title" className="text-xl font-semibold">
            {title}
          </h2>
          <button
            onClick={onClose}
            className="rounded-full p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
            aria-label="Close dialog"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </header>
        <div>{children}</div>
      </div>
    </dialog>
  );
}

export default ${Name};
"@
}

function Get-ContextTemplate {
    return @"
'use client';

import {
  createContext,
  useContext,
  useState,
  useCallback,
  useMemo,
  type ReactNode,
} from 'react';

// --- Types ---

export interface ${Name}State {
  /** Define the context state shape here */
  value: string;
}

export interface ${Name}Actions {
  /** Define actions here */
  setValue: (value: string) => void;
  reset: () => void;
}

export type ${Name}Value = ${Name}State & ${Name}Actions;

// --- Context ---

const ${Name} = createContext<${Name}Value | undefined>(undefined);

// --- Hook ---

export function use${Name}(): ${Name}Value {
  const context = useContext(${Name});
  if (!context) {
    throw new Error('use${Name} must be used within a ${Name}Provider');
  }
  return context;
}

// --- Provider ---

const INITIAL_STATE: ${Name}State = {
  value: '',
};

export interface ${Name}ProviderProps {
  children: ReactNode;
  initialState?: Partial<${Name}State>;
}

export function ${Name}Provider({ children, initialState }: ${Name}ProviderProps) {
  const [state, setState] = useState<${Name}State>({
    ...INITIAL_STATE,
    ...initialState,
  });

  const setValue = useCallback((value: string) => {
    setState((prev) => ({ ...prev, value }));
  }, []);

  const reset = useCallback(() => {
    setState(INITIAL_STATE);
  }, []);

  const contextValue = useMemo<${Name}Value>(
    () => ({ ...state, setValue, reset }),
    [state, setValue, reset]
  );

  return <${Name}.Provider value={contextValue}>{children}</${Name}.Provider>;
}

export default ${Name};
"@
}

# --- Test Template ---

function Get-TestTemplate {
    switch ($Type) {
        'context' {
            return @"
import { render, screen, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import { ${Name}Provider, use${Name} } from './${Name}';

function TestConsumer() {
  const { value, setValue, reset } = use${Name}();
  return (
    <div>
      <span data-testid="value">{value}</span>
      <button onClick={() => setValue('updated')}>Update</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}

describe('${Name}', () => {
  it('provides default context values', () => {
    render(
      <${Name}Provider>
        <TestConsumer />
      </${Name}Provider>
    );
    expect(screen.getByTestId('value').textContent).toBe('');
  });

  it('updates value via context action', async () => {
    const user = userEvent.setup();
    render(
      <${Name}Provider>
        <TestConsumer />
      </${Name}Provider>
    );
    await user.click(screen.getByText('Update'));
    expect(screen.getByTestId('value').textContent).toBe('updated');
  });

  it('resets state', async () => {
    const user = userEvent.setup();
    render(
      <${Name}Provider>
        <TestConsumer />
      </${Name}Provider>
    );
    await user.click(screen.getByText('Update'));
    await user.click(screen.getByText('Reset'));
    expect(screen.getByTestId('value').textContent).toBe('');
  });

  it('throws when used outside provider', () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    expect(() => render(<TestConsumer />)).toThrow(
      'use${Name} must be used within a ${Name}Provider'
    );
    consoleSpy.mockRestore();
  });
});
"@
        }
        'form' {
            return @"
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { ${Name} } from './${Name}';

describe('${Name}', () => {
  const mockSubmit = vi.fn();

  beforeEach(() => {
    mockSubmit.mockClear();
  });

  it('renders all form fields', () => {
    render(<${Name} onSubmit={mockSubmit} />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/message/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  it('shows validation errors for empty fields', async () => {
    const user = userEvent.setup();
    render(<${Name} onSubmit={mockSubmit} />);
    await user.click(screen.getByRole('button', { name: /submit/i }));
    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/message is required/i)).toBeInTheDocument();
    expect(mockSubmit).not.toHaveBeenCalled();
  });

  it('submits valid form data', async () => {
    const user = userEvent.setup();
    render(<${Name} onSubmit={mockSubmit} />);
    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/message/i), 'Hello');
    await user.click(screen.getByRole('button', { name: /submit/i }));
    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        message: 'Hello',
      });
    });
  });

  it('disables submit button while submitting', async () => {
    const user = userEvent.setup();
    mockSubmit.mockImplementation(() => new Promise((r) => setTimeout(r, 100)));
    render(<${Name} onSubmit={mockSubmit} />);
    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/message/i), 'Hello');
    await user.click(screen.getByRole('button', { name: /submit/i }));
    expect(screen.getByRole('button', { name: /submitting/i })).toBeDisabled();
  });
});
"@
        }
        'modal' {
            return @"
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { ${Name} } from './${Name}';

describe('${Name}', () => {
  const mockClose = vi.fn();

  beforeEach(() => {
    mockClose.mockClear();
  });

  it('renders when open', () => {
    render(
      <${Name} isOpen={true} onClose={mockClose} title="Test Modal">
        <p>Modal content</p>
      </${Name}>
    );
    expect(screen.getByText('Test Modal')).toBeInTheDocument();
    expect(screen.getByText('Modal content')).toBeInTheDocument();
  });

  it('does not render when closed', () => {
    render(
      <${Name} isOpen={false} onClose={mockClose} title="Test Modal">
        <p>Modal content</p>
      </${Name}>
    );
    expect(screen.queryByText('Test Modal')).not.toBeInTheDocument();
  });

  it('calls onClose when close button is clicked', async () => {
    const user = userEvent.setup();
    render(
      <${Name} isOpen={true} onClose={mockClose} title="Test Modal">
        <p>Content</p>
      </${Name}>
    );
    await user.click(screen.getByLabelText(/close dialog/i));
    expect(mockClose).toHaveBeenCalledTimes(1);
  });

  it('has proper accessibility attributes', () => {
    render(
      <${Name} isOpen={true} onClose={mockClose} title="Accessible Modal">
        <p>Content</p>
      </${Name}>
    );
    const dialog = screen.getByRole('dialog');
    expect(dialog).toHaveAttribute('aria-labelledby');
  });
});
"@
        }
        default {
            return @"
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { ${Name} } from './${Name}';

describe('${Name}', () => {
  it('renders without crashing', () => {
    render(<${Name} />);
    expect(screen.getByRole('region', { name: '${Name}' })).toBeInTheDocument();
  });

  it('applies custom className', () => {
    render(<${Name} className="custom-class" />);
    expect(screen.getByRole('region')).toHaveClass('custom-class');
  });

  it('passes through additional props', () => {
    render(<${Name} data-testid="custom-test" />);
    expect(screen.getByTestId('custom-test')).toBeInTheDocument();
  });
});
"@
        }
    }
}

# --- Story Template ---

function Get-StoryTemplate {
    switch ($Type) {
        'modal' {
            return @"
import type { Meta, StoryObj } from '@storybook/react';
import { useState } from 'react';
import { ${Name} } from './${Name}';

const meta: Meta<typeof ${Name}> = {
  title: 'Components/${Name}',
  component: ${Name},
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof ${Name}>;

function ${Name}Demo() {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <>
      <button onClick={() => setIsOpen(true)} className="rounded bg-blue-500 px-4 py-2 text-white">
        Open Modal
      </button>
      <${Name} isOpen={isOpen} onClose={() => setIsOpen(false)} title="Example Modal">
        <p>This is the modal content.</p>
      </${Name}>
    </>
  );
}

export const Default: Story = {
  render: () => <${Name}Demo />,
};

export const Small: Story = {
  render: () => {
    const [open, setOpen] = useState(true);
    return (
      <${Name} isOpen={open} onClose={() => setOpen(false)} title="Small Modal" size="sm">
        <p>Small modal content.</p>
      </${Name}>
    );
  },
};

export const Large: Story = {
  render: () => {
    const [open, setOpen] = useState(true);
    return (
      <${Name} isOpen={open} onClose={() => setOpen(false)} title="Large Modal" size="lg">
        <p>Large modal with more content area.</p>
      </${Name}>
    );
  },
};
"@
        }
        'form' {
            return @"
import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { ${Name} } from './${Name}';

const meta: Meta<typeof ${Name}> = {
  title: 'Forms/${Name}',
  component: ${Name},
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  args: {
    onSubmit: fn(),
  },
};

export default meta;
type Story = StoryObj<typeof ${Name}>;

export const Default: Story = {};

export const WithDefaults: Story = {
  args: {
    defaultValues: {
      email: 'user@example.com',
      message: 'Pre-filled message',
    },
  },
};

export const Submitting: Story = {
  args: {
    onSubmit: () => new Promise((r) => setTimeout(r, 5000)),
  },
};
"@
        }
        default {
            return @"
import type { Meta, StoryObj } from '@storybook/react';
import { ${Name} } from './${Name}';

const meta: Meta<typeof ${Name}> = {
  title: 'Components/${Name}',
  component: ${Name},
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof ${Name}>;

export const Default: Story = {};

export const WithCustomClass: Story = {
  args: {
    className: 'bg-gray-100 p-4 rounded-lg',
  },
};
"@
        }
    }
}

# --- Generate Files ---

$componentTemplate = switch ($Type) {
    'functional' { Get-FunctionalTemplate }
    'page'       { Get-PageTemplate }
    'form'       { Get-FormTemplate }
    'modal'      { Get-ModalTemplate }
    'context'    { Get-ContextTemplate }
}

$componentFile = Join-Path $componentDir "${Name}.tsx"
Set-Content -Path $componentFile -Value $componentTemplate -Encoding utf8
Write-Host "[+] Created component: $componentFile" -ForegroundColor Green

# Index barrel
$indexContent = if ($Type -eq 'context') {
    "export { ${Name}Provider, use${Name}, type ${Name}Value, type ${Name}State } from './${Name}';"
} else {
    "export { ${Name}, type ${Name}Props } from './${Name}';`nexport { default } from './${Name}';"
}
$indexFile = Join-Path $componentDir "index.ts"
Set-Content -Path $indexFile -Value $indexContent -Encoding utf8
Write-Host "[+] Created barrel:    $indexFile" -ForegroundColor Green

if ($WithTest) {
    $testContent = Get-TestTemplate
    $testFile = Join-Path $componentDir "${Name}.test.tsx"
    Set-Content -Path $testFile -Value $testContent -Encoding utf8
    Write-Host "[+] Created test:      $testFile" -ForegroundColor Green
}

if ($WithStory -and $Type -ne 'context') {
    $storyContent = Get-StoryTemplate
    $storyFile = Join-Path $componentDir "${Name}.stories.tsx"
    Set-Content -Path $storyFile -Value $storyContent -Encoding utf8
    Write-Host "[+] Created story:     $storyFile" -ForegroundColor Green
} elseif ($WithStory -and $Type -eq 'context') {
    Write-Host "[~] Skipped story: Context components typically do not need Storybook stories" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Component '${Name}' (${Type}) scaffolded in: $componentDir" -ForegroundColor Cyan
Write-Host "Files created:" -ForegroundColor Cyan
Get-ChildItem -Path $componentDir -File | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Gray }
