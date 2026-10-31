/** Generic Bootstrap modal that other components fill with their own content. */

import { h } from "./dom.js";

export class ModalDialog {
    /** Builds the modal structure and exposes its title, body and footer. */
    constructor({ asForm = false, size = "" } = {}) {
        this.titleElement = h("h2", { class: "modal-title h5" });
        this.bodyElement = h("div", { class: "modal-body" });
        this.footerElement = h("div", { class: "modal-footer" });

        this.content = h(
                asForm ? "form" : "div",
                { class: "modal-content" },
                h(
                    "div",
                    { class: "modal-header" },
                    this.titleElement,
                    h("button", { type: "button", class: "btn-close", "data-bs-dismiss": "modal", "aria-label": "Close" })
                ),
                this.bodyElement,
                this.footerElement,
            );
        this.element = h(
            "div",
            { class: "modal fade", tabindex: "-1", "aria-hidden": "true" },
            h("div", { class: `modal-dialog modal-dialog-centered modal-dialog-scrollable ${size}` }, this.content)
        );

        document.body.append(this.element);
        this.modal = new bootstrap.Modal(this.element);
    }

    show(title) {
        /** Open the modal with the given title. */
        this.titleElement.textContent = title;
        this.modal.show();
    }

    hide() {
        /** Close the modal. */
        this.modal.hide();
    }
}