import { json } from '@sveltejs/kit';
import { spawn } from 'child_process';
import path from 'path';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
  const { command } = await request.json();

  if (!command) {
    return json({ error: 'No command provided' }, { status: 400 });
  }

  const [cmd, ...args] = command.split(' ');

  let scriptArgs: string[];

  // Use path.resolve to get an absolute path from the project root
  const paiPath = path.resolve(process.cwd(), 'pai/pai.py');

  if (cmd === 'ask') {
    scriptArgs = ['ask', ...args, '--stream'];
  } else if (cmd === 'run_agent') {
    scriptArgs = ['run_agent', ...args, '--stream'];
  } else {
    return json({ error: 'Unknown command' }, { status: 400 });
  }

  try {
    const stream = new ReadableStream({
      start(controller) {
        const process = spawn('python3', [paiPath, ...scriptArgs]);

        process.stdout.on('data', (data) => {
          controller.enqueue(data.toString());
        });

        process.stderr.on('data', (data) => {
          console.error(`stderr: ${data}`);
        });

        process.on('close', (code) => {
          if (code !== 0) {
            controller.error(new Error(`Process exited with code ${code}`));
          } else {
            controller.close();
          }
        });

        request.signal.addEventListener('abort', () => {
          process.kill();
          controller.close();
        });
      },
    });

    return new Response(stream, {
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
      },
    });

  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
    return json({ error: errorMessage }, { status: 500 });
  }
};
