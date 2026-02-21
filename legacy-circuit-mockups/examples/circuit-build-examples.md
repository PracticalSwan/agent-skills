# Legacy Circuit Mockup Examples

## Example 1: Single LED Circuit

Creating a basic LED circuit with current-limiting resistor:

```javascript
// LED Circuit Component Layout
{
  components: [
    {
      type: 'led',
      x: 200,
      y: 200,
      color: 'red',
      properties: {
        forwardVoltage: 2.0,
        forwardCurrent: 20  // mA
      }
    },
    {
      type: 'resistor',
      x: 200,
      y: 240,
      ohms: 220,
      power: 0.25,  // Watts
      properties: {
        bands: 'red-red-brown-gold'  // 220Ω ±5%
      }
    }
  ],
  wires: [
    {
      start: { x: 100, y: 200 },  // +5V rail
      end: { x: 200, y: 200 },     // LED anode
      color: 'red'
    },
    {
      start: { x: 200, y: 240 },   // Resistor to LED cathode
      end: { x: 200, y: 260 },
      color: 'black'
    },
    {
      start: { x: 200, y: 260 },   // To GND
      end: { x: 100, y: 260 },
      color: 'black'
    }
  ]
}

// Resistor calculation: R = (Vcc - Vled) / Iled
// R = (5V - 2V) / 0.02A = 150Ω → use 220Ω (standard value)
```

## Example 2: 555 Timer Astable Multivibrator

Creating a blinking LED circuit with 555 timer:

```javascript
// 555 Astable Circuit
{
  components: [
    {
      type: 'ic-555',
      x: 300,
      y: 200,
      rotation: 0,
      properties: {
        pins: 8,
        mode: 'astable'
      }
    },
    {
      type: 'resistor',
      x: 360,
      y: 180,
      ohms: 10000,  // 10kΩ (R1)
      label: 'R1'
    },
    {
      type: 'resistor',
      x: 380,
      y: 220,
      ohms: 100000,  // 100kΩ (R2)
      label: 'R2'
    },
    {
      type: 'capacitor',
      x: 360,
      y: 260,
      farads: 10e-6,  // 10µF (C)
      type: 'electrolytic',
      label: 'C'
    },
    {
      type: 'led',
      x: 420,
      y: 200,
      color: 'green'
    }
  ],
  connections: [
    // Pin 1 (GND) → Ground rail
    { pin: 1, to: 'gnd' },
    // Pin 8 (Vcc) → +5V rail
    { pin: 8, to: 'vcc' },
    // Pin 4 (RESET) → Pin 8 (disable reset)
    { from: 4, to: 8 },
    // R1 between Pin 7 and Vcc
    { from: 'r1-start', to: 'vcc' },
    { from: 'r1-end', to: 7 },
    // R2 between Pin 7 and Pin 6
    { from: 'r2-start', to: 7 },
    { from: 'r2-end', to: 6 },
    // C between Pin 6 and GND
    { from: 6, to: 'c-positive' },
    { from: 'c-negative', to: 'gnd' },
    // Pin 2 (TRIG) connected to Pin 6 (THR)
    { from: 2, to: 6 },
    // Pin 3 (OUT) to LED
    { from: 3, to: 'led-anode' }
  ]
}

// Frequency calculation:
// f = 1.44 / ((R1 + 2×R2) × C)
// f = 1.44 / ((10000 + 200000) × 10e-6)
// f ≈ 0.69 Hz → ~1.5 second blink cycle
```

## Example 3: 6502 Microprocessor Minimal System

Creating a minimal 6502 computer circuit:

```javascript
// 6502 Minimal System Layout
{
  components: [
    // Microprocessor
    {
      type: 'ic-6502',
      x: 400,
      y: 300,
      properties: {
        pins: 40,
        label: 'W65C02S'
      }
    },
    // Program memory (EEPROM)
    {
      type: 'ic-28c256',
      x: 400,
      y: 100,
      properties: {
        pins: 28,
        capacity: '32KB',
        label: '28C256 EEPROM'
      }
    },
    // I/O Adapter
    {
      type: 'ic-6522',
      x: 600,
      y: 300,
      properties: {
        pins: 40,
        label: 'W65C22 VIA'
      }
    },
    // Clock crystal
    {
      type: 'crystal',
      x: 250,
      y: 320,
      frequency: 1000000,  // 1 MHz
      label: '1 MHz'
    },
    // Reset button
    {
      type: 'button',
      x: 200,
      y: 350,
      label: 'RESET'
    }
  ],
  buses: [
    // Address bus (A0-A15) - Blue wires
    {
      name: 'Address Bus',
      color: 'blue',
      lines: [
        { from: '6502-A0', to: 'EEPROM-A0' },
        { from: '6502-A1', to: 'EEPROM-A1' },
        // ... A2-A14
        { from: '6502-A15', to: 'CS-decoder' }
      ]
    },
    // Data bus (D0-D7) - Green wires
    {
      name: 'Data Bus',
      color: 'green',
      lines: [
        { from: '6502-D0', to: 'EEPROM-D0' },
        { from: '6502-D1', to: 'EEPROM-D1' },
        // ... D2-D6
        { from: '6502-D7', to: 'EEPROM-D7' }
      ]
    }
  ],
  control_signals: [
    // Clock - Yellow wire
    { name: 'PHI2', from: 'clock', to: '6502-PIN37', color: 'yellow' },
    // Read/Write - Orange wire
    { name: 'R/W', from: '6502-PIN34', to: 'EEPROM-W27', color: 'orange' },
    // Reset - White wire
    { name: 'RESB', from: 'reset-button', to: '6502-PIN40', color: 'white' }
  ]
}
```

## Example 4: 7400 NAND Gate Logic

Creating a basic logic gate circuit:

```javascript
// 7400 Quad 2-Input NAND Gate
{
  components: [
    {
      type: 'ic-7400',
      x: 300,
      y: 200,
      properties: {
        pins: 14,
        gates: 4,
        label: 'SN7400'
      }
    },
    {
      type: 'led',
      x: 400,
      y: 220,
      color: 'red',
      label: 'Output'
    },
    {
      type: 'switch',
      x: 200,
      y: 180,
      label: 'Input A'
    },
    {
      type: 'switch',
      x: 200,
      y: 240,
      label: 'Input B'
    }
  ],
  connections: [
    // Switch A to Gate 1 input A (Pin 1)
    { from: 'switch-a', to: 'pin-1' },
    // Switch B to Gate 1 input B (Pin 2)
    { from: 'switch-b', to: 'pin-2' },
    // Gate 1 output (Pin 3) to LED
    { from: 'pin-3', to: 'led-anode' },
    // Pin 7 to GND, Pin 14 to Vcc
    { pin: 7, to: 'gnd' },
    { pin: 14, to: 'vcc' }
  ]
}

// Truth table for NAND gate:
// A | B | Output
// 0 | 0 |   1
// 0 | 1 |   1
// 1 | 0 |   1
// 1 | 1 |   0
```

## Example 5: Complete Breadboard Layout

Full breadboard with power rails and component placement:

```javascript
// Complete Breadboard Layout
{
  breadboard: {
    width: 620,  // 31 columns × 20px
    height: 420, // 21 rows × 20px
    power_rails: {
      top: {
        positive: { y: 20, color: 'red' },
        negative: { y: 40, color: 'blue' }
      },
      bottom: {
        positive: { y: 380, color: 'red' },
        negative: { y: 400, color: 'blue' }
      }
    }
  },
  placement: [
    // IC placement (straddling center divide)
    {
      component: 'ic-555',
      position: { x: 200, y: 200 },
      orientation: 'horizontal',
      note: 'Pins 1-4 left, 5-8 right of center'
    },
    // Passive components
    {
      component: 'resistor-220',
      position: { x: 300, y: 180 },
      orientation: 'vertical'
    },
    {
      component: 'capacitor-10uF',
      position: { x: 320, y: 260 },
      orientation: 'vertical',
      note: 'Negative stripe to ground'
    },
    // Output
    {
      component: 'led-red',
      position: { x: 400, y: 220 },
      orientation: 'vertical',
      note: 'Long leg to positive, short leg to resistor'
    }
  ]
}
```
