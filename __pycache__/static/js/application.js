// static/js/application.js

// Support TLS-specific URLs, when appropriate.
if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};

var ws = new ReconnectingWebSocket(ws_scheme + location.host + "/shenron");