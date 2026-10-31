/** Thin wrapper around fetch that talks JSON with the backend and turns failures into errors. */

export class ApiError extends Error {}


export class ApiClient {
    /** Sends JSON requests to the backend API. */
    constructor(baseUrl = "") {
        this.baseUrl = baseUrl;
    }

    async request(method, path, body = undefined) {
        /** Send a request and return the parsed JSON body, or null when the response has no content. */
        const response = await fetch(`${this.baseUrl}${path}`, {
            method,
            headers: body === undefined ? {} : { "Content-Type": "application/json" },
            body: body === undefined ? undefined : JSON.stringify(body)
        });

        if (!response.ok) {
            throw new ApiError(await this.#extractMessage(response));
        }

        return response.status === 204 ? null : response.json();
    }

    async #extractMessage(response) {
        /** Build a readable message from the error body, whether it is a domain error or a validation error. */
        try {
            const { detail } = await response.json();

            if (typeof detail === "string") {
                return detail;
            }
            if (Array.isArray(detail)) {
                return detail.map((issue) => `${issue.loc.slice(1).join(".")}: ${issue.msg}`).join("; ");
            }
        } catch {
        }

        return `The request failed (${response.status}).`;
    }
}