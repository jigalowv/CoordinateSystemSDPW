/**
 * websocket.js — WebSocket connection manager
 * Exposes: wsModule.connect(), wsModule.disconnect(), wsModule.toggle()
 * Fires:   window.app.onMessage(data) when a valid JSON frame arrives
 */

window.wsModule = (() => {

  let socket    = null;
  let isOnline  = false;

  /* ── Connect ── */
  function connect() {
    const host = document.getElementById('ws-host').value.trim();
    const url  = `ws://${host}`;

    window.uiModule.log(`Connecting → ${url}`, 'info');

    try {
      socket = new WebSocket(url);

      socket.onopen = () => {
        isOnline = true;
        window.uiModule.setConnectionState(true);
        window.uiModule.log('WebSocket connected', 'ok');
      };

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (window.app && typeof window.app.onMessage === 'function') {
            window.app.onMessage(data);
          }
        } catch (e) {
          window.uiModule.log(`Parse error: ${e.message}`, 'err');
        }
      };

      socket.onclose = () => {
        isOnline = false;
        window.uiModule.setConnectionState(false);
        window.uiModule.log('Connection closed', 'err');
        socket = null;
      };

      socket.onerror = () => {
        window.uiModule.log('WebSocket error', 'err');
      };

    } catch (e) {
      window.uiModule.log(`Failed to connect: ${e.message}`, 'err');
    }
  }

  /* ── Disconnect ── */
  function disconnect() {
    if (socket) {
      socket.close();
      socket   = null;
      isOnline = false;
    }
    window.uiModule.setConnectionState(false);
    window.uiModule.log('Disconnected by user', 'info');
  }

  /* ── Toggle (used by button) ── */
  function toggle() {
    isOnline ? disconnect() : connect();
  }

  return { connect, disconnect, toggle };
})();