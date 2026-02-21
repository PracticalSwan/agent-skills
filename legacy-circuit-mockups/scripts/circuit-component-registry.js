/**
 * Legacy Circuit Component Registry
 *
 * This script defines the complete component registry for
 * legacy circuit mockups, including pinouts, dimensions,
 * and rendering specifications.
 */

// Grid system
const GRID_SIZE = 20;

// Component registry
const COMPONENT_REGISTRY = {
  // Microprocessors
  'W65C02S': {
    type: 'cpu',
    pins: 40,
    width: 200,  // 10 grid columns
    height: 100, // 5 grid rows
    color: '#3B82F6',
    pinout: {
      // Power
      8: 'VDD',
      21: 'VSS',
      // Clock
      37: 'PHI2',
      // Control
      40: 'RESB',
      34: 'RWB',
      // Address bus (A0-A15)
      9: 'A0', 10: 'A1', 11: 'A2',
      12: 'A3', 13: 'A4', 14: 'A5',
      15: 'A6', 16: 'A7', 17: 'A8',
      18: 'A9', 19: 'A10', 20: 'A11',
      22: 'A12', 23: 'A13', 24: 'A14',
      25: 'A15',
      // Data bus (D0-D7)
      26: 'D0', 27: 'D1', 28: 'D2',
      29: 'D3', 30: 'D4', 31: 'D5',
      32: 'D6', 33: 'D7'
    }
  },

  // Memory
  '28C256': {
    type: 'eeprom',
    pins: 28,
    width: 160,
    height: 80,
    color: '#10B981',
    pinout: {
      14: 'GND', 28: 'VCC',
      20: 'CE', 22: 'OE', 27: 'WE',
      // Address (A0-A14)
      1: 'A0', 2: 'A1', 3: 'A2',
      4: 'A3', 5: 'A4', 6: 'A5',
      7: 'A6', 8: 'A7', 9: 'A8',
      10: 'A9', 21: 'A10', 23: 'A11',
      24: 'A12', 25: 'A13', 26: 'A14',
      // Data (I/O0-I/O7)
      11: 'I/O0', 12: 'I/O1', 13: 'I/O2',
      14: 'I/O3', 15: 'I/O4', 16: 'I/O5',
      17: 'I/O6', 18: 'I/O7'
    }
  },

  '62256': {
    type: 'ram',
    pins: 28,
    width: 160,
    height: 80,
    color: '#8B5CF6',
    pinout: {
      14: 'GND', 28: 'VCC',
      20: 'CE', 22: 'OE', 27: 'WE'
    }
  },

  // VIA
  'W65C22': {
    type: 'via',
    pins: 40,
    width: 200,
    height: 100,
    color: '#F59E0B',
    pinout: {
      8: 'VDD', 21: 'VSS',
      // Port A
      2: 'PA0', 3: 'PA1', 4: 'PA2',
      5: 'PA3', 6: 'PA4', 7: 'PA5',
      8: 'PA6', 9: 'PA7',
      // Port B
      10: 'PB0', 11: 'PB1', 12: 'PB2',
      13: 'PB3', 14: 'PB4', 15: 'PB5',
      16: 'PB6', 17: 'PB7'
    }
  },

  // Timer IC
  'NE555': {
    type: 'timer',
    pins: 8,
    width: 80,
    height: 60,
    color: '#EF4444',
    pinout: {
      1: 'GND',
      2: 'TRIG',
      3: 'OUT',
      4: 'RESET',
      5: 'CTRL',
      6: 'THR',
      7: 'DIS',
      8: 'VCC'
    }
  },

  // Logic gates (7400 series)
  '7400': {
    type: 'logic-nand',
    pins: 14,
    width: 100,
    height: 70,
    color: '#6B7280',
    description: 'Quad 2-input NAND',
    gates: [
      { inputs: [1, 2], output: 3 },
      { inputs: [4, 5], output: 6 },
      { inputs: [9, 10], output: 8 },
      { inputs: [12, 13], output: 11 }
    ]
  },

  '7402': {
    type: 'logic-nor',
    pins: 14,
    width: 100,
    height: 70,
    color: '#6B7280',
    description: 'Quad 2-input NOR'
  },

  '7404': {
    type: 'logic-not',
    pins: 14,
    width: 100,
    height: 70,
    color: '#6B7280',
    description: 'Hex inverter'
  },

  '7408': {
    type: 'logic-and',
    pins: 14,
    width: 100,
    height: 70,
    color: '#6B7280',
    description: 'Quad 2-input AND'
  },

  '7432': {
    type: 'logic-or',
    pins: 14,
    width: 100,
    height: 70,
    color: '#6B7280',
    description: 'Quad 2-input OR'
  },

  // Passive components
  'resistor': {
    type: 'resistor',
    width: 60,
    height: 20,
    color: '#D97706',
    defaultValues: [220, 1000, 10000, 22000, 100000],
    bands: ['brown', 'black', 'red', 'gold']  // 1kΩ
  },

  'capacitor-ceramic': {
    type: 'capacitor',
    subtype: 'ceramic',
    width: 30,
    height: 20,
    color: '#9CA3AF'
  },

  'capacitor-electrolytic': {
    type: 'capacitor',
    subtype: 'electrolytic',
    width: 40,
    height: 60,
    color: '#1F2937',
    polarity: true
  },

  // Active components
  'led': {
    type: 'led',
    width: 30,
    height: 30,
    colors: ['red', 'green', 'yellow', 'blue', 'white'],
    forwardVoltages: {
      red: 2.0,
      green: 2.2,
      yellow: 2.0,
      blue: 3.2,
      white: 3.2
    }
  },

  'crystal': {
    type: 'crystal',
    width: 50,
    height: 30,
    frequencies: [1000000, 4000000, 8000000, 16000000]
  },

  // Controls
  'switch': {
    type: 'switch',
    width: 60,
    height: 40,
    poles: 1,
    throws: 2
  },

  'button': {
    type: 'button',
    width: 40,
    height: 40,
    momentary: true
  },

  'potentiometer': {
    type: 'potentiometer',
    width: 60,
    height: 60,
    defaultValues: [10000, 50000, 100000]
  }
};

// Wire color standards
const WIRE_COLORS = {
  red: '+5V / Power',
  black: 'Ground',
  yellow: 'Clock / Timing',
  blue: 'Address bus',
  green: 'Data bus',
  orange: 'Control signals',
  white: 'General purpose'
};

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    COMPONENT_REGISTRY,
    WIRE_COLORS,
    GRID_SIZE
  };
}
