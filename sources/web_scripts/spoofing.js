
// Core automation masking 
Object.defineProperty(navigator, 'webdriver', {get: () => undefined}); 
delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array; 
delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise; 
delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol; 

Object.keys(window).forEach((key) => {
  if (key.includes("webdriver") || key.includes("selenium") || key.includes("driver")) {
    delete window[key];
  }
});

// Forceful chrome object spoofing 
try { 
    Object.defineProperty(window, 'chrome', { 
        writable: true, 
        configurable: true, 
        value: { 
            app: {isInstalled: false}, 
            webstore: {onInstallStageChanged: {}, onDownloadProgress: {}}, 
            runtime: { 
                PlatformOs: {MAC: 'mac', WIN: 'win', ANDROID: 'android'}, 
                PlatformArch: {ARM: 'arm', X86_32: 'x86-32', X86_64: 'x86-64'}, 
                PlatformNaclArch: {ARM: 'arm', X86_32: 'x86-32', X86_64: 'x86-64'}, 
                RequestUpdateCheckStatus: { 
                    THROTTLED: 'throttled', 
                    NO_UPDATE: 'no_update', 
                    UPDATE_AVAILABLE: 'update_available' 
                }, 
                OnInstalledReason: { 
                    INSTALL: 'install', 
                    UPDATE: 'update', 
                    SHARED_MODULE_UPDATE: 'shared_module_update' 
                }, 
                OnRestartRequiredReason: { 
                    APP_UPDATE: 'app_update', 
                    OS_UPDATE: 'os_update', 
                    PERIODIC: 'periodic' 
                } 
            } 
        } 
    }); 
} catch (e) { 
    console.log("Error in defining window.chrome: ", e);
    // Fallback: direct assignment 
    window.chrome = window.chrome || {}; 
    window.chrome.app = {isInstalled: false}; 
    window.chrome.webstore = {onInstallStageChanged: {}, onDownloadProgress: {}}; 
}

// Randomize plugins
const pluginsList = [
    {type: 'application/x-google-chrome-pdf', description: 'Portable Document Format', filename: 'internal-pdf-viewer', name: 'Chrome PDF Plugin'},
    {type: 'application/x-nacl', description: 'Native Client Executable', filename: 'internal-nacl-plugin', name: 'Native Client'},
    {type: 'application/x-ppapi-widevine-cdm', description: 'Widevine Content Decryption Module', filename: 'widevinecdm', name: 'Widevine CDM'}
];
Object.defineProperty(navigator, 'plugins', {
    get: () => pluginsList.slice(0, Math.floor(Math.random() * pluginsList.length) + 1)
});

// Font spoofing with randomized font list
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
const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
HTMLCanvasElement.prototype.toDataURL = function() {
    const ctx = this.getContext('2d');
    ctx.fillStyle = `rgba(${Math.random() * 10},${Math.random() * 10},${Math.random() * 10},0.01)`;
    ctx.fillRect(0, 0, 1, 1);
    return originalToDataURL.apply(this, arguments);
};

// Screen resolution spoofing
const resolutions = [[1920, 1080], [1366, 768], [1440, 900]];
const [w, h] = resolutions[Math.floor(Math.random() * resolutions.length)];
Object.defineProperty(window, 'screen', {
    value: {
        width: w,
        height: h,
        availWidth: w,
        availHeight: h - 50,
        colorDepth: 24,
        pixelDepth: 24
    }
});

// Timezone and language spoofing
Object.defineProperty(navigator, 'language', {get: () => 'en-US'});
Intl.DateTimeFormat = function() {
    return {resolvedOptions: () => ({timeZone: 'America/New_York'})};
};

// AudioContext spoofing
const originalCreate = window.AudioContext || window.webkitAudioContext;
window.AudioContext = window.webkitAudioContext = function() {
    const context = new originalCreate();
    const dest = context.createAnalyser();
    dest.fake = true;
    return context;
};

// WebRTC spoofing
Object.defineProperty(navigator, 'mediaDevices', {
    get: () => undefined
});
Object.defineProperty(navigator, 'getUserMedia', {
    get: () => undefined
});

// web gl spoofing
const getParameter = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function(parameter) {
    // Common WebGL parameters
    const params = {
        37445: 'Intel Open Source Technology Center', // VENDOR
        37446: 'Mesa DRI Intel® HD Graphics 4000',   // RENDERER
        34076: 'WebKit WebGL',                       // SHADING_LANGUAGE_VERSION
        35661: '2.1 INTEL-16.4.5',                   // VERSION
        36349: 'Intel Inc.'                          // UNMASKED_VENDOR_WEBGL
    };
    return params[parameter] || getParameter.call(this, parameter);
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

  // Battery API spoofing
if ('getBattery' in navigator) {
    Object.defineProperty(navigator, 'getBattery', {
      value: () => Promise.resolve({
        level: 0.85,
        charging: true,
        chargingTime: 1800,
        dischargingTime: Infinity,
        onchargingchange: null,
        onchargingtimechange: null,
        ondischargingtimechange: null,
        onlevelchange: null
      }),
      configurable: true
    });
  }

window.RTCPeerConnection = undefined;
window.webkitRTCPeerConnection = undefined;
window.mozRTCPeerConnection = undefined;

Object.defineProperty(navigator, 'permissions', {
    value: {
        query: () => Promise.resolve({ state: 'denied' })
    }
});
Object.defineProperty(navigator, 'languages', {
    get: () => ['en-US', 'en'],
});

const canvas = document.createElement('canvas');
const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

if (gl) {
    // Store original getParameter function
    const originalGetParameter = gl.getParameter;
    // Override getParameter to spoof values
    gl.getParameter = function(parameter) {
        // UNMASKED_VENDOR_WEBGL
        if (parameter === 37445) return 'Intel Inc.';
        // UNMASKED_RENDERER_WEBGL
        if (parameter === 37446) return 'Intel Iris Pro OpenGL Engine';
        // Other common fingerprint points
        if (parameter === gl.VERSION) return 'WebGL 2.0 (OpenGL ES 3.0 Intel)';
        if (parameter === gl.SHADING_LANGUAGE_VERSION) return 'WebGL GLSL ES 3.00 (OpenGL ES GLSL ES 3.0)';
        
        // Default to original behavior
        return originalGetParameter.call(gl, parameter);
    };
    
    // Spoof debug renderer info extension
    const debugInfo = {
        getExtension: function(name) {
            if (name === 'WEBGL_debug_renderer_info') {
                return {
                    UNMASKED_VENDOR_WEBGL: 37445,
                    UNMASKED_RENDERER_WEBGL: 37446,
                    __proto__: WebGLExtension.prototype
                };
            }
            return null;
        },
        __proto__: WebGLRenderingContext.prototype
    };
    
    // Override getExtension
    const originalGetExtension = gl.getExtension;
    gl.getExtension = function(name) {
        if (name === 'WEBGL_debug_renderer_info') {
            return debugInfo;
        }
        return originalGetExtension.call(gl, name);
    };
    
    // Freeze objects to prevent detection
    Object.freeze(gl);
    Object.freeze(debugInfo);
}