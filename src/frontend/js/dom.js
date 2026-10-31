/** DOM helper that keeps element creation short and safe. */

export function h(tag, attributes = {}, ...children) {
    /** Create an element with attributes and children. */
    const element = document.createElement(tag);
    element.append(...children.flat().filter((child) => child !== null && child !== undefined && child !== false));

    for (const [name, value] of Object.entries(attributes)) {
        if (value === null || value === undefined || value === false) {
        continue;
        }

        if (name === "class") {
            element.className = value;
        } else if (name.startsWith("on")) {
            element.addEventListener(name.slice(2), value);
        } else if (name === "value" || name === "checked") {
            element[name] = value;
        } else {
            element.setAttribute(name, value === true ? "" : value);
        }
    }

    return element;
}