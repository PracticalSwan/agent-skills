# shadcn/ui Component Integration Reference

Reference for shadcn/ui components, installation, customization, and common integration patterns.

## Installation

### Project Setup

```bash
# Initialize shadcn/ui in an existing Vite + React + TypeScript project
npx shadcn-ui@latest init

# Follow prompts:
#   Style: Default or New York
#   Base color: Slate, Gray, Zinc, Neutral, Stone
#   CSS variables: Yes (recommended)
```

### Adding Components

```bash
# Add individual components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog

# Add multiple at once
npx shadcn-ui@latest add button card dialog input label
```

---

## Available Components

### Layout & Container

| Component | Install Command | Description |
|-----------|----------------|-------------|
| Card | `npx shadcn-ui@latest add card` | Container with header, content, footer sections |
| Sheet | `npx shadcn-ui@latest add sheet` | Slide-out panel from any edge |
| Separator | `npx shadcn-ui@latest add separator` | Visual divider (horizontal/vertical) |
| ScrollArea | `npx shadcn-ui@latest add scroll-area` | Custom scrollable container |
| Collapsible | `npx shadcn-ui@latest add collapsible` | Expandable/collapsible content section |
| Resizable | `npx shadcn-ui@latest add resizable` | Resizable panel groups |

### Form & Input

| Component | Install Command | Description |
|-----------|----------------|-------------|
| Button | `npx shadcn-ui@latest add button` | Button with variants: default, destructive, outline, secondary, ghost, link |
| Input | `npx shadcn-ui@latest add input` | Text input field |
| Label | `npx shadcn-ui@latest add label` | Accessible form label |
| Textarea | `npx shadcn-ui@latest add textarea` | Multi-line text input |
| Select | `npx shadcn-ui@latest add select` | Dropdown select with search |
| Checkbox | `npx shadcn-ui@latest add checkbox` | Checkbox with label |
| RadioGroup | `npx shadcn-ui@latest add radio-group` | Radio button group |
| Switch | `npx shadcn-ui@latest add switch` | Toggle switch |
| Slider | `npx shadcn-ui@latest add slider` | Range slider |
| Form | `npx shadcn-ui@latest add form` | Form wrapper with react-hook-form + zod validation |
| InputOTP | `npx shadcn-ui@latest add input-otp` | One-time password input |

### Data Display

| Component | Install Command | Description |
|-----------|----------------|-------------|
| Table | `npx shadcn-ui@latest add table` | Styled HTML table |
| Badge | `npx shadcn-ui@latest add badge` | Status/category labels |
| Avatar | `npx shadcn-ui@latest add avatar` | User avatar with fallback |
| Calendar | `npx shadcn-ui@latest add calendar` | Date picker calendar |
| Skeleton | `npx shadcn-ui@latest add skeleton` | Loading placeholder |
| Progress | `npx shadcn-ui@latest add progress` | Progress bar |

### Overlay & Feedback

| Component | Install Command | Description |
|-----------|----------------|-------------|
| Dialog | `npx shadcn-ui@latest add dialog` | Modal dialog |
| AlertDialog | `npx shadcn-ui@latest add alert-dialog` | Confirmation dialog |
| Popover | `npx shadcn-ui@latest add popover` | Floating content panel |
| Tooltip | `npx shadcn-ui@latest add tooltip` | Hover tooltip |
| Toast | `npx shadcn-ui@latest add toast` | Notification toasts |
| Alert | `npx shadcn-ui@latest add alert` | Inline alert message |
| Sonner | `npx shadcn-ui@latest add sonner` | Toast notifications (sonner-based) |

### Navigation

| Component | Install Command | Description |
|-----------|----------------|-------------|
| Tabs | `npx shadcn-ui@latest add tabs` | Tabbed interface |
| NavigationMenu | `npx shadcn-ui@latest add navigation-menu` | Site navigation |
| Menubar | `npx shadcn-ui@latest add menubar` | Horizontal menu bar |
| DropdownMenu | `npx shadcn-ui@latest add dropdown-menu` | Dropdown with items, separators, sub-menus |
| ContextMenu | `npx shadcn-ui@latest add context-menu` | Right-click context menu |
| Command | `npx shadcn-ui@latest add command` | Command palette (⌘K style) |
| Breadcrumb | `npx shadcn-ui@latest add breadcrumb` | Breadcrumb navigation |
| Pagination | `npx shadcn-ui@latest add pagination` | Page navigation |

---

## Theming with CSS Variables

### Setup in `src/index.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}
```

### Customizing Colors

Override CSS variables to match a Stitch design's color palette:

```css
:root {
  /* Map Stitch design tokens to shadcn variables */
  --primary: 24 95% 53%;        /* Orange from Stitch palette */
  --primary-foreground: 0 0% 100%;
  --accent: 142 71% 45%;         /* Green accent */
  --accent-foreground: 0 0% 100%;
  --radius: 0.75rem;             /* Match Stitch border-radius */
}
```

---

## Common UI Patterns

### Data Table with Sorting and Filtering

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

function DataTable({ data, columns }) {
  const [filter, setFilter] = useState("")
  const [sortKey, setSortKey] = useState(null)

  const filtered = data.filter(row =>
    Object.values(row).some(v => String(v).toLowerCase().includes(filter.toLowerCase()))
  )

  return (
    <div className="space-y-4">
      <Input placeholder="Filter..." value={filter} onChange={e => setFilter(e.target.value)} />
      <Table>
        <TableHeader>
          <TableRow>
            {columns.map(col => (
              <TableHead key={col.key} onClick={() => setSortKey(col.key)} className="cursor-pointer">
                {col.label}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {filtered.map(row => (
            <TableRow key={row.id}>
              {columns.map(col => (
                <TableCell key={col.key}>{row[col.key]}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
```

### Command Palette

```tsx
import { Command, CommandDialog, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"

function CommandPalette({ open, onOpenChange, items }) {
  return (
    <CommandDialog open={open} onOpenChange={onOpenChange}>
      <CommandInput placeholder="Type a command or search..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Actions">
          {items.map(item => (
            <CommandItem key={item.id} onSelect={item.onSelect}>
              {item.icon} {item.label}
            </CommandItem>
          ))}
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  )
}
```

### Multi-Step Form

```tsx
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"

function MultiStepForm({ steps }) {
  const [current, setCurrent] = useState(0)
  const progress = ((current + 1) / steps.length) * 100

  return (
    <Card className="max-w-lg mx-auto">
      <CardHeader>
        <CardTitle>{steps[current].title}</CardTitle>
        <Progress value={progress} className="mt-2" />
      </CardHeader>
      <CardContent>{steps[current].component}</CardContent>
      <CardFooter className="flex justify-between">
        <Button variant="outline" onClick={() => setCurrent(c => c - 1)} disabled={current === 0}>
          Previous
        </Button>
        <Button onClick={() => setCurrent(c => c + 1)} disabled={current === steps.length - 1}>
          {current === steps.length - 1 ? "Submit" : "Next"}
        </Button>
      </CardFooter>
    </Card>
  )
}
```

### Dashboard Layout

```tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

function DashboardLayout({ stats, charts, tables }) {
  return (
    <div className="space-y-6 p-6">
      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map(stat => (
          <Card key={stat.label}>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">{stat.label}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">{stat.change}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Tabbed Content */}
      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
        </TabsList>
        <TabsContent value="overview">{charts}</TabsContent>
        <TabsContent value="analytics">{tables}</TabsContent>
        <TabsContent value="reports">Report content</TabsContent>
      </Tabs>
    </div>
  )
}
```

---

## Stitch-to-shadcn Mapping

When converting Stitch screen designs to shadcn/ui components:

| Stitch Element | shadcn/ui Component | Notes |
|---------------|---------------------|-------|
| Hero section | Card with large padding | Use `CardHeader` + `CardContent` |
| Navigation bar | NavigationMenu or Sheet (mobile) | Combine with `Button` for actions |
| Grid of items | Card in CSS Grid | `grid grid-cols-1 md:grid-cols-3 gap-4` |
| Form fields | Form + Input + Label | Use react-hook-form + zod for validation |
| Modal/popup | Dialog or AlertDialog | `AlertDialog` for confirmations |
| Sidebar | Sheet (side="left") | Or custom sidebar with Collapsible |
| Data list | Table | Add sorting/filtering as needed |
| Status label | Badge | Variants: default, secondary, destructive, outline |
| Loading state | Skeleton | Match layout shape of real content |
| Notification | Toast or Sonner | Sonner for stacked notifications |
