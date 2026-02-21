/**
 * Agent Discovery Script
 *
 * This script helps discover available custom agents in the workspace
 * by searching for .agent.md files and extracting their frontmatter.
 *
 * Usage: node scripts/agent-discovery.js
 */

const fs = require('fs');
const path = require('path');

/**
 * Recursively find all .agent.md files in a directory
 */
function findAgentFiles(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      // Skip node_modules and hidden directories
      if (!entry.name.startsWith('.') && entry.name !== 'node_modules') {
        findAgentFiles(fullPath, files);
      }
    } else if (entry.name.endsWith('.agent.md')) {
      files.push(fullPath);
    }
  }

  return files;
}

/**
 * Extract agent name and description from .agent.md file
 */
function extractAgentInfo(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const frontmatterMatch = content.match(/^---\n(.*?)\n---/s);

  if (!frontmatterMatch) {
    return { path: filePath, name: null, description: null, invocable: null };
  }

  const frontmatter = frontmatterMatch[1];
  const nameMatch = frontmatter.match(/name:\s*["']?([^"'\n]+)["']?/);
  const descMatch = frontmatter.match(/description:\s*(.+)$/);
  const invocationMatch = frontmatter.match(/disable-model-invocation:\s*(false|true)/);

  return {
    path: filePath,
    name: nameMatch ? nameMatch[1].trim() : null,
    description: descMatch ? descMatch[1].trim() : null,
    invocable: invocationMatch ? invocationMatch[1] === 'false' : null
  };
}

/**
 * Main function to discover and display agents
 */
function main() {
  const workspaceDir = process.cwd();
  console.log(`Searching for agents in: ${workspaceDir}\n`);

  const agentFiles = findAgentFiles(workspaceDir);

  if (agentFiles.length === 0) {
    console.log('No .agent.md files found.');
    return;
  }

  console.log(`Found ${agentFiles.length} agent(s):\n`);

  const agents = agentFiles.map(extractAgentInfo);

  // Display table of agents
  console.log('Agent Name'.padEnd(40) + 'Invocable'.padEnd(12) + 'Description');
  console.log('='.repeat(120));

  for (const agent of agents) {
    const name = agent.name || '(unnamed)';
    const invocable = agent.invocable === null ? '?' : (agent.invocable ? 'Yes' : 'No');
    const description = agent.description || '(no description)';
    console.log(
      name.padEnd(40) +
      invocable.padEnd(12) +
      description.substring(0, 65)
    );
  }

  console.log('\n');
  console.log('Invocable agents can be used with runSubagent({ agentName: "..." })');
  console.log('Non-invocable agents have disable-model-invocation: true');
}

main();
