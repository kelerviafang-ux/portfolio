// Optional Python runtime for static Pages that cannot reach an execution API.
// Pin the runtime so the published notebook uses a consistent Python version.
const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs';
let pythonReady;
let executionQueue = Promise.resolve();

function getPython() {
  if (!pythonReady) {
    pythonReady = import(PYODIDE_URL)
      .then(({ loadPyodide }) => loadPyodide())
      .catch((error) => {
        pythonReady = undefined;
        throw error;
      });
  }
  return pythonReady;
}

export function runPythonInBrowser(code) {
  // Serialize runs because the interpreter's output streams are shared.
  const execution = executionQueue.then(async () => {
    const python = await getPython();
    const lines = [];
    python.setStdout({ batched: (line) => lines.push(line) });
    python.setStderr({ batched: (line) => lines.push(line) });
    const globals = python.toPy({ __name__: '__main__' });
    let result;
    try {
      result = await python.runPythonAsync(code, { globals });
      return lines.join('\n') || '[no output]';
    } catch (error) {
      return [...lines, String(error)].join('\n');
    } finally {
      result?.destroy?.();
      globals.destroy();
      python.setStdout();
      python.setStderr();
    }
  });
  // A failed download must not prevent later attempts or other runners.
  executionQueue = execution.catch(() => {});
  return execution;
}
