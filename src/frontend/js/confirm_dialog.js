/** Confirmation modal that replaces the browser's confirm box. */

import { h } from "./dom.js";
import { ModalDialog } from "./modal_dialog.js";

export class ConfirmDialog {
    /** Asks the user to confirm an action and answers with a promise. */
    #resolver = null;

    constructor() {
        /** Initialize the dialog with its message and its two buttons. */
        this.dialog = new ModalDialog();
        this.messageElement = h("p", { class: "mb-0" });
        this.confirmButton = h("button", { type: "button", class: "btn btn-danger", onclick: () => this.#settle(true) });

        this.dialog.bodyElement.append(this.messageElement);
        this.dialog.footerElement.append(
            h("button", { type: "button", class: "btn btn-light", "data-bs-dismiss": "modal" }, "Cancel"),
            this.confirmButton
        );
        this.dialog.element.addEventListener("hidden.bs.modal", () => this.#settle(false));
    }

    ask({ title, message, confirmLabel = "Delete" }) {
        /** Show the dialog and resolve with true if the user confirms, or false if they cancel or close it. */
        this.messageElement.textContent = message;
        this.confirmButton.textContent = confirmLabel;

        return new Promise((resolve) => {
            this.#resolver = resolve;
            this.dialog.show(title);
        });
    }

    #settle(result) {
        /** Resolve the pending question once, closing the dialog when it was confirmed. */
        const resolve = this.#resolver;
        this.#resolver = null;
        resolve?.(result);

        if (result) {
            this.dialog.hide();
        }
    }
}