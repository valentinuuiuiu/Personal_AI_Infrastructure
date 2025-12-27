#!/usr/bin/env bun
import { argv } from 'node:process';

const httpxMcpUrl = 'https://httpx-mcp.danielmiessler.workers.dev';
// The API key is redacted in the config.
// This script will expect it to be in an environment variable.
const apiKey = process.env.HTTPX_API_KEY;

async function main() {
  if (argv.length < 3) {
    console.error('Usage: bun run httpx.ts <url>');
    process.exit(1);
  }

  if (!apiKey) {
    console.error('Error: HTTPX_API_KEY environment variable not set.');
    console.error('Please set the HTTPX_API_KEY environment variable with the key from .mcp.json.');
    process.exit(1);
  }

  const targetUrl = argv[2];

  console.log(`Querying httpx MCP for: ${targetUrl}`);

  try {
    const response = await fetch(httpxMcpUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
      },
      body: JSON.stringify({ url: targetUrl }),
    });

    if (!response.ok) {
        const errorBody = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, body: ${errorBody}`);
    }

    const data = await response.json();
    console.log(JSON.stringify(data, null, 2));
  } catch (error) {
    console.error('Error interacting with httpx MCP:', error);
  }
}

main();
