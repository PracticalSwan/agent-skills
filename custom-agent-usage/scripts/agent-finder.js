/**
 * Custom Agent Finder
 *
 * This script helps you discover, inspect, and use custom agents
 * defined in .agent.md files throughout your workspace.
 *
 * Usage: node scripts/agent-finder.js
 */

const fs = require('fs');
const path = require('path');
const { glob } = require('glob');

/**
 * Extract frontmatter from a markdown file
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
    if (match) {
      const key = match[1];
      let value = match[2].trim();

      // Remove quotes from string values
      if ((value.startsWith('"') && value.endsWith('"')) ||
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }

      // Parse boolean values
      if (value === 'true') value = true;
      if (value === 'false') value = false;

      frontmatter[key] = value;
    }
  }

  return frontmatter;
}

/**
 * Find all .agent.md files in the workspace
 */
async function findAgentFiles() {
  const files = await glob('**/*.agent.md', {
    ignore: ['**/node_modules/**', '**/.git/**', '**/dist/**', '**/build/**']
  });
  return files;
}

/**
 * Get agent information from .agent.md file
 */
function getAgentInfo(filePath) {
  const frontmatter = extractFrontmatter(filePath);

  if (!frontmatter) {
    return {
      path: filePath,
      name: path.basename(filePath).replace('.agent.md', ''),
      description: null,
      invocable: false,
      tools: []
    };
  }

  return {
    path: filePath,
    name: frontmatter.name || path.basename(filePath).replace('.agent.md', ''),
    description: frontmatter.description || null,
    invocable: frontmatter['disable-model-invocation'] === false,
    tools: frontmatter.tools || []
  };
}

/**
 * Display agent information in a formatted table
 */
function displayAgents(agents) {
  if (agents.length === 0) {
    console.log('No custom agents found in workspace.\n');
    console.log('Create .agent.md files to define custom agents.');
    return;
  }

  console.log('\n' + '='.repeat(100));
  console.log('CUSTOM AGENTS IN WORKSPACE');
  console.log('='.repeat(100) + '\n');

  // Group by invocable status
  const invocable = agents.filter(a => a.invocable);
  const nonInvocable = agents.filter(a => !a.invocable);

  if (invocable.length > 0) {
    console.log('INVOCABLE AGENTS (can be used with runSubagent):\n');
    console.log('Agent Name'.padEnd(35) + 'Description');
    console.log('-'.repeat(100));

    for (const agent of invocable) {
      const desc = agent.description || '(no description)';
      console.log(agent.name.padEnd(35) + desc.substring(0, 64));
    }
    console.log();
  }

  if (nonInvocable.length > 0) {
    console.log('NON-INVOCABLE AGENTS (disable-model-invocation: true):\n');
    console.log('Agent Name'.padEnd(35) + 'Description');
    console.log('-'.repeat(100));

    for (const agent of nonInvocable) {
      const desc = agent.description || '(no description)';
      console.log(agent.name.padEnd(35) + desc.substring(0, 64));
    }
    console.log();
  }

  // Show usage example
  if (invocable.length > 0) {
    console.log('USAGE EXAMPLE:\n');
    console.log(`runSubagent({`);
    console.log(`  agentName: "${invocable[0].name}",`);
    console.log(`  description: "Brief task description",`);
    console.log(`  prompt: "Detailed instructions for the agent..."`);
    console.log(`});\n`);
  }
}

/**
 * Main function
 */
async function main() {
  console.log('Searching for custom agents...\n');

  const agentFiles = await findAgentFiles();
  const agents = agentFiles.map(getAgentInfo);

  displayAgents(agents);
}

main().catch(console.error);
