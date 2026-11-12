const root = new URL('./vendor/', import.meta.url);
const loadScript = (name) => new Promise((resolve, reject) => {
  const script = document.createElement('script');
  script.src = new URL(name, root).href;
  script.onload = resolve;
  script.onerror = () => reject(new Error('Unable to load ' + name));
  document.head.append(script);
});
async function diagrams() {
  const nodes = [...document.querySelectorAll('pre.mermaid')];
  if (!nodes.length) return;
  const sources = nodes.map((node) => node.textContent);
  await loadScript('mermaid.min.js');
  let pending = Promise.resolve();
  const draw = () => {
    pending = pending.then(async () => {
      nodes.forEach((node, i) => { node.textContent = sources[i]; node.removeAttribute('data-processed'); });
      window.mermaid.initialize({
        startOnLoad: false, securityLevel: 'strict',
        theme: document.documentElement.dataset.theme === 'dark' ? 'dark' : 'default',
      });
      await window.mermaid.run({ nodes });
    }).catch((error) => {
      console.error('Diagram rendering failed', error);
      nodes.forEach((node, i) => { node.textContent = sources[i]; });
    });
  };
  draw();
  new MutationObserver(draw).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
}
async function recordings() {
  const nodes = [...document.querySelectorAll('.asciinema-cast')];
  if (!nodes.length) return;
  const css = document.createElement('link');
  css.rel = 'stylesheet'; css.href = new URL('asciinema-player.css', root).href; document.head.append(css);
  await loadScript('asciinema-player.min.js');
  for (const node of nodes) window.AsciinemaPlayer.create(node.dataset.src, node, { fit: 'width', idleTimeLimit: 2 });
}
diagrams().catch(console.error);
recordings().catch(console.error);
