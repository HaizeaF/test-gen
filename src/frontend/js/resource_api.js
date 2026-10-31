/** CRUD access to one REST resource of the backend. */

export class ResourceApi {
    /** Wraps the four operations every resource of the API supports. */
    constructor(client, path) {
        this.client = client;
        this.path = path;
    }

    list() {
        return this.client.request("GET", this.path);
    }

    create(payload) {
        return this.client.request("POST", this.path, payload);
    }

    update(id, payload) {
        return this.client.request("PATCH", `${this.path}/${id}`, payload);
    }

    remove(id) {
        return this.client.request("DELETE", `${this.path}/${id}`);
    }
}