(() => {
  const button = document.getElementById("copy-button");
  let currentArgs = {};
  let lastEventId = null;

  function handleRender(event) {
    currentArgs = event.data.args || {};
    button.textContent = currentArgs.before_copy_label || "Copy prompt";
    button.disabled = false;
  }

  window.addEventListener("message", (event) => {
    if (event.data && event.data.type === "streamlit:render") {
      handleRender(event);
    }
  });

  button.addEventListener("click", async () => {
    if (!currentArgs.text) return;
    button.disabled = true;
    try {
      await navigator.clipboard.writeText(currentArgs.text);
      lastEventId = (window.crypto && crypto.randomUUID)
        ? crypto.randomUUID()
        : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
      button.textContent = currentArgs.after_copy_label || "Copied";
      Streamlit.setComponentValue({ copied: true, event_id: lastEventId });
      window.setTimeout(() => {
        button.textContent = currentArgs.before_copy_label || "Copy prompt";
        button.disabled = false;
      }, 1200);
    } catch (_error) {
      button.textContent = "คัดลอกไม่สำเร็จ กรุณาลองอีกครั้ง";
      button.disabled = false;
    }
  });

  Streamlit.setComponentReady();
  Streamlit.setFrameHeight(56);
})();
