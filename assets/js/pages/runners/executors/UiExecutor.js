export class UiExecutor {
  constructor({ editor, outputElement, language = 'javascript' } = {}) {
    this.editor = editor;
    this.outputElement = outputElement;
    this.language = language;
    this.currentExecution = null;
  }

  stop() {
    if (this.outputElement) {
      this.outputElement.innerHTML = '';
    }

    if (this.currentExecution && typeof this.currentExecution.stop === 'function') {
      this.currentExecution.stop();
    }

    this.currentExecution = null;
  }

  run() {
    const code = this.editor?.getValue?.() || '';
    this.stop();

    try {
      const outputElement = this.outputElement;
      if (this.language === 'html') {
        outputElement.innerHTML = code;
        // Scripts inserted with innerHTML are inert. Run inline scripts explicitly
        // so HTML notebook exercises can wire up controls inside this output.
        const scripts = [...outputElement.querySelectorAll('script')]
          .filter(script => !script.src && (!script.type || script.type === 'text/javascript'));
        if (scripts.length) {
          const runScripts = new Function('outputElement', `
            'use strict';
            ${scripts.map(script => script.textContent).join('\n')}
          `);
          this.currentExecution = runScripts(outputElement);
        }
        return;
      }
      const userFunction = new Function('outputElement', `
        'use strict';
        ${code}
      `);

      this.currentExecution = userFunction(outputElement);
    } catch (err) {
      if (this.outputElement) {
        const message = document.createElement('pre');
        message.setAttribute('role', 'alert');
        message.textContent = `Error: ${err.message}`;
        this.outputElement.replaceChildren(message);
      }
    }
  }
}

export default UiExecutor;
