---
name: legacy-circuit-mockups
version: "1.2"
last_updated: 2026-04-25
tags: [legacy, circuit, mockups, design, frontend]
description: "Breadboard circuit mockups via HTML5 Canvas. Use when creating circuit layouts, visualizing 6502/retro electronics components, drawing breadboard diagrams, or designing vintage computer schematics with discrete parts."
---

# Legacy Circuit Mockups

A skill for creating breadboard circuit mockups and visual diagrams for retro computing and electronics projects. This skill leverages HTML5 Canvas drawing mechanisms to render interactive circuit layouts featuring vintage components like the 6502 microprocessor, 555 timer ICs, EEPROMs, and 7400-series logic gates.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## When to Use This Skill

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- User asks to create a breadboard layout or circuit mockup
- User wants visualized component placement for legacy electronics
- User needs diagrams for 6502, 555 timer, EEPROM, VIA, or 7400-series builds
- User asks for educational electronics visuals or wiring diagrams
- User is following retro-computing tutorials and needs visual references

## Prerequisites

- Understanding of component pinouts from bundled reference files
- Knowledge of breadboard layout conventions (rows, columns, power rails)

## Supported Components

### Microprocessors & Memory

| Component | Pins | Description |
|-----------|------|-------------|
| W65C02S | 40-pin DIP | 8-bit microprocessor with 16-bit address bus |
| 28C256 | 28-pin DIP | 32KB parallel EEPROM |
| W65C22 | 40-pin DIP | Versatile Interface Adapter (VIA) |
| 62256 | 28-pin DIP | 32KB static RAM |

### Logic & Timer ICs

| Component | Pins | Description |
|-----------|------|-------------|
| NE555 | 8-pin DIP | Timer IC for timing and oscillation |
| 7400 | 14-pin DIP | Quad 2-input NAND gate |
| 7402 | 14-pin DIP | Quad 2-input NOR gate |
| 7404 | 14-pin DIP | Hex inverter (NOT gate) |
| 7408 | 14-pin DIP | Quad 2-input AND gate |
| 7432 | 14-pin DIP | Quad 2-input OR gate |

### Passive & Active Components

| Component | Description |
|-----------|-------------|
| LED | Light emitting diode (various colors) |
| Resistor | Current limiting (configurable values) |
| Capacitor | Filtering and timing (ceramic/electrolytic) |
| Crystal | Clock oscillator |
| Switch | Toggle switch (latching) |
| Button | Momentary push button |
| Potentiometer | Variable resistor |
| Photoresistor | Light-dependent resistor |

### Grid System

```javascript
// Standard breadboard grid: 20px spacing
const gridSize = 20;
const cellX = Math.floor(x / gridSize) * gridSize;
const cellY = Math.floor(y / gridSize) * gridSize;
```

### Component Rendering Pattern

```javascript
// All components follow this structure:
{
  type: 'component-type',
  x: gridX,
  y: gridY,
  width: componentWidth,
  height: componentHeight,
  rotation: 0,  // 0, 90, 180, 270
  properties: { /* component-specific data */ }
}
```

### Wire Connections

```javascript
// Wire connection format:
{
  start: { x: startX, y: startY },
  end: { x: endX, y: endY },
  color: '#ff0000'  // Wire color coding
}
```

## Step-by-Step Workflows

### Creating a Basic LED Circuit Mockup

1. Define breadboard dimensions and grid
2. Place power rail connections (+5V and GND)
3. Add LED component with anode/cathode orientation
4. Place current-limiting resistor
5. Draw wire connections between components
6. Add labels and annotations

### Creating a 555 Timer Circuit

1. Place NE555 IC on breadboard (pins 1-4 left, 5-8 right)
2. Connect pin 1 (GND) to ground rail
3. Connect pin 8 (Vcc) to power rail
4. Add timing resistors and capacitors
5. Wire trigger and threshold connections
6. Connect output to LED or other load

### Creating a 6502 Microprocessor Layout

1. Place W65C02S centered on breadboard
2. Add 28C256 EEPROM for program storage
3. Place W65C22 VIA for I/O
4. Add 7400-series logic for address decoding
5. Wire address bus (A0-A15)
6. Wire data bus (D0-D7)
7. Connect control signals (R/W, PHI2, RESB)
8. Add reset button and clock crystal

## Component Pinout Quick Reference

### 555 Timer (8-pin DIP)

| Pin | Name | Function |
|:---:|:-----|:---------|
| 1 | GND | Ground (0V) |
| 2 | TRIG | Trigger (< 1/3 Vcc starts timing) |
| 3 | OUT | Output (source/sink 200mA) |
| 4 | RESET | Active-low reset |
| 5 | CTRL | Control voltage (bypass with 10nF) |
| 6 | THR | Threshold (> 2/3 Vcc resets) |
| 7 | DIS | Discharge (open collector) |
| 8 | Vcc | Supply (+4.5V to +16V) |

### W65C02S (40-pin DIP) - Key Pins

| Pin | Name | Function |
|:---:|:-----|:---------|
| 8 | VDD | Power supply |
| 21 | VSS | Ground |
| 37 | PHI2 | System clock input |
| 40 | RESB | Active-low reset |
| 34 | RWB | Read/Write signal |
| 9-25 | A0-A15 | Address bus |
| 26-33 | D0-D7 | Data bus |

### 28C256 EEPROM (28-pin DIP) - Key Pins

| Pin | Name | Function |
|:---:|:-----|:---------|
| 14 | GND | Ground |
| 28 | VCC | Power supply |
| 20 | CE | Chip enable (active-low) |
| 22 | OE | Output enable (active-low) |
| 27 | WE | Write enable (active-low) |
| 1-10, 21-26 | A0-A14 | Address inputs |
| 11-19 | I/O0-I/O7 | Data bus |

## Formulas Reference

### Resistor Calculations

- **Ohm's Law:** V = I × R
- **LED Current:** R = (Vcc - Vled) / Iled
- **Power:** P = V × I = I² × R

### 555 Timer Formulas

**Astable Mode:**

- Frequency: f = 1.44 / ((R1 + 2×R2) × C)
- High time: t₁ = 0.693 × (R1 + R2) × C
- Low time: t₂ = 0.693 × R2 × C
- Duty cycle: D = (R1 + R2) / (R1 + 2×R2) × 100%

**Monostable Mode:**

- Pulse width: T = 1.1 × R × C

### Capacitor Calculations

- Capacitive reactance: Xc = 1 / (2πfC)
- Energy stored: E = ½ × C × V²

## Color Coding Conventions

### Wire Colors

| Color | Purpose |
|-------|---------|
| Red | +5V / Power |
| Black | Ground |
| Yellow | Clock / Timing |
| Blue | Address bus |
| Green | Data bus |
| Orange | Control signals |
| White | General purpose |

### LED Colors

| Color | Forward Voltage |
|-------|-----------------|
| Red | 1.8V - 2.2V |
| Green | 2.0V - 2.2V |
| Yellow | 2.0V - 2.2V |
| Blue | 3.0V - 3.5V |
| White | 3.0V - 3.5V |

## Anti-Patterns

- Starting from a generic template without adapting it: The output may look polished but still miss the real audience or medium.
- Ignoring final render or export review: Layout bugs often appear only after the asset is opened in its destination tool.
- Fixing content and presentation in one pass: It becomes hard to tell whether a problem is structural or visual.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Legacy Circuit Mockups implementation names the target runtime, framework version, and affected files.
2. Pass/fail: Build, lint, test, or equivalent local validation is run for the changed surface.
3. Pass/fail: Edge cases for errors, dependency drift, and environment differences are addressed or explicitly out of scope.
4. Pressure-test scenario: Apply the workflow to a change that passes happy-path tests but fails one boundary condition.
5. Success metric: Zero untested success claims; every implementation claim maps to a command or artifact.


## Build Examples

### Build 1 — Single LED

**Components:** Red LED, 220Ω resistor, jumper wires, power source

**Steps:**

1. Insert black jumper wire from power GND to row A5
2. Insert red jumper wire from power +5V to row J5
3. Place LED with cathode (short leg) in row aligned with GND
4. Place 220Ω resistor between power and LED anode

### Build 2 — 555 Astable Blinker

**Components:** NE555, LED, resistors (10kΩ, 100kΩ), capacitor (10µF)

**Steps:**

1. Place 555 IC straddling center channel
2. Connect pin 1 to GND, pin 8 to +5V
3. Connect pin 4 to pin 8 (disable reset)
4. Wire 10kΩ between pin 7 and +5V
5. Wire 100kΩ between pins 6 and 7
6. Wire 10µF between pin 6 and GND
7. Connect pin 3 (output) to LED circuit

## Troubleshooting

| Issue | Solution |
|-------|----------|
| LED doesn't light | Check polarity (anode to +, cathode to -) |
| Circuit doesn't power | Verify power rail connections |
| IC not working | Check VCC and GND pin connections |
| 555 not oscillating | Verify threshold/trigger capacitor wiring |
| Microprocessor stuck | Check RESB is HIGH after reset pulse |

## References

Detailed component specifications are available in the bundled reference files:

### Documentation
- [555](references/555.md) — Complete 555 timer IC specification
- [6502](references/6502.md) — MOS 6502 microprocessor details
- [6522](references/6522.md) — W65C22 VIA interface adapter
- [28256-eeprom](references/28256-eeprom.md) — AT28C256 EEPROM specification
- [6C62256](references/6C62256.md) — 62256 SRAM details
- [7400-series](references/7400-series.md) — TTL logic gate pinouts
- [assembly-compiler](references/assembly-compiler.md) — Assembly compiler specification
- [assembly-language](references/assembly-language.md) — Assembly language specification
- [basic-electronic-components](references/basic-electronic-components.md) — Resistors, capacitors, switches
- [breadboard](references/breadboard.md) — Breadboard specifications
- [common-breadboard-components](references/common-breadboard-components.md) — Comprehensive component reference
- [connecting-electronic-components](references/connecting-electronic-components.md) — Step-by-step build guides
- [emulator-28256-eeprom](references/emulator-28256-eeprom.md) — Emulating 28256-eeprom specification
- [emulator-6502](references/emulator-6502.md) — Emulating 6502 specification
- [emulator-6522](references/emulator-6522.md) — Emulating 6522 specification
- [emulator-6C62256](references/emulator-6C62256.md) — Emulating 6C62256 specification
- [emulator-lcd](references/emulator-lcd.md) — Emulating a LCD specification
- [lcd](references/lcd.md) — LCD display interfacing
- [minipro](references/minipro.md) — EEPROM programmer usage
- [t48eeprom-programmer](references/t48eeprom-programmer.md) — T48 programmer reference

### Examples
- [Circuit Build Examples](examples/circuit-build-examples.md) — Example circuit layouts and component configurations

### Scripts
- [Circuit Component Registry](scripts/circuit-component-registry.js) — Component registry for circuit mockups


---

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:legacy-circuit-mockups` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py legacy-circuit-mockups` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Legacy Circuit Mockups skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [frontend-design](../frontend-design/SKILL.md): Use it when the workflow also needs UI composition and front-end design direction.
- [premium-frontend-ui](../premium-frontend-ui/SKILL.md): Use it when the workflow also needs high-fidelity UI polish and interaction detail.
- [web-design-reviewer](../web-design-reviewer/SKILL.md): Use it when the workflow also needs browser-based UI review and responsive QA.
- [stitch-design](../stitch-design/SKILL.md): Use it when the workflow also needs turning interface designs into implementation-ready assets.
