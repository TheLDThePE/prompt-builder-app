function sendMessageToStreamlitClient(type, data) {
  window.parent.postMessage(
    Object.assign({ isStreamlitMessage: true, type }, data || {}),
    "*"
  );
}

const Streamlit = {
  setComponentReady() {
    sendMessageToStreamlitClient("streamlit:componentReady", { apiVersion: 1 });
  },
  setFrameHeight(height) {
    sendMessageToStreamlitClient("streamlit:setFrameHeight", { height });
  },
  setComponentValue(value) {
    sendMessageToStreamlitClient("streamlit:setComponentValue", { value });
  },
};
