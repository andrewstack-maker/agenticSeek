
// Core automation masking 
delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array; 
delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise; 
delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol; 

window.RTCPeerConnection = undefined;
window.webkitRTCPeerConnection = undefined;
window.mozRTCPeerConnection = undefined;

window.Notification = class Notification {
    constructor(title, options = {}) {
        this.title = title;
        this.options = options;
    }
    static permission = 'granted';
    static requestPermission = () => Promise.resolve('granted');
    close() {}
    onclick = null;
    onerror = null;
    onclose = null;
    onshow = null;
};

Object.keys(window).forEach((key) => {
  if (key.includes("webdriver") || key.includes("selenium") || key.includes("driver")) {
    delete window[key];
  }
});

// Randomize plugins

const pluginsList = [
    {type: 'application/x-google-chrome-pdf', description: 'Portable Document Format', filename: 'internal-pdf-viewer', name: 'Chrome PDF Plugin'},
    {type: 'application/x-nacl', description: 'Native Client Executable', filename: 'internal-nacl-plugin', name: 'Native Client'},
    {type: 'application/x-ppapi-widevine-cdm', description: 'Widevine Content Decryption Module', filename: 'widevinecdm', name: 'Widevine CDM'}
];
Object.defineProperty(navigator, 'plugins', {
    get: () => pluginsList.slice(0, Math.floor(Math.random() * pluginsList.length) + 1)
});

// Font spoofing 

const fontList = ['Arial', 'Helvetica', 'Times New Roman', 'Courier New', 'Verdana'];
Object.defineProperty(document, 'fonts', {
    value: {
        add: function() {},
        check: function(font) { return fontList.includes(font.split(' ').slice(-1)[0]); },
        delete: function() {},
        forEach: function(cb) { fontList.forEach(f => cb(f)); },
        has: function(font) { return fontList.includes(font.split(' ').slice(-1)[0]); },
        keys: function() { return fontList; },
        size: fontList.length
    }
});

// Canvas fingerprint spoofing

HTMLCanvasElement.prototype.toDataURL = function() {
    const ctx = this.getContext('2d');
    // Add varied noise to avoid consistent fingerprints
    for (let i = 0; i < 10; i++) {
        ctx.fillStyle = `rgba(${Math.random() * 5}, ${Math.random() * 5}, ${Math.random() * 5}, 0.005)`;
        ctx.fillRect(Math.random() * this.width, Math.random() * this.height, 1, 1);
    }
    return originalToDataURL.apply(this, arguments);
};

const [w, h] = [1920, 1080];
Object.defineProperty(window, 'screen', {
  value: {
    width: w,
    height: h,
    availWidth: w - 20,
    availHeight: h - 100,
    colorDepth: 24,
    pixelDepth: 24
  }
});


// ===== WebGL Consistency =====
const os = navigator.userAgent.includes('Windows') ? 'Windows' : 'Mac';
const webGLParams = {
  'Windows': {
    37445: 'Google Inc. (NVIDIA)', // VENDOR
    37446: 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060)', // RENDERER
    36349: 'NVIDIA Corporation', // UNMASKED_VENDOR_WEBGL
    37444: 'NVIDIA GeForce RTX 3060', // UNMASKED_RENDERER_WEBGL
    35661: 'WebGL 2.0' // VERSION
  },
  'Mac': {
    37445: 'Apple Inc.', 
    37446: 'Apple M1 Pro',
    36349: 'Apple',
    37444: 'Apple M1 Pro',
    35661: 'WebGL 2.0 (Metal)'
  }
};

// replace WebGL parameters
WebGLRenderingContext.prototype.getParameter = function(parameter) {
    return webGLParams[os][parameter] || getParameter.call(this, parameter);
  };

// Performance API spoofing
if ('performance' in window) {
    Object.defineProperty(performance, 'memory', {
      value: {
        jsHeapSizeLimit: 4294705152,
        totalJSHeapSize: 78365432,
        usedJSHeapSize: 46543210
      },
      configurable: true
    });
  }

const originalCreate = window.AudioContext || window.webkitAudioContext;
window.AudioContext = window.webkitAudioContext = function() {
  const context = new originalCreate();
  const analyser = context.createAnalyser();
  analyser.fake = true; // Mark as spoofed
  // Spoof common methods
  analyser.getFloatFrequencyData = () => new Float32Array(1024).fill(Math.random() * -100);
  return context;
};