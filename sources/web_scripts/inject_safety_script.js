// Block hardware access by removing or disabling APIs
Object.defineProperty(navigator, 'serial', { get: () => undefined });
Object.defineProperty(navigator, 'hid', { get: () => undefined });
Object.defineProperty(navigator, 'bluetooth', { get: () => undefined });
// Block media playback
HTMLMediaElement.prototype.play = function() {
    this.pause(); // Immediately pause if play is called
    return Promise.reject('Blocked by script');
};
// Block fullscreen requests
Element.prototype.requestFullscreen = function() {
    console.log('Blocked fullscreen request');
    return Promise.reject('Blocked by script');
};
// Block pointer lock
Element.prototype.requestPointerLock = function() {
    console.log('Blocked pointer lock');
};
//block fetch
window.fetch = function() {
    console.log('Blocked fetch request');
    return Promise.reject('Blocked');
};

window.prompt = function() { return null; };