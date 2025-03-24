function findInputs(element, result = []) {
    // Find all <input> elements in the current DOM tree
    const inputs = element.querySelectorAll('input');
    inputs.forEach(input => {
        result.push({
            tagName: input.tagName,
            text: input.name || '',
            type: input.type || '',
            class: input.className || '',
            xpath: getXPath(input),
            displayed: isElementDisplayed(input)
        });
    });
    const allElements = element.querySelectorAll('*');
    allElements.forEach(el => {
        if (el.shadowRoot) {
            findInputs(el.shadowRoot, result);
        }
    });
    return result;
}
// function to get the XPath of an element
function getXPath(element) {
    if (!element) return '';
    if (element.id !== '') return '//*[@id="' + element.id + '"]';
    if (element === document.body) return '/html/body';

    let ix = 0;
    const siblings = element.parentNode ? element.parentNode.childNodes : [];
    for (let i = 0; i < siblings.length; i++) {
        const sibling = siblings[i];
        if (sibling === element) {
            return getXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
        }
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
            ix++;
        }
    }
    return '';
}
return findInputs(document.body);

function isElementDisplayed(element) {
    const style = window.getComputedStyle(element);
    if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
        return false;
    }
    return true;
}