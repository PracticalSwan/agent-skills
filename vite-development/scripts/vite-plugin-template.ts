/**
 * Vite Plugin Template
 *
 * This is a template for creating custom Vite plugins.
 * Copy and modify this template for your specific use case.
 *
 * Usage:
 * 1. Rename the plugin class
 * 2. Implement the transform or handleHotUpdate hooks
 * 3. Add your custom logic
 * 4. Export the plugin function
 */

import type { Plugin, TransformResult } from 'vite';

interface PluginOptions {
  /**
   * Enable/disable the plugin
   * @default true
   */
  enabled?: boolean;

  /**
   * Files to include (glob pattern)
   * @default '**/*.{js,jsx,ts,tsx,vue}'
   */
  include?: string;

  /**
   * Files to exclude (glob pattern)
   * @default 'node_modules/**'
   */
  exclude?: string;

  /**
   * Custom transform function
   */
  transform?: (code: string, id: string) => string | null;
}

/**
 * Create a new Vite plugin instance
 */
export function createPlugin(options: PluginOptions = {}): Plugin {
  const {
    enabled = true,
    include = '**/*.{js,jsx,ts,tsx,vue}',
    exclude = 'node_modules/**',
  } = options;

  return {
    name: 'vite-plugin-template',

    // Plugin configuration
    config(config) {
      return {
        // Modify Vite config
        resolve: {
          alias: {
            // Add aliases
          },
        },
      };
    },

    // Transform files during build
    transform(code, id) {
      if (!enabled) return null;

      // Skip excluded files
      if (id.includes(exclude)) return null;

      // Process only included file types
      if (!/\.(js|jsx|ts|tsx|vue)$/.test(id)) return null;

      // Use custom transform if provided
      if (options.transform) {
        const result = options.transform(code, id);
        if (result) return { code: result };
      }

      return null;
    },

    // Handle hot module replacement
    handleHotUpdate(ctx) {
      if (!enabled) return;

      const { file, modules, read } = ctx;

      // Custom HMR logic
      if (file.endsWith('.vue')) {
        // Force Vue component reload
        return modules;
      }
    },

    // Configure build process
    configResolved(config) {
      // Access final Vite config
      console.log('Vite config resolved:', config.mode);
    },

    // Build hooks
    buildStart() {
      console.log('Build started');
    },

    buildEnd() {
      console.log('Build ended');
    },

    // Server hooks
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        // Custom middleware
        if (req.url?.startsWith('/custom')) {
          res.statusCode = 200;
          res.end('Custom response');
        } else {
          next();
        }
      });
    },
  };
}

/**
 * Example: File size reporting plugin
 */
export function fileSizeReporter(): Plugin {
  return {
    name: 'file-size-reporter',
    generateBundle(_, bundle) {
      for (const [fileName, file] of Object.entries(bundle)) {
        if ('code' in file) {
          const size = Buffer.byteLength(file.code, 'utf-8');
          const kb = (size / 1024).toFixed(2);
          console.log(`[file-size-reporter] ${fileName}: ${kb} KB`);
        }
      }
    },
  };
}

/**
 * Example: SVG sprite generator plugin
 */
export function svgSpritePlugin(options: { inputDir: string; outputFile: string }): Plugin {
  return {
    name: 'svg-sprite-generator',
    async buildStart() {
      // Read SVG files and generate sprite
      const fs = await import('fs/promises');
      const path = await import('path');

      try {
        const files = await fs.readdir(options.inputDir);
        const svgs = files.filter(f => f.endsWith('.svg'));

        let spriteContent = '<svg xmlns="http://www.w3.org/2000/svg">';
        for (const file of svgs) {
          const content = await fs.readFile(path.join(options.inputDir, file), 'utf-8');
          const symbolId = file.replace('.svg', '');
          const innerContent = content.replace('<svg', '').replace('</svg>', '').replace(/xmlns="[^"]*"/, '');
          spriteContent += `<symbol id="${symbolId}"${innerContent}</symbol>`;
        }
        spriteContent += '</svg>';

        this.emitFile({
          type: 'asset',
          fileName: options.outputFile,
          source: spriteContent,
        });
      } catch (error) {
        console.error('Error generating SVG sprite:', error);
      }
    },
  };
}

/**
 * Example: Environment variable validator plugin
 */
export function envValidatorPlugin(requiredVars: string[]): Plugin {
  return {
    name: 'env-validator',
    config(config) {
      const missing = requiredVars.filter(v => !process.env[v]);
      if (missing.length > 0) {
        throw new Error(
          `Missing required environment variables: ${missing.join(', ')}`
        );
      }
      return config;
    },
  };
}

/**
 * Example: Bundle analyzer plugin
 */
export function bundleAnalyzerPlugin(options: { outputDir: string }): Plugin {
  return {
    name: 'bundle-analyzer',
    generateBundle(_, bundle) {
      const fs = await import('fs/promises');
      const path = await import('path');

      const analysis = [];
      let totalSize = 0;

      for (const [fileName, file] of Object.entries(bundle)) {
        if ('code' in file) {
          const size = Buffer.byteLength(file.code, 'utf-8');
          totalSize += size;
          analysis.push({ fileName, size, kb: (size / 1024).toFixed(2) });
        }
      }

      // Sort by size
      analysis.sort((a, b) => b.size - a.size);

      // Generate report
      const report = {
        totalSize,
        totalKb: (totalSize / 1024).toFixed(2),
        files: analysis,
      };

      const outputPath = path.join(options.outputDir, 'bundle-analysis.json');
      await fs.mkdir(options.outputDir, { recursive: true });
      await fs.writeFile(outputPath, JSON.stringify(report, null, 2));

      console.log(`[bundle-analyzer] Report written to ${outputPath}`);
    },
  };
}

// Export default plugin
export default createPlugin;
