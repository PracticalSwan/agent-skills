/**
 * Custom Agent Finder
 *
 * This script helps you discover, inspect, and use custom agents
 * defined in the local Claude and VS Code Insiders agent directories.
 *
 * Usage: node scripts/agent-finder.js [extra-directory ...]
 */

const fs = require('fs');
const os = require('os');
const path = require('path');

const APPDATA = process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming');
const DEFAULT_SEARCH_ROOTS = [
  {
    label: 'Claude agents',
    dir: path.join(os.homedir(), '.claude', 'agents')
  },
  {
    label: 'VS Code Insiders prompts',
    dir: path.join(APPDATA, 'Code - Insiders', 'User', 'prompts')
  }
];

/**
 * Extract frontmatter from a markdown file.
 */
function extractFrontmatter(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const frontmatterMatch = content.match(/^---\n(.*?)\n---/s);

  if (!frontmatterMatch) {
    return null;
  }

  const frontmatter = {};
  const lines = frontmatterMatch[1].split('\n');

  for (const line of lines) {
    const match = line.match(/^(\w+(?:-\w+)*):\s*(.+)$/);
    if (!match) {
      continue;
    }

    const key = match[1];
    let value = match[2].trim();

    if ((value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }

    if (value === 'true') {
      value = true;
    } else if (value === 'false') {
      value = false;
    }

    frontmatter[key] = value;
  }

  return frontmatter;
}

/**
 * Build the agent search roots.
 */
function getSearchRoots() {
  const extraDirs = process.argv.slice(2).map((dir) => ({
    label: `Extra: ${path.resolve(dir)}`,
    dir: path.resolve(dir)
  }));

  return [...DEFAULT_SEARCH_ROOTS, ...extraDirs];
}

/**
 * Find all .agent.md files in the configured directories.
 */
async function findAgentFiles(searchRoots) {
  const results = [];

  for (const root of searchRoots) {
    if (!fs.existsSync(root.dir)) {
      results.push({ ...root, exists: false, files: [] });
      continue;
    }

    const files = findAgentFilesInDirectory(root.dir);

    results.push({ ...root, exists: true, files: files.sort() });
  }

  return results;
}

/**
 * Recursively find .agent.md files without external dependencies.
 */
function findAgentFilesInDirectory(rootDir) {
  const files = [];
  const skippedDirs = new Set(['node_modules', '.git', 'dist', 'build']);

  function walk(currentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);

      if (entry.isDirectory()) {
        if (!skippedDirs.has(entry.name)) {
          walk(fullPath);
        }
        continue;
      }

      if (entry.isFile() && entry.name.endsWith('.agent.md')) {
        files.push(fullPath);
      }
    }
  }

  walk(rootDir);
  return files;
}

/**
 * Get agent information from a .agent.md file.
 */
function getAgentInfo(filePath, source) {
  const frontmatter = extractFrontmatter(filePath);

  if (!frontmatter) {
    return {
      source,
      path: filePath,
      name: path.basename(filePath).replace('.agent.md', ''),
      description: null,
      invocable: false,
      tools: []
    };
  }

  return {
    source,
    path: filePath,
    name: frontmatter.name || path.basename(filePath).replace('.agent.md', ''),
    description: frontmatter.description || null,
    invocable: frontmatter['disable-model-invocation'] === false,
    tools: frontmatter.tools || []
  };
}

/**
 * Display agent information in a formatted table.
 */
function displayAgents(searchResults, agents) {
  console.log('\nSEARCH ROOTS:\n');
  for (const result of searchResults) {
    const status = result.exists ? `FOUND (${result.files.length} agent file(s))` : 'MISSING';
    console.log(`- ${result.label}: ${result.dir} -> ${status}`);
  }
  console.log();

  if (agents.length === 0) {
    console.log('No custom agents found in the configured directories.\n');
    console.log('Create *.agent.md files in one of the discovery roots above.');
    return;
  }

  console.log('='.repeat(110));
  console.log('CUSTOM AGENTS');
  console.log('='.repeat(110) + '\n');

  const invocable = agents.filter((agent) => agent.invocable);
  const nonInvocable = agents.filter((agent) => !agent.invocable);

  if (invocable.length > 0) {
    console.log('INVOCABLE AGENTS (can be used with runSubagent):\n');
    console.log('Agent Name'.padEnd(35) + 'Source'.padEnd(30) + 'Description');
    console.log('-'.repeat(110));

    for (const agent of invocable) {
      const desc = agent.description || '(no description)';
      console.log(
        agent.name.padEnd(35) +
        agent.source.padEnd(30) +
        desc.substring(0, 34)
      );
    }
    console.log();
  }

  if (nonInvocable.length > 0) {
    console.log('NON-INVOCABLE AGENTS (disable-model-invocation: true):\n');
    console.log('Agent Name'.padEnd(35) + 'Source'.padEnd(30) + 'Description');
    console.log('-'.repeat(110));

    for (const agent of nonInvocable) {
      const desc = agent.description || '(no description)';
      console.log(
        agent.name.padEnd(35) +
        agent.source.padEnd(30) +
        desc.substring(0, 34)
      );
    }
    console.log();
  }

  if (invocable.length > 0) {
    console.log('USAGE EXAMPLE:\n');
    console.log('runSubagent({');
    console.log(`  agentName: "${invocable[0].name}",`);
    console.log('  description: "Brief task description",');
    console.log('  prompt: "Detailed instructions for the agent..."');
    console.log('});\n');
  }
}

/**
 * Main function.
 */
async function main() {
  console.log('Searching for custom agents...\n');
  console.log('The VS Code Insiders prompts folder may also contain .prompt.md and .instructions.md files.');
  console.log('This script only loads *.agent.md because those are the subagent definitions.\n');

  const searchRoots = getSearchRoots();
  const searchResults = await findAgentFiles(searchRoots);
  const agents = searchResults
    .flatMap((result) => result.files.map((filePath) => getAgentInfo(filePath, result.label)))
    .sort((left, right) => left.name.localeCompare(right.name));

  displayAgents(searchResults, agents);
}

main().catch(console.error);
